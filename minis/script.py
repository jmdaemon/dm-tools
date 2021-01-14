#/usr/bin/python3.9

import downloader

def downloadHTMLIndices():
    soup = downloader.createSoup("creations.html")
    downloader.getAllHTML(soup, "./null")

# def downloadAllMinis():
# def createMasterIndex():
