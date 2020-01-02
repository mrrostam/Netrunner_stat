import requests
import json
import shutil
import os.path as path
from bs4 import BeautifulSoup

db_path = path.join(path.abspath(path.join(__file__ ,'../../..')),'db')
netrunnerdb_t_url = 'https://alwaysberunning.net/api/tournaments?start=2012.01.01&desc=1&concluded=1'

r = requests.get(netrunnerdb_t_url)
cards = json.loads(r.content)

save_name = 'ABR_tournaments.json'

if path.exists(path.join(db_path, save_name)):
    shutil.copy2(path.join(db_path, save_name), path.join(db_path, save_name + '_bu'))

with open(path.join(db_path, save_name), 'w') as outfile:
    json.dump(cards, outfile)