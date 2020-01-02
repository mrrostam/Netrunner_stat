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
import datetime

db_path = path.join(path.abspath(path.join(__file__ ,'../../..')),'db')
#Just to test the internet connection
r = requests.get("https://stimhack.com/tournament-decklists/")
soup = BeautifulSoup(r.text, "html.parser")
content = soup.find_all("a", attrs={"class": "pagi-link"})
if (r.status_code == 200): 
    print("Connection is established")

open_name = 'Netrunnerdb_cards.json'
with open(path.join(db_path, open_name)) as json_file:
    cards = json.load(json_file)
    
tournaments_list = []
tournaments = soup.find_all("td", attrs={"class": "column-2"})

k = 1
for idx, tournament in reversed(list(enumerate(tournaments))):
    if tournament.text != 'NONE RECORDED' and len(tournament.text) > 1:
        wrd = {}
        wcd = {}
        r = requests.get(tournament.a.attrs['href'])
        soup = BeautifulSoup(r.text, "html.parser")
        date = soup.find_all("span", attrs={"class": "onDate date updated"})
        deck_text = soup.find_all("div", attrs={"class": "entry-content"})
        for card in cards:
            if deck_text[0].text.replace('”','"').replace('“','"').lower().find(card['title'].lower())!=-1:
                if card['side_code']=='corp':
                    wcd.update({card['code']:1})
                else:
                    wrd.update({card['code']:1})    
        tournaments_list.append({"id": k,
                    "title": tournament.text,
                    "url": tournament.a.attrs['href'],
                    "cardpool": "",
                    "date": datetime.datetime.strptime(date[0].a.text, '%B %d, %Y').strftime("%Y-%m-%d"),
                    "type": "",
                    "format": "standard",
                    "players_count": "",
                    "top_count": "0",
                    "claim_count": 1,
                    "claim_conflict": 'false',
                    "matchdata": 'false',
                    "winner_runner_deck": wrd,
                    "winner_corp_deck": wcd
                    })

        k += 1
        print(k)

save_name = 'stimhack_tournaments.json'

if path.exists(path.join(db_path, save_name)):
    shutil.copy2(path.join(db_path, save_name), path.join(db_path, save_name + '_bu'))

with open(path.join(db_path, save_name), 'w') as outfile:
    json.dump(tournaments_list, outfile)