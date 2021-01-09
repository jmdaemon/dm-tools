from bs4 import BeautifulSoup
import re
import os
import requests
import cProfile

import downloadAllMinis
# import unittest

import pytest


@pytest.fixture
def createSoup():
    f = open("creations.html", "r")
    soup = BeautifulSoup(f, 'html.parser')
    return soup

def test_getPages_ShouldReturnsSoup(createSoup):
    pages = downloadAllMinis.getPages(createSoup)
    assert(pages is not None)

def test_makeHTMLDir_ShouldCreateDir():
    path = "testpath"
    downloadAllMinis.makeHTMLDir(path)
    assert(os.path.exists(path))
    os.rmdir(path)

def test_writeToFileShouldCreateFile(): 
    testFile = "testFile.txt"
    downloadAllMinis.writeToFile("Writing to file", testFile)
    assert(os.path.exists(testFile))
    try:
        f = open(testFile, "r")
        contents = f.read()
        # print(f.read(0))
        print(contents)
        # assert(f.read() is not None or f.read() is not '')
        assert(contents is not None or f.read() is not '')
        # assert(f.read(0) == "Writing to file")
        assert(contents == "Writing to file")
    finally:
        f.close()
        os.remove(testFile)

