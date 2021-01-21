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

def downloadHTMLIndices():
    # downloader.getAllHTML(soup, "./html")
    # downloader.getAllHTML(soup, "./null", dry_run=True)
    downloader.getAllHTML(soup, "./null")

def downloadAllMinis():
    links = downloader.getLinks(site, soup)
    minis_ids = downloader.getIds(links, soup)
    downloader.getNames(site, soup)
    downloader.downloadMini(minis_ids)

def createMasterIndex():
    links = downloader.getLinks(site, soup)
    mini_ids = downloader.getIds(links, soup)
    downloader.getNames(site, soup)
    downloader.createIndex()

def downloadAllMiniMetadata():
    # metadataUtil = ExtractMetadata()
    # linksList   = ExtractMetadata.extractMiniatureLinks(site, soup)
    # namesList   = ExtractMetadata.extractMiniatureNames(site, soup)
    # idsList     = ExtractMetadata.extractMiniatureProductIds(soup)
    # linksList   = metadataUtil.extractMiniatureLinks(site, soup)
    # namesList   = metadataUtil.extractMiniatureNames(site, soup)
    # idsList     = metadataUtil.extractMiniatureProductIds(soup)
    linksList   = extractMiniatureLinks(site, soup)
    namesList   = extractMiniatureNames(site, soup)
    idsList     = extractMiniatureProductIds(soup, linksList)
    metadata = Metadata(linksList, namesList, idsList)
    # populateQueue(linksList, namesList, idsList, metadata)
    getProductHTML(soup, metadata, dry_run=False)

# downloadHTMLIndices()
# downloadAllMinis()
# createMasterIndex()
downloadAllMiniMetadata()
