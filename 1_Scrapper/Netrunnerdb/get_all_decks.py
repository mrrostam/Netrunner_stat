import requests
import json
import shutil
import os.path as path
from bs4 import BeautifulSoup
from time import sleep

db_path = path.join(path.abspath(path.join(__file__ ,'../../..')),'db')
netrunnerdb_decks_url = 'https://netrunnerdb.com/api/2.0/public/decklist/'

save_name = 'Netrunnerdb_decks.json'
N_final = 60000

if path.exists(path.join(db_path, save_name)):
    shutil.copy2(path.join(db_path, save_name), path.join(db_path, save_name + '_bu'))

with open(path.join(db_path, save_name), 'w+') as outfile:
    outfile.write("[\n")
    for i in range(1,N_final):
        r = requests.get(netrunnerdb_decks_url + str(i))
        sleep(0.1)
        if (r.text.find('Sorry')==-1):
            if (i!=1):
                outfile.write(",\n")
            deck = json.loads(r.content)
            print(deck['data'][0]['date_creation'] + ' id:' + str(deck['data'][0]['id']))
            json.dump(deck['data'][0], outfile)
    outfile.write("\n]")
