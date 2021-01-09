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

path = "testpath"
def getPagesShouldReturnsSoup(createSoup):
    pages = getPages(createSoup)
    assert(pages is not None)

def makeHTMLDirShouldCreateDir():
    makeHTMLDir()
    assert(os.path.exists(path))
    os.rmdir(path)

def writeToFileShouldCreateFile():
    writeToFile("Writing to file", "testFile.txt")
    # Assert file exists
    # Assert file has contents
    # Clean

