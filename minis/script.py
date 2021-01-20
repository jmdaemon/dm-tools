#/usr/bin/python3.9

import downloader

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
    # links = downloader.getLinks(site, soup)
    downloader.getLinks(site, soup)
    # minis_ids = downloader.getIds(links, soup)
    minis_ids = downloader.getIds(soup)
    mini_names = downloader.getNames(site, soup)
    # downloader.getProductHTML(soup, links, mini_names,dry_run=False)
    # downloader.getProductHTML(soup, links, dry_run=False)
    downloader.getProductHTML(soup, dry_run=False)

# downloadHTMLIndices()
# downloadAllMinis()
# createMasterIndex()
downloadAllMiniMetadata()
