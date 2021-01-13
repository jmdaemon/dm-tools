from bs4 import BeautifulSoup
import re
import os
import requests
import cProfile

# import downloader.downloadAllMinis
# import downloader.downloadAllMinis
# import downloader.Pages
# import downloader.Pages
# import unittest
import downloader

import pytest

@pytest.fixture
def createSoup():
    f = open("creations.html", "r")
    soup = BeautifulSoup(f, 'html.parser')
    return soup

def test_makeHTMLDir_ShouldCreateDir():
    path = "testpath"
    downloader.downloadAllMinis.makeHTMLDir(path)
    assert(os.path.exists(path))
    os.rmdir(path)

def test_writeToFileShouldCreateFile(): 
    testFile = "testFile.txt"
    downloader.downloadAllMinis.writeToFile("Writing to file", testFile)
    assert(os.path.exists(testFile))
    try:
        f = open(testFile, "r")
        contents = f.read()
        assert(contents is not None or f.read() is not '')
        assert(contents == "Writing to file")
    finally:
        f.close()
        os.remove(testFile)

def test_getHTML_ReturnsHTML():
    site = "https://www.shapeways.com/designer/mz4250/creations"
    page = downloader.downloadAllMinis.getHTML(site)
    assert(page is not None)

def test_getEnd_ReturnsInteger(createSoup):
    pages = downloader.Pages.getPages(createSoup)
    assert(pages is not None)
    end = downloader.downloadAllMinis.getEnd(pages)
    assert(end is not None)
