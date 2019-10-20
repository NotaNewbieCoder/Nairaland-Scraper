#!/usr/bin/env python
# coding: utf-8
"""importing libraries"""
import urllib
import requests
from bs4 import BeautifulSoup

WORDLIST = []


def put_in_file():
    """save searched comments as txt file"""
    file_name = SEARCHTERM + '.txt'
    for word in WORDLIST:
        with open(file_name, "a+", encoding="utf-8") as f:
            f.write(word)


def word_count(string):
    """count number of words in sentence and return count"""
    counts = dict()
    words = string.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return len(counts)


def search_item(search_term, next=False, page=0, board=0):
    """search for inputted text on nairaland"""
    if next == False:
        page = requests.get("https://www.nairaland.com/search?q="
                            + urllib.parse.quote_plus(str(search_term))
                            + "&board="+str(board))
    else:
        page = requests.get("https://www.nairaland.com/search/"
                            + str(search_term) + "/0/"+str(board)
                            +"/0/1" + str(page))
    soup = BeautifulSoup(page.content, 'html.parser')
    comments = soup.findAll("div", {"class": "narrow"})
    return comments


def add_to_word_list(strings):
    """adding each comment to Word list"""
    k = 0
    while k < len(strings):
        if word_count(strings[k].text) > 1:
            WORDLIST.append(strings[k].text)
        k += 1


SEARCHTERM = input("Enter search term: ")
BOARD = int(input("Enter Section: "))

J = 0

while J < 20:
    if J == 0:
        NEXTITEM = False
    else:
        NEXTITEM = True
    COMMENTSCURRENT = search_item(SEARCHTERM, NEXTITEM, J, BOARD)
    add_to_word_list(COMMENTSCURRENT)
    J += 1

put_in_file()
