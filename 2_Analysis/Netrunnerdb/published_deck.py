import os.path as path
import json
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd


db_path = path.join(path.abspath(path.join(__file__ ,"../../..")),"db")
result_path = path.join(path.abspath(path.join(__file__ ,"../../..")),"3_Results\\Netrunnerdb")
        
#Published decks on Netrunnerdb
open_name = "Netrunnerdb_decks.json"
with open(path.join(db_path, open_name)) as json_file:
    decks = json.load(json_file)

open_name = "Netrunnerdb_packs.json"
with open(path.join(db_path, open_name)) as json_file:
    packs = json.load(json_file)

open_name = "Netrunnerdb_cards.json"
with open(path.join(db_path, open_name)) as json_file:
    cards = json.load(json_file)
    
deck_date = pd.DataFrame()
deck_year_str = []

for deck in decks:
    for card in cards:
        for card2 in [*deck['cards']]:
            if card['code']==card2 and card['type_code']=='identity':
                deck_date = deck_date.append(pd.DataFrame({'datetime': datetime.strptime(deck['date_creation'], '%Y-%m-%dT%H:%M:%S+00:00'), 'anarch': int(card['faction_code']=='anarch'), 'criminal': int(card['faction_code']=='criminal'), 'shaper': int(card['faction_code']=='shaper'), 'haas-bioroid': int(card['faction_code']=='haas-bioroid') , 'jinteki': int(card['faction_code']=='jinteki'), 'nbn': int(card['faction_code']=='nbn'), 'weyland-consortium': int(card['faction_code']=='weyland-consortium')}, index=[0]), ignore_index=True)
                # if deck_date.iloc[-1,1:].sum()==0:
                #     print(deck['id'])
                break

plt.rc('xtick', labelsize=4)    # fontsize of the tick labels
plt.rc('ytick', labelsize=6)    # fontsize of the tick labels
ax = deck_date.groupby([deck_date['datetime'].dt.year, deck_date['datetime'].dt.month]).sum().plot(kind='bar', legend=False, color=['orangered','blue', 'limegreen', 'blueviolet', 'darkred', 'gold', 'slategrey'])
ax.set_xlabel('Packs')
ax.set_ylabel('# of decks published on Netrunnerdb')
labels = ax.get_xticklabels()
plt.legend(['Anarch', 'Criminal', 'Shaper', 'Haas-Bioroid', 'Jinteki', 'NBN', 'Weyland Consortium'],prop={'size': 6});

new_label = []
for label in labels:
    for pack in packs:
        if pack['date_release']!=None:
            if ('('+str(datetime.strptime(pack['date_release'], '%Y-%m-%d').year)+', '+str(datetime.strptime(pack['date_release'], '%Y-%m-%d').month)+')' == label.get_text()):
                label.set_text(pack['name'])
    new_label.append(label.get_text())

ax.set_xticklabels(new_label) 
fig = plt.gcf()
fig.set_size_inches(8, 2)   

   
save_name = 'publisheddecks.pdf'
plt.savefig(path.join(result_path, save_name), bbox_inches='tight')

#ax = sns.barplot(x="index", y="datetime", data=test)
# #Popular cards
# open_name = "Netrunnerdb_cards.json"
# with open(path.join(db_path, open_name)) as json_file:
#     cards = json.load(json_file)
    
# deck_cards = pd.DataFrame(index=np.arange(len(decks)+1))
# k = 0
# for card in cards:
#     deck_cards.insert(k, card['code'], 0)
#     k += 1

# k = 0
# for idx,deck in enumerate(decks):
#     #deck_cards.loc[k] = [0]*len(cards)
#     for card in [*deck['cards']]:
#         deck_cards.loc[k][card] = 1
#     k += 1
#     print(idx)
    
# save_name = 'Netrunnerdb_decks_cards.csv'
# deck_cards.to_csv(path.join(db_path, save_name))