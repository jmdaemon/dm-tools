from bs4 import BeautifulSoup
import re

# class ExtractMetadata:
    # def __init__(self):
        # self.Metadata 

def removeEmpty(name):
    if(name):
        return True
    else:
        return False 

def extractMiniatureLinks(site, soup):
    exp = r"\"?(https://www.shapeways.com/product/\w{9}/)(\w*-*)*(\?optionId=\d{1,16})(.*user-profile)\"?"
    URLS = soup.find_all('a', href = re.compile(exp))
    linkList = list(map(lambda url: url['href'], URLS))
    return linkList

def extractMiniatureNames(site, soup):
    exp = r"\"?(https://www.shapeways.com/product/\w{9}/)(\w*-*)*(\?optionId=\d{1,16})(.*user-profile)\"?"
    results = soup.find_all('a', href = re.compile(exp))
    # nameList = list(filter(ExtractMetadata.removeEmpty, map(lambda name: name.get_text(strip=True), results)))
    nameList = list(filter(removeEmpty, map(lambda name: name.get_text(strip=True), results)))
    return nameList

def extractMiniatureProductIds(soup, linkList): 
    exp = r"(\"?)(?<=https://www.shapeways.com/product/)(\w+)"
    regex = re.compile(exp)
    # idsList = [regex.search(link).group(0) for link in links.queue]
    # idsList = [regex.search(link).group(0) for link in self.Metadata.getLinks()]
    # idsList = [regex.search(link).group(0) for link in metadata.getLinks()]
    idsList = [regex.search(link).group(0) for link in linkList]
    return idsList
