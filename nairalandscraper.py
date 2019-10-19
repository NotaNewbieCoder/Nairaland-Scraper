#!/usr/bin/env python
# coding: utf-8

# In[4]:



import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import urllib

WordList = []

def put_in_file():
    global WordList
    file_name = searchTerm + '.txt'
    for word in WordList:
        with open(file_name, "a+", encoding="utf-8") as f:
            f.write(word)


def word_count(string):
    counts = dict()
    words = string.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return len(counts)


def search_item(search_term, next=False, page=0,  board=0):
    if next == False:
        page = requests.get("https://www.nairaland.com/search?q=" + urllib.parse.quote_plus(str(search_term)) + "&board="+str(board))
    else:
        page = requests.get("https://www.nairaland.com/search/"
                            + str(search_term) + "/0/"+str(board)+"/0/1" + str(page))
    soup = BeautifulSoup(page.content, 'html.parser')

    comments = soup.findAll("div", {"class": "narrow"})

    return comments


def add_to_word_list(strings):
    global WordList
    k = 0
    while k < len(strings):
        if word_count(strings[k].text) > 1:
            WordList.append(strings[k].text)
        k += 1


searchTerm = input("Enter search term: ")
board = int(input("Enter Section: "))

j = 0

while j < 20:
    if j == 0:
        nextItem = False
    else:
        nextItem = True
    commentsCurrent = search_item(searchTerm, nextItem, j,  board)
    add_to_word_list(commentsCurrent)
    j += 1

put_in_file()

