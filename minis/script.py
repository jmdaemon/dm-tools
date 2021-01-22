#/usr/bin/python3.9

from downloader import *

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

def downloadAllMiniMetadata():
    print(f"============ Tag Extraction ============")
    end = extractEnd(extractProductPages(createSoup("creations.html")))
    print(f"Last Page Offset: {end}")
    offset = 0
    pagesEnd = (len([offset for offset in ([*range(offset, end, 48)] + [end])]))
    print(f"Last Page Index: {pagesEnd}")

    base = "./html"
    directory = f"{base}/products"
    pageIndexes = [f"{directory}/pages-{index}" for index in ([*range(1, pagesEnd)] + [pagesEnd])]
    # pageIndexes.add(pagesEnd)
    print (pageIndexes)
    print(f"")

    currentIndex = 1
    pageIndex = 0
    stopAtPageEnd = pagesEnd - 1
    print(stopAtPageEnd)
    while (currentIndex <= pagesEnd and pageIndex < pagesEnd):
        soup = createSoup(f"{base}/mz4250-creations-page-{currentIndex}")
        metadata = setupMetadata(soup)

        print(f"Iteration: {currentIndex}")
        getProductHTML(soup, metadata, pageIndexes[pageIndex], dry_run=False)
        currentIndex += 1
        pageIndex += 1
    print("")

# downloadHTMLIndices()
# downloadAllMinis()
# createMasterIndex()
# downloadAllMiniMetadata()
