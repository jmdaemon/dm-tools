from bs4 import BeautifulSoup
import re
import os
import requests
import cProfile
import threading, queue
import json

from requests.auth import HTTPBasicAuth

# downloadAllMinis.py - Downloads .stl files of miniatures

# Process
# 1. Get all HTML Pages
# 2. Get end of last HTML Page
# 3. Iterate through all the pages, create list of urls to files
# 4. Obtain list of names of all files
# 6. Create master index hash table.
# 7. Look up each url, get the file, download and save as filename

pages = queue.Queue()
saved = queue.Queue()

def createSoup(filename):
    f = open(filename, "r") 
    soup = BeautifulSoup(f, 'html.parser')
    return soup

def makeHTMLDir(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

def writeToFile(html, fileName):
    with open(fileName, 'w') as f:
        f.write(html)

def getHTML(site): 
    page = requests.get(site)
    return page.text

def getHTMLParallel():
    html = getHTML(pages.get())
    writeToFile(html, saved.get())

def printDownload(currentPage, pageIndex, saveAs):
    print(f'currentPage : {currentPage}')
    print(f'pageIndex   : {pageIndex}')
    print(f'saveAs      : {saveAs}')

def downloadHTML():
    while (not pages.empty() and not saved.empty()):
        if (threading.active_count() <= 4):
            worker = threading.Thread(target=getHTMLParallel)
            worker.start()
        else:
            for thread in threading.enumerate():
                if (thread is threading.main_thread()): 
                    continue
                else: 
                    thread.join()

def getAllHTML(end, site, directory):
    index = 1
    pageIndex = 0
    while (pageIndex < end):
        currentPage, saveAs = Pages.getHTMLPage(pageIndex, index)
        if (not os.path.exists(saveAs)):
            Pages.pushBackPage(currentPage, saveAs)
        pageIndex += 48
        index += 1

    pageIndex = end 
    currentPage, saveAs = Pages.getHTMLPage(pageIndex, index)
    Pages.pushBackPage(currentPage, saveAs)
    downloadHTML()

minis_links = queue.Queue()
ids = queue.Queue()
names = queue.Queue()

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

def printMiniMetadata(mini_id, name, downloadLink):
    print(f"mini_id         : {mini_id}")
    print(f"name            : {name}")
    print(f"downloadLink    : {downloadLink}")
    print(f"")

def downloadMini(soup, creds_file = 'creds.json'):
    if (ids.empty() or names.empty() or minis_links.empty()):
        print(f"No miniatures to download...")
        return

    mini_id         = ids.get()
    name            = names.get()
    downloadLink    = (f'https://www.shapeways.com/product/download/{mini_id}')
    printMiniMetadata(mini_id, name, downloadLink)

    session = requests.Session()
    headers = createHeaders()

    with open(creds_file) as f: 
        data = json.load(f)

    print(data['username'] + " " + data['password'])

    # mini = session.get(downloadLink, allow_redirects=True, headers=headers, auth=(data['username'], data['password']))
    # if (mini.status_code != 404):
        # print(mini.text)
        # with open('test.zip', 'wb') as f:
            # f.write(mini.content)

    # print (mini.headers)
    # print (mini.request.headers)

# path = "./html"
site = "https://www.shapeways.com/designer/mz4250/creations"

# writeToFile(getHTMLPage(site), path + "/mz4250-creations-page-1")
# getAllHTML(end)

# end = getEnd(getPages(createSoup("creations.html")))
# getAllHTML(end, site, "./html")
# soup = createSoup("creations.html")
soup = createSoup("./html/mz4250-creations-page-1")

# links = getLinks(site, soup)
# getNames(site, soup)
# getIds(links, soup)
# downloadMini(soup)
