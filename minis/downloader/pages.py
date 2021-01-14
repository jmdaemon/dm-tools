from bs4 import BeautifulSoup
import re
import queue

def getPages(soup):
    regexp = "(\/designer\/mz4250\/creations\?s=\d{0,4}#more-products)"
    pages = soup.find_all('a', href = re.compile(regexp))
    return pages

def getHTMLPage(site, pageIndex, index, directory):
    currentPage = (f'{site}?s={pageIndex}') 
    saveAs = (f'{directory}/mz4250-creations-page-{index}') 
    return currentPage, saveAs

def pushBackPage(currentPage, saveAs, pages, saved):
    pages.put(currentPage)
    saved.put(saveAs)
