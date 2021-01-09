from bs4 import BeautifulSoup
import re
import os
import requests
import cProfile

# downloadAllMinis.py - Downloads .stl files of miniatures

# Process
# 1. Get all HTML Pages
# 2. Get end of last HTML Page
# 3. Iterate through all the pages, create list of urls to files
# 4. Obtain list of names of all files
# 6. Create master index hash table.
# 7. Look up each url, get the file, download and save as filename

# f = open("creations", "r");
# soup = BeautifulSoup(f, 'html.parser')

# path = "./html"

site = "https://www.shapeways.com/designer/mz4250/creations"

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

def getAllHTML(end, site):
    index = 1
    pageIndex = 48
    while (pageIndex < end):
        currentPage = (f'{site}?s={pageIndex}')
        pageIndex += 48
        saveAs = (f'{site}/mz4250-creations-page-{index}')

        print(f'currentPage: {currentPage}')
        print(f'pageIndex: {pageIndex}')
        print(f'saveAs: {saveAs}')

        if (not os.path.exists(saveAs)):
            html = getHTML(currentPage)
            writeToFile(html, saveAs)
        index += 1


def getEnd(tag):
    exp = "(?<=\/designer\/mz4250\/creations\?s=)(\d{1,4})(?=#more-products)"
    regexp = re.compile(exp)
    index = regexp.search(tag[5]['href'])
    return int(index.group(0))

# writeToFile(getHTMLPage(site), path + "/mz4250-creations-page-1")
# end = getEnd(getPages(soup))
# getAllHTML(end)

# cProfile.run('getAllHTML(end)')
