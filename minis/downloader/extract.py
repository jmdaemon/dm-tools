from bs4 import BeautifulSoup
import re

def removeEmpty(name):
    if(name):
        return True
    else:
        return False 

def extractMiniatureLinks(soup):
    exp = r"\"?(https://www.shapeways.com/product/\w{9}/)(\w*-*)*(\?optionId=\d{1,16})(.*user-profile)\"?"
    URLS = soup.find_all('a', href = re.compile(exp))
    linkList = list(map(lambda url: url['href'], URLS))
    return dict.fromkeys(linkList, 1)

def extractMiniatureNames(soup):
    exp = r"\"?(https://www.shapeways.com/product/\w{9}/)(\w*-*)*(\?optionId=\d{1,16})(.*user-profile)\"?"
    results = soup.find_all('a', href = re.compile(exp))
    nameList = list(filter(removeEmpty, map(lambda name: name.get_text(strip=True), results)))
    return nameList

def extractMiniatureProductIds(soup, linkList): 
    exp = r"(\"?)(?<=https://www.shapeways.com/product/)(\w+)"
    regex = re.compile(exp)
    idsList = [regex.search(link).group(0) for link in linkList]
    return idsList

def extractMiniatureTags(soup):
    tags = soup.find_all('a', class_="product-keyword sw-dms--bg-grey-96")
    result = [tag.text for tag in tags]
    return result
