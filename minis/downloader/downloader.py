from bs4 import BeautifulSoup
import re
import os
import requests
from requests.auth import HTTPBasicAuth
import threading, queue
import json

from .show_info import *

# downloadAllMinis.py - Downloads .stl files of miniatures

# Process
# 1. Get all HTML Pages
# 2. Get end of last HTML Page
# 3. Iterate through all the pages, create list of urls to files
# 4. Obtain list of names of all files
# 6. Create master index hash table.
# 7. Look up each url, get the file, download and save as filename

site       = "https://www.shapeways.com/designer/mz4250/creations"
HTML       = "./html"

pages = queue.Queue()       # pages => HTML Pages
saved = queue.Queue()       # saved => Save HTML Pages As [filename]

minis_links = queue.Queue() # Links to Minis
ids = queue.Queue()         # Product-ID
names = queue.Queue()       # Mini Name

def createSoup(fileName):
    with open(fileName, 'r') as f: 
        soup = BeautifulSoup(f, 'html.parser')
        return soup

def createDir(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

def writeToFile(html, fileName):
    with open(fileName, 'w') as f:
        f.write(html)

def saveHTML():
    html = requests.get(pages.get()).text
    writeToFile(html, saved.get())

def downloadHTML():
    while (not pages.empty() and not saved.empty()):
        if (threading.active_count() <= 4):
            worker = threading.Thread(target=saveHTML)
            worker.start()
        else:
            for thread in threading.enumerate():
                if (thread is threading.main_thread()): 
                    continue
                else: 
                    thread.join()

def getPages(soup):
    regexp = r"(/designer/mz4250/creations\?s=\d{0,4}#more-products)"
    pages = soup.find_all('a', href = re.compile(regexp))
    return pages

def pushBackPage(currentPage, saveAs):
    pages.put(currentPage)
    saved.put(saveAs)

def getHTMLPage(site, pageIndex, index, directory):
    currentPage = (f'{site}?s={pageIndex}') 
    saveAs = (f'{directory}/mz4250-creations-page-{index}') 
    return currentPage, saveAs

def getAllHTML(soup, directory, index = 1, pageIndex = 0):
    end = getEnd(getPages(soup))
    while (pageIndex < end):
        currentPage, saveAs = getHTMLPage(site, pageIndex, index, directory)
        if (not os.path.exists(saveAs)):
            pushBackPage(currentPage, saveAs, pages, saved)
        pageIndex += 48
        index += 1

    currentPage, saveAs = getHTMLPage(site, end, index, directory)
    pushBackPage(currentPage, saveAs, pages, saved)
    downloadHTML()

def createHeaders():
    headers = { 
        'Content-type': 'application/zip',
        'Host': 'www.shapeways.com',
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Referer': minis_links.get(),
        'Cookie': '__cfduid=dd4e4ad5a12f3eeb9a89139f43b137d211608008733; shapeways_guest=2ad9b47812f7643badebb042252d45aefa12e9eb; whid=9; PHPSESSID=u1bh765cf6oosb7dcco7433gdc; sw_usr=187af943d900b0a1753cb31f192f4f1f06854c9c; uauth=2343099'
    }
    return headers

def loadCredentials(creds_file = 'creds.json'):
    with open(creds_file) as f: 
        data = json.load(f)
    return data['username'], data['password']

def getEnd(tag):
    exp = r"(?<=/designer/mz4250/creations\?s=)(\d{1,4})(?=#more-products)"
    regexp = re.compile(exp)
    index = regexp.search(tag[5]['href'])
    return int(index.group(0))

def getLinks(site, soup):
    exp = r"\"?(https://www.shapeways.com/product/\w{9}/)(\w*-*)*(\?optionId=\d{1,16})(.*user-profile)\"?"
    URLS = soup.find_all('a', href = re.compile(exp))

    print(f"============ Links ============")
    linkList = list(map(lambda url: url['href'], URLS))

    linkDict = dict.fromkeys(linkList, 1)
    for link in linkDict: 
        minis_links.put(link)
        print(f"link: {link}")
    print(f"")
    return linkDict

def removeEmpty(name): 
    if(name): # if null
        return True
    else:
        return False

def getNames(site, soup):
    exp = r"\"?(https://www.shapeways.com/product/\w{9}/)(\w*-*)*(\?optionId=\d{1,16})(.*user-profile)\"?"
    results = soup.find_all('a', href = re.compile(exp))
    print(f"============ Names ============")
    nameList = list(filter(removeEmpty, map(lambda name: name.get_text(strip=True), results)))
    nameDict = dict.fromkeys(nameList, 1)
    for name in nameDict: 
        names.put(name)
        print(f"name: {name}")
    print(f"")

def getIds(links, soup): 
    exp = r"(\"?)(?<=https://www.shapeways.com/product/)(\w+)"
    regex = re.compile(exp)

    print(f"============ Ids ============")
    for link in links:
        print(f"ids: {link}")
        ids.put(regex.search(link).group(0))
    print(f"")

def downloadMini():
    if (ids.empty() or names.empty() or minis_links.empty()):
        print(f"No miniatures to download...")
        return

    # while (not ids.empty() and not names.empty()):
    mini_id         = ids.get()
    name            = names.get()
    downloadLink    = (f'https://www.shapeways.com/product/download/{mini_id}')
    printMiniMetadata(mini_id, name, downloadLink)

    session = requests.Session()
    mini = session.get(downloadLink, allow_redirects=True, headers=createHeaders(), auth=(loadCredentials()))
    if (mini.status_code != 404):
        with open(f"{name}.zip", 'wb') as f:
            f.write(mini.content)
