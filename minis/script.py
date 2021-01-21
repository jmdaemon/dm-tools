#/usr/bin/python3.9

from downloader import *

soup = createSoup("creations.html")

def setupMetadata():
    linksList   = extractMiniatureLinks(soup)
    namesList   = extractMiniatureNames(soup)
    idsList     = extractMiniatureProductIds(soup, linksList)
    metadata    = Metadata(linksList, namesList, idsList)
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
    metadata: Metadata = setupMetadata
    getProductHTML(soup, metadata, dry_run=False)

# downloadHTMLIndices()
# downloadAllMinis()
# createMasterIndex()
downloadAllMiniMetadata()
