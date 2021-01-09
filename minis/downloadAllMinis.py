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

pages = queue.Queue()
saved = queue.Queue()

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

def getHTMLParallel():
    html = getHTML(pages.get())
    writeToFile(html, saved.get())
    # currentPage = pages.get()
    # saveAs = saved.get()
    # print(f'currentPage : {currentPage}')
    # print(f'saveAs      : {saveAs}')

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

def getHTMLPage(pageIndex, index):
    currentPage = (f'{site}?s={pageIndex}') 
    saveAs = (f'{directory}/mz4250-creations-page-{index}') 
    return currentPage, saveAs

def pushBackPage(currentPage, saveAs):
    pages.put(currentPage)
    saved.put(saveAs)

def getAllHTML(end, site, directory):
    index = 1
    pageIndex = 0
    while (pageIndex < end):
        currentPage, saveAs = getHTMLPage(pageIndex, index)
        if (not os.path.exists(saveAs)):
            pushBackPage(currentPage, saveAs)
        pageIndex += 48
        index += 1

    pageIndex = end 
    currentPage, saveAs = getHTMLPage(pageIndex, index)
    pushBackPage(currentPage, saveAs)
    downloadHTML()

def getEnd(tag):
    exp = "(?<=\/designer\/mz4250\/creations\?s=)(\d{1,4})(?=#more-products)"
    regexp = re.compile(exp)
    index = regexp.search(tag[5]['href'])
    return int(index.group(0))


def getLinks(site, soup):
    exp = r"\"?(https:\/\/www\.shapeways.com\/product\/\w{9}\/)(\w*\-*)*(\?optionId=\d{1,16})(.*user-profile)\"?"
    URLS = soup.find_all('a', href = re.compile(exp))

    links = []
    for url in URLS:
        link = url['href']
        links.append(link)
    return links

def getNames(site, soup):
    exp = r"(\w+.)+\n(?=The DM Workshop)"
    regexp = re.compile(exp)
    # resultsSet = soup.find_all('a')
    # results = soup.find_all('a', text=True)
    # results = soup.find_all('a', 'product-url', text=re.compile("(\w+.)+"))
    results = soup.find_all('a', 'product-url', text=True)
    names = []
    for result in results:
        # print(result.get_text())
        names.append(result.get_text())

    print(names)
    return names


    # results = []
    # for result in resultsSet:
        # results.append(result.text)
    # print(results)
    # results = resultsSet.text
    
    # names = list(filter(regexp.match, results))
    # print(names)
    # print(results)
    # for name in names:
        # print(name.text)
    # print(type(names))
    # names = []
    # for result in resultSet:
        # names.append(result.string)

    # results = []
    # for name in names:
        # result.append(re.find
        # for name in names:
            # # results = re.findall(exp, names)
            # results = re.find(exp, name)

    # print(names)
    # print(resultSet)

    # results = re.findall(exp, names)
    # results = filter(regexp.match, resultSet)
    # print(list(results))
    # # print(results)
    # # for result in results:
        # # print(result)
    # print(results)
    # return results
    # it = re.finditer(exp, str(resultSet[0]))
    # for match in it:
        # print(match.group(0))
    # for reuslt in resultSet:
        # print(result)

    # results = regexp.findall(resultSet)

    # results = re.findall(exp, names)
    # for result in results:
        # print(result)
    # print(results)
    # for name in names:
        # print(name.content)
    # print(names.text)
    # return names


# path = "./html"
site = "https://www.shapeways.com/designer/mz4250/creations"

# writeToFile(getHTMLPage(site), path + "/mz4250-creations-page-1")
# getAllHTML(end)

# end = getEnd(getPages(createSoup("creations.html")))
# getAllHTML(end, site, "./html")

# getLinks(site, createSoup("creations.html"))
getNames(site, createSoup("creations.html"))
