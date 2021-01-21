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
    end = extractEnd(extractProductPages(createSoup("creations.html")))
    print(end)
    offset = 0
    pagesEnd = (len([offset for offset in ([*range(offset, end, 48)] + [end])]))
    print(pagesEnd)
    base = "./html"
    directory = f"{base}/products"
    pageIndexes = [f"{directory}/pages-{index}" for index in range(1, pagesEnd)]
    print(f"============ Tag Extraction ============")
    currentIndex = 1
    while (currentIndex < pagesEnd):
        soup = createSoup(f"{base}/mz4250-creations-page-{currentIndex}")
        metadata = setupMetadata(soup)

        print(f"Iteration: {currentIndex}")
        getProductHTML(soup, metadata, pageIndexes[currentIndex], dry_run=False)
        currentIndex += 1

    print(f"")

# downloadHTMLIndices()
# downloadAllMinis()
# createMasterIndex()
downloadAllMiniMetadata()
