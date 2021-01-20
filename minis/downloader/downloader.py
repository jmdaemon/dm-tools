from bs4 import BeautifulSoup
import re
import os
import requests
from requests.auth import HTTPBasicAuth
import threading, queue
import json

from .show_info import *

# downloadAllMinis.py - Downloads .stl files of miniatures

site        = "https://www.shapeways.com/designer/mz4250/creations"
mini_dir    = "miniatures"

pages = queue.Queue()       # pages => HTML Pages
saved = queue.Queue()       # saved => Save HTML Pages As [filename]

links = queue.Queue()
mini_links = queue.Queue()
mini_saved = queue.Queue()
names = queue.Queue()
downloadLinks = queue.Queue()

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

def writeToFile(content, fileName, modes = 'w'):
    with open(fileName, modes) as f:
        f.write(content)

def saveHTML():
    html = requests.get(pages.get()).text
    writeToFile(html, saved.get())

def download(firstQueue, secondQueue, target):
    while (not firstQueue.empty() and not secondQueue.empty()):
        if (threading.active_count() <= 4): worker = threading.Thread(target=target).start() 
        else:
            list = [thread.join for thread in threading.enumerate() if thread is not threading.main_thread()]
    
def getPages(soup):
    regexp = r"(/designer/mz4250/creations\?s=\d{0,4}#more-products)"
    pages = soup.find_all('a', href = re.compile(regexp))
    return pages

def getAllHTML(soup, directory = "./html", index = 1, offset = 0, dry_run = False):
    if(os.path.exists(directory)):
        print(f"Directory {directory} already exists.")
        return
    elif (not os.path.exists(directory)):
        os.makedirs(directory)
    end = getEnd(getPages(soup))
    pagesList = [f'{site}?s={offset}' for offset in ([*range(offset, end, 48)] + [end])]
    savedList = [f'{directory}/mz4250-creations-page-{index}' for index in range(index, len(pagesList) + 1)]
    list = [pages.put(page) for page in pagesList]
    list = [saved.put(saveFile) for saveFile in savedList]
    if (not dry_run): download(pages, saved, saveHTML)

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

def pushOntoQueue(title, keyword, itemList, itemQueue):
    itemDict = createDict(title, keyword, itemList)
    result = [itemQueue.put(item) for item in itemDict]
    return itemDict

def removeEmpty(name): 
    if(name): # if null
        return True
    else:
        return False

def createDict(title, keyword, itemList):
    itemDict = dict.fromkeys(itemList, 1)
    print(f"============ {title} ============")
    list = [print(f"{keyword}: {item}") for item in itemDict] + [print(f"")]
    return itemDict

def getLinks(site, soup):
    exp = r"\"?(https://www.shapeways.com/product/\w{9}/)(\w*-*)*(\?optionId=\d{1,16})(.*user-profile)\"?"
    URLS = soup.find_all('a', href = re.compile(exp))
    linkList = list(map(lambda url: url['href'], URLS))
    # return createDict("Links", "link", linkList)
    pushOntoQueue("Links", "link", linkList, links)

def getNames(site, soup):
    exp = r"\"?(https://www.shapeways.com/product/\w{9}/)(\w*-*)*(\?optionId=\d{1,16})(.*user-profile)\"?"
    results = soup.find_all('a', href = re.compile(exp))
    nameList = list(filter(removeEmpty, map(lambda name: name.get_text(strip=True), results)))
    return pushOntoQueue("Names", "name", nameList, names)

# def getIds(links, soup): 
def getIds(soup): 
    exp = r"(\"?)(?<=https://www.shapeways.com/product/)(\w+)"
    regex = re.compile(exp)
    idsList = [regex.search(link).group(0) for link in links.queue]
    return createDict("Ids", "id", idsList)

def saveMini():
    # mini = requests.get(downloadLinks.get(), allow_redirects=True, headers=createHeaders(), auth=(loadCredentials()))
    print(f"Saving as: {mini_dir}/{names.get()}.zip", flush=True)
    # if (mini.status_code != 404):
        # print(f"Saving as: {mini_dir}/{names.get()}.zip")
        # writeToFile(mini.content, f"{mini_dir}/{names.get()}.zip", 'wb')

def downloadMini(mini_ids, directory = "miniatures"):
    if (not os.path.exists(directory)):
        os.makedirs(directory)
        mini_dir = directory
    list = [downloadLinks.put(f'https://www.shapeways.com/product/download/{mini_id}') for mini_id in mini_ids]
    download(downloadLinks, names, saveMini)
    print(f"")

def getMiniMetadata():
    printProductMetadata(mini_saved, mini_links)
    # html = requests.get(links.get()).text
    # writeToFile(html, names.get())

# def getProductHTML(soup, links, mini_names, directory = "./html/products", index = 1, offset = 0, dry_run = False):
# def getProductHTML(soup, links, directory = "./html/products", index = 1, offset = 0, dry_run = False):
def getProductHTML(soup, directory = "./html/products", index = 1, offset = 0, dry_run = False):
    if(os.path.exists(directory)):
        print(f"Directory {directory} already exists.")
        return
    elif (not os.path.exists(directory)):
        os.makedirs(directory)
    # minis_savedList = [f"{directory}/page-{index}/{name}".replace(" ", "-") for name in mini_names]
    # print(names.queue)
    # mini_names = [name for name in names.queue]
    # minis_savedList = [f"{directory}/{name}".replace(" ", "-") for name in mini_names]
    minis_savedList = [f"{directory}/{name}".replace(" ", "-") for name in names.queue]
    list = [mini_saved.put(mini_savedData) for mini_savedData in minis_savedList]
    list = [mini_links.put(mini_link) for mini_link in links.queue]
    print(f"============ Mini Metadata ============")
    if (not dry_run): download(mini_links, mini_saved, getMiniMetadata) 
    os.rmdir(directory)
    print(f"")
