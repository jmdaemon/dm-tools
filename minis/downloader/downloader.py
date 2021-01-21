from bs4 import BeautifulSoup
import re
import os
import requests
from requests.auth import HTTPBasicAuth
import threading, queue
import json

from .show_info import *
from .extract import *
from .fileutils import *

# downloadAllMinis.py - Downloads .stl files of miniatures

def createSoup(fileName):
    with open(fileName, 'r') as f: 
        soup = BeautifulSoup(f, 'html.parser')
        return soup

def extractProductPages(soup):
    regexp = r"(/designer/mz4250/creations\?s=\d{0,4}#more-products)"
    pages = soup.find_all('a', href = re.compile(regexp))
    return pages

def extractEnd(tag):
    exp = r"(?<=/designer/mz4250/creations\?s=)(\d{1,4})(?=#more-products)"
    regexp = re.compile(exp)
    index = regexp.search(tag[5]['href'])
    return int(index.group(0))

def saveHTML(pages, saved):
    writeToFile(requests.get(pages.get()).text, saved.get())

def download(target, args):
    if (threading.active_count() <= 4): worker = threading.Thread(target=target, args=args).start() 
    else:
        list = [thread.join for thread in threading.enumerate() if thread is not threading.main_thread()]
    
def listToQueue(itemList):
    itemQueue = queue.Queue()
    list = [itemQueue.put(item) for item in itemList]
    return itemQueue 

def getCreationsHTML(soup, site="https://www.shapeways.com/designer/mz4250/creations", directory = "./html", index = 1, offset = 0, dry_run = False):
    if (dirExists(directory)): return
    end = extractEnd(extractProductPages(soup))
    pagesList = [f'{site}?s={offset}' for offset in ([*range(offset, end, 48)] + [end])]
    pages = listToQueue(pagesList)
    saved = listToQueue([f'{directory}/mz4250-creations-page-{index}' for index in range(index, len(pagesList) + 1)])
    if (not dry_run):
        while (not pages.empty() and not saved.empty()):
            download(saveHTML, args=(pages, saved)) 

def createHeaders(links):
    headers = { 
        'Content-type': 'application/zip',
        'Host': 'www.shapeways.com',
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Referer': links.get(),
        'Cookie': '__cfduid=dd4e4ad5a12f3eeb9a89139f43b137d211608008733; shapeways_guest=2ad9b47812f7643badebb042252d45aefa12e9eb; whid=9; PHPSESSID=u1bh765cf6oosb7dcco7433gdc; sw_usr=187af943d900b0a1753cb31f192f4f1f06854c9c; uauth=2343099'
    }
    return headers

def loadCredentials(creds_file = 'creds.json'):
    with open(creds_file) as f: 
        data = json.load(f)
    return data['username'], data['password']

def retrieveMiniature(directory, downloadLinks, links, names):
    mini = requests.get(downloadLinks.get(), allow_redirects=True, headers=createHeaders(links), auth=(loadCredentials()))
    print(f"Saving as: {directory}/{names.get()}.zip", flush=True)
    if (mini.status_code != 404):
        writeToFile(mini.content, f"{directory}/{names.get()}.zip", 'wb')

def downloadMiniature(metadata, directory = "miniatures"):
    if (dirExists(directory)): return
    downloadLinks = listToQueue([(f'https://www.shapeways.com/product/download/{mini_id}') for mini_id in metadata.ids.queue])
    while (not downloadLinks.empty() and not metadata.names.empty()):
        download(retrieveMiniature, args=(directory, downloadLinks, metadata.links, metadata.names)) 
    print(f"")

def printMetadata(LinksQueue, SavedQueue):
    printProductMetadata(SavedQueue, LinksQueue)

def getProductHTML(soup, metadata, directory = "./html/products", index = 1, offset = 0, dry_run = False):
    if(dirExists(directory)): return
    SavedQueue = listToQueue([f"{directory}/{name}".replace(" ", "-") for name in metadata.names.queue])
    if (not dry_run): 
        while (not metadata.links.empty() and not SavedQueue.empty()):
            download(printMetadata, args=(metadata.links, SavedQueue)) 
    os.rmdir(directory)
