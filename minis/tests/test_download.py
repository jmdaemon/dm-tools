from bs4 import BeautifulSoup
import re
import os
import requests
import cProfile

# import unittest
import downloader

import pytest

@pytest.fixture
def createSoup():
    f = open("creations.html", "r")
    soup = BeautifulSoup(f, 'html.parser')
    f.close()
    return soup

def test_createDir_CreatesHTML():
    path = "testpath"
    downloader.createDir(path)
    assert(os.path.exists(path))
    os.rmdir(path)

def test_writeToFile_OutputsFile(): 
    testFile = "testFile.txt"
    downloader.writeToFile("Writing to file", testFile)
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
    page = downloader.Downloader.getHTML(site)
    assert(page is not None)

def test_getEnd_ReturnsInteger(createSoup):
    pages = downloader.getPages(createSoup)
    assert(pages is not None)
    end = downloader.getEnd(pages)
    assert(end is not None)
