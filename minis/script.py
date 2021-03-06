#/usr/bin/python3.9

from downloader import *
import os

def setupMetadata(soup):
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

def getEnd(offset = 0): 
    end = extractEnd(extractProductPages(createSoup("creations.html")))
    pagesEnd = (len([offset for offset in ([*range(offset, end, 48)] + [end])]))
    print(f"Last Page Offset: {end}")
    print(f"Last Page Index: {pagesEnd}")
    return end, pagesEnd

def indicesToRange(pagesEnd): 
    return ([*range(1, pagesEnd)] + [pagesEnd])

def run(directory, title, keyword, target, currentIndex = 1, pageIndex = 0):
    end, pagesEnd = getEnd()
    pages = [f"{directory}/pages-{index}" for index in indicesToRange(pagesEnd)]
    while (currentIndex <= pagesEnd and pageIndex < pagesEnd):
        print("Page Index       : {currentIndex}")
        currentPageDir = pages[pageIndex]
        print(f"Page Directory  : {currentPageDir}")
        print(os.listdir(f"{currentPageDir}")) 
        pages = os.listdir(f"{currentPageDir}")
        print(f"")

        print(f"============ {title} ============")
        for page in pages:
            print(f"Miniature Page: {page}")
            soup = createSoup(f"{currentPageDir}/{page}")
            tags = target(soup)
            for tag in tags:
                print(f"{keyword}: {tag}") 
            print(f"")
        print(f"")
        currentIndex += 1
        pageIndex += 1

def downloadAllMiniMetadata(base = "./html"):
    print(f"============ Tag Extraction ============")
    end, pagesEnd = getEnd()
    directory = f"{base}/products"
    pageIndexes = [f"{directory}/pages-{index}" for index in indicesToRange]
    print(pageIndexes)
    print(f"")
    
    currentIndex = 1
    pageIndex = 0
    while (currentIndex <= pagesEnd and pageIndex < pagesEnd):
        soup = createSoup(f"{base}/mz4250-creations-page-{currentIndex}")
        metadata = setupMetadata(soup)

        print(f"Iteration: {currentIndex}")
        getProductHTML(soup, metadata, pageIndexes[pageIndex], dry_run=False)
        currentIndex += 1
        pageIndex += 1
    print("")

def downloadAllMiniatureTags(directory = "./html/products"):
    run(directory, "Tags", "Tag", extractMiniatureTags)

def downloadAllMiniatureImgs(directory = "./html/products"):
    run(directory, "Imgs", "Img", extractMiniatureImgs)

# downloadHTMLIndices()
# downloadAllMinis()
# createMasterIndex()
# downloadAllMiniMetadata()
# downloadAllMiniatureTags()
downloadAllMiniatureImgs()
