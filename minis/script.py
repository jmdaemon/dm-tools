#/usr/bin/python3.9

from downloader import *
# from downloader import ExtractMetadata

# 1. Setup Class
# Set 
# .soup = createSoup(fileName)
# .site = "" (constant)
# .path = "./html"

# 2. Get All HTML Files
# getAllHTML()

# 3. Create the download links, and download all of the miniatures
# Set links, ids, names queues
# downloadMini()

soup = downloader.createSoup("creations.html")
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
    downloader.getAllHTML(soup, "./null")

def downloadAllMinis():
    downloadMiniature(setupMetadata())

def createMasterIndex():

    downloader.createIndex()

def downloadAllMiniMetadata():
    getProductHTML(soup, setupMetadata, dry_run=False)

# downloadHTMLIndices()
downloadAllMinis()
# createMasterIndex()
# downloadAllMiniMetadata()
