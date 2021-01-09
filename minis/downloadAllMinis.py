from bs4 import BeautifulSoup
import re
import os
import requests
import cProfile
import threading, queue

# downloadAllMinis.py - Downloads .stl files of miniatures

# Process
# 1. Get all HTML Pages
# 2. Get end of last HTML Page
# 3. Iterate through all the pages, create list of urls to files
# 4. Obtain list of names of all files
# 6. Create master index hash table.
# 7. Look up each url, get the file, download and save as filename


def createSoup(filename):
    f = open(filename, "r") 
    soup = BeautifulSoup(f, 'html.parser')
    return soup

def getPages(soup):
    regexp = "(\/designer\/mz4250\/creations\?s=\d{0,4}#more-products)"
    pages = soup.find_all('a', href = re.compile(regexp))
    return pages

def makeHTMLDir(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

def writeToFile(html, fileName):
    f = open(fileName, "w")
    f.write(html)
    f.close()

def getHTML(site): 
    page = requests.get(site)
    return page.text

# def runOnNewThread():
    # thread_count += 1

# pages = queue.Queue()
# saved = queue.Queue()

def getHTMLParallel(currentPage, saveAs):
    # if (pages is not None and saved is not None):
        # writeToFile(getHTML(pages.get()), saved.get())
    if (currentPage is not None and saveAs is not None):
        print(f"Got HTML page: {currentPage}")
        print(f"Wrote to file: {saveAs}")
        # html = getHTML(currentPage)
        # writeToFile(html, saveAs)

def getAllHTML(end, site, directory):
    index = 1
    pageIndex = 0
    while (pageIndex < end):
        currentPage = (f'{site}?s={pageIndex}') 
        pageIndex += 48
        saveAs = (f'{directory}/mz4250-creations-page-{index}')

        print(f'currentPage : {currentPage}')
        print(f'pageIndex   : {pageIndex}')
        print(f'saveAs      : {saveAs}')

        if (not os.path.exists(saveAs)):
            # thread_count = threading.active_count()
            # if (thread_count < 5):
            if (threading.active_count() <= 5):
                # print(f"Creating new worker: worker_count: {thread_count}")
                worker = threading.Thread(target=getHTMLParallel, args=(currentPage, saveAs))
                worker.start()
            # elif (thread_count == 4 or thread_count > 4):
            else:
                for thread in threading.enumerate():
                    if (thread is threading.main_thread()): 
                        continue
                    else: 
                        thread.join()
            # else:
            # html = getHTML(currentPage)
            # writeToFile(html, saveAs)
        index += 1
    currentPage = (f'{site}?s={pageIndex}') 
    pageIndex = end 
    saveAs = (f'{directory}/mz4250-creations-page-{index}')

    getHTMLParallel(currentPage, saveAs)
    # html = getHTML(currentPage)
    # writeToFile(html, saveAs)


def getEnd(tag):
    exp = "(?<=\/designer\/mz4250\/creations\?s=)(\d{1,4})(?=#more-products)"
    regexp = re.compile(exp)
    index = regexp.search(tag[5]['href'])
    return int(index.group(0))


# path = "./html"
site = "https://www.shapeways.com/designer/mz4250/creations"

# x = threading.Thread(target=getHTMLParallel, args=(1,))
# writeToFile(getHTMLPage(site), path + "/mz4250-creations-page-1")
# getAllHTML(end)


end = getEnd(getPages(createSoup("creations.html")))
getAllHTML(end, site, "./html")

# cProfile.run('getAllHTML(end)')
