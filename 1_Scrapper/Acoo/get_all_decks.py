import requests
import scipy.io
import matplotlib.pyplot as plt
import matplotlib 
import pandas as pd
import numpy as np
import pickle
import timeit
import sqlite3
import os.path as path
from bs4 import BeautifulSoup
from time import sleep
import json
import shutil

db_path = path.join(path.abspath(path.join(__file__ ,'../../..')),'db')

open_name = 'Netrunnerdb_cards.json'
with open(path.join(db_path, open_name)) as json_file:
    cards = json.load(json_file)
    
page_final = 176
decks_list = []
base_url = 'https://www.acoo.net/deck-gallery/'

for i in range(page_final):
    r = requests.get(base_url + str(i+1))
    soup = BeautifulSoup(r.text, "html.parser")
    content_main = soup.find_all("div", attrs={"class": "deck-meta"})
    for each_deck in content_main:
        deck = {}
        print(each_deck.a['href'])
        r = requests.get('https://www.acoo.net/' + each_deck.a['href'])
        soup = BeautifulSoup(r.text, "html.parser")
        content = soup.find_all("div", attrs={"class": "tab2 deck-display-type"})
        if (content[0].text!='Identity (1)1x  ()  '):
            card_list = {}
            deck.update({'id':int(each_deck.a['href'].split('/')[2])})
            items = content[0].find_all('li')
            for item in items:
                for card in cards:
                    if item.a.text==card['title']:
                        deck.update({'side_code':card['side_code']})
                        if card['type_code']=='identity':
                            card_list.update({card['code']:1})
                        else:
                            card_list.update({card['code']:int(item.text[0])})
                deck.update({'cards':card_list})
            decks_list.append(deck)
            sleep(0.1)

save_name = 'acoo_decks.json'

if path.exists(path.join(db_path, save_name)):
    shutil.copy2(path.join(db_path, save_name), path.join(db_path, save_name + '_bu'))

with open(path.join(db_path, save_name), 'w') as outfile:
    json.dump(decks_list, outfile)