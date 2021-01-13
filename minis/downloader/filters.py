from bs4 import BeautifulSoup
import re
import queue

def getEnd(tag):
    exp = "(?<=\/designer\/mz4250\/creations\?s=)(\d{1,4})(?=#more-products)"
    regexp = re.compile(exp)
    index = regexp.search(tag[5]['href'])
    return int(index.group(0))

def getLinks(site, soup, links):
    exp = r"\"?(https:\/\/www\.shapeways.com\/product\/\w{9}\/)(\w*\-*)*(\?optionId=\d{1,16})(.*user-profile)\"?"
    URLS = soup.find_all('a', href = re.compile(exp))

    links = set()
    for url in URLS:
        link = url['href']
        links.add(link)
        minis_links.put(link)
    return links

def getNames(site, soup):
    results = soup.find_all('a', 'product-url', text=True)
    for result in results:
        names.put(result.get_text())

def getIds(links, soup): 
    exp = r"(\"?)(?<=https:\/\/www\.shapeways\.com\/product\/)(\w+)"
    regex = re.compile(exp)

    for link in links:
        match = regex.search(link)
        ids.put(match.group(0))

