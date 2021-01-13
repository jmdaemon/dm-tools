from bs4 import BeautifulSoup
import re
import os
import requests
import cProfile

# import downloader.downloadAllMinis
# import downloader.Pages
import downloader

@pytest.fixture
def createSoup():
    f = open("creations.html", "r")
    soup = BeautifulSoup(f, 'html.parser')
    return soup

def test_getPages_ShouldReturnsSoup(createSoup):
    pages = downloader.downloadAllMinis.getPages(createSoup)
    assert(pages is not None)
