#/usr/bin/python3.9

from downloader import *

soup = createSoup("creations.html")
site = "https://www.shapeways.com/designer/mz4250/creations"

def setupMetadata():
    linksList   = extractMiniatureLinks(site, soup)
    namesList   = extractMiniatureNames(site, soup)
    idsList     = extractMiniatureProductIds(soup, linksList)
    metadata = Metadata(linksList, namesList, idsList)
    return metadata

def downloadHTMLIndices():
    # downloader.getAllHTML(soup, "./html")
    # downloader.getAllHTML(soup, "./null", dry_run=True)
    getAllHTML(soup, directory = "./null")

def downloadAllMinis():
    downloadMiniature(setupMetadata())

def createMasterIndex():
    downloader.createIndex()

def downloadAllMiniMetadata():
    getProductHTML(soup, setupMetadata, dry_run=False)

downloadHTMLIndices()
# downloadAllMinis()
# createMasterIndex()
# downloadAllMiniMetadata()
