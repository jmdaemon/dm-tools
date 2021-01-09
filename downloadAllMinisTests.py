from bs4 import BeautifulSoup
import re
import os
import requests
import cProfile

import downloadAllMinis
# import unittest
import pytest

path = "testpath"
def getPagesShouldReturnsSoup():
    # Check Soup not null
    print("")

def makeHTMLDirShouldCreateDir():
    makeHTMLDir()
    assert(os.path.exists(path))
    os.rmdir(path)

def writeToFileShouldCreateFile():
    writeToFile("Writing to file", "testFile.txt")
    # Assert file exists
    # Assert file has contents
    # Clean

