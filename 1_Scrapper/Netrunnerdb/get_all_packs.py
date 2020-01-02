import requests
import json
import shutil
import os.path as path
from bs4 import BeautifulSoup

db_path = path.join(path.abspath(path.join(__file__ ,'../../..')),'db')
netrunnerdb_packs_url = 'https://netrunnerdb.com/api/2.0/public/packs'

r = requests.get(netrunnerdb_packs_url)
cards = json.loads(r.content)

save_name = 'Netrunnerdb_packs.json'

if path.exists(path.join(db_path, save_name)):
    shutil.copy2(path.join(db_path, save_name), path.join(db_path, save_name + '_bu'))

with open(path.join(db_path, save_name), 'w') as outfile:
    json.dump(cards['data'], outfile)