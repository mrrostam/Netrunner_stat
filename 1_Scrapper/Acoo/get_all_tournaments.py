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
#Just to test the internet connection
r = requests.get("https://www.acoo.net/anr-tournament-archive")
soup = BeautifulSoup(r.text, "html.parser")
contect = soup.find_all("a", attrs={"class": "pagi-link"})
if (r.status_code == 200): 
    print("Connection is established")
num_last_page = int(contect[-2].attrs['href'].split('/')[-2])

tournaments_per_page = 14

open_name = 'Netrunnerdb_packs.json'
with open(path.join(db_path, open_name)) as json_file:
    packs = json.load(json_file)
    
open_name = 'Netrunnerdb_cards.json'
with open(path.join(db_path, open_name)) as json_file:
    cards = json.load(json_file)

tournaments_list = []
for i in range(num_last_page):
    current_page_url = "https://www.acoo.net/anr-tournament-archive/" + str(num_last_page - i)
    r = requests.get(current_page_url)
    soup = BeautifulSoup(r.text, "html.parser")
    if (r.status_code == 200):  # 404 not found and the like. Hopefully 200!
        print("Page %i scraped successfully" % (num_last_page - i))
    tournaments = soup.find_all("tr", attrs={"class": "tournament-line"})
    if tournaments:
        for idx, tournament in enumerate(tournaments):
            table = tournament.find_all('td')
            sleep(0.1)
            r = requests.get("https://www.acoo.net/anr-tournament/" + tournament.attrs['id'])
            soup = BeautifulSoup(r.text, "html.parser")
            title = soup.find_all("div", attrs={"class": "section"})
            ranking = soup.find_all("table", attrs={"class": "tournament sortable"})
            players = ranking[-1].find_all("tr", attrs={"class": "rank-line"})
            player_list = []
            for idx, player in enumerate(players):
                detail = player.find_all("td")
                cdu = ''
                rdu = ''
                cdf = ''
                rdf = ''
                if (detail[2].a):
                    cdu = detail[2].a['href']
                if (detail[3].a):
                    rdu = detail[3].a['href']
                for card in cards:
                    if card['side_code']=='corp':
                        if card['title'].lower().find(detail[2].text.lower().split(':')[0].split(' ')[0])!=-1:
                            cdf = card['faction_code']
                        elif detail[2].text.lower().split(':')[0].find('hb')!=-1:
                            cdf = 'haas-bioroid'
                        elif detail[2].text.lower().split(':')[0].find('neh')!=-1:
                            cdf = 'nbn'
                        elif detail[2].text.lower().split(':')[0].find('twiy')!=-1:
                            cdf = 'nbn'
                    if card['side_code']=='runner':
                        if card['title'].lower().find(detail[3].text.lower().split(':')[0].split(' ')[0])!=-1:
                            rdf = card['faction_code']
                        elif detail[3].text.lower().split(':')[0].find('andy')!=-1:
                            cdf = 'criminal'
                        elif detail[3].text.lower().split(':')[0].find('kate')!=-1:
                            cdf = 'shaper'
                        elif detail[3].text.lower().split(':')[0].find('reja')!=-1:
                            cdf = 'anarch'
                player_d = { 'rank': detail[0].text[:-2],
                             'name': detail[1].text,
                             'corp_deck': detail[2].text,
                             'corp_deck_url': cdu,
                             'corp_deck_faction': cdf,
                             'runner_deck': detail[3].text,
                             'runner_deck_url': rdu,
                             'runner_deck_faction': rdf
                    }
                player_list.append(player_d)
                
            for pack in packs:
                if (title[1].text.lower().find(pack['name'].lower())!=-1):
                    tour_pack = pack['name']
            tournaments_list.append({"id": int(tournament.attrs['id']),
                                "title": table[0].text.split('\n')[2],
                                "url": "https://www.acoo.net/anr-tournament/" + tournament.attrs['id'],
                                "cardpool": tour_pack,
                                "date": table[1].text,
                                "type": tournament.img.attrs['src'].split('/')[-1][:-4],
                                "format": "standard",
                                "players_count": int(table[3].text),
                                "top_count": "0",
                                "claim_count": 1,
                                "claim_conflict": 'false',
                                "matchdata": 'false',
                                "winner_runner_identity": "",
                                "winner_corp_identity": "",
                                "players": player_list
                                })

    sleep(0.1)

save_name = 'acoo_tournaments.json'

if path.exists(path.join(db_path, save_name)):
    shutil.copy2(path.join(db_path, save_name), path.join(db_path, save_name + '_bu'))

with open(path.join(db_path, save_name), 'w') as outfile:
    json.dump(tournaments_list, outfile)
