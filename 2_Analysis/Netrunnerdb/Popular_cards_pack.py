import os.path as path
import json
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import string
import seaborn as sns   
import matplotlib.colors as colors
import matplotlib.cm as cm
from numpy import linspace
import matplotlib.dates as mdates
from time import sleep
import os

def format_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename

db_path = path.join(path.abspath(path.join(__file__ ,"../../..")),"db")
result_path = path.join(path.abspath(path.join(__file__ ,"../../..")),"3_Results\\Netrunnerdb\\")

open_name = "Netrunnerdb_decks.json"
with open(path.join(db_path, open_name)) as json_file:
    decks = json.load(json_file)

open_name = "Netrunnerdb_packs.json"
with open(path.join(db_path, open_name)) as json_file:
    packs = json.load(json_file)
    
open_name = "Netrunnerdb_cards.json"
with open(path.join(db_path, open_name)) as json_file:
    cards = json.load(json_file)

selected_pack = packs[0] #<<<<<<-------------------- Select
tourna = False

pack_path = result_path +  str(selected_pack['cycle_code']) + '-' + str(selected_pack['position']) + '-' + selected_pack['code'] + ('\\tournament' if tourna else '')
if not os.path.exists(pack_path):
    os.makedirs(pack_path)

card_cn = {}
for card in cards:
    card_cn.update({card['code']:card['title']})

decks_r = []
decks_c = []
for deck in decks:
    for card in cards:
        if card['code'] in [*deck['cards']]:
            if card['side_code']=='runner':
                decks_r.append(deck)
            else:
                decks_c.append(deck)
            break
                
deck_cards_r = pd.DataFrame(index=np.arange(len(decks_r)))
deck_cards_c = pd.DataFrame(index=np.arange(len(decks_c)))

for card in cards:
    if not card['type_code']=='identity' and card['pack_code']==selected_pack['code'] and not(card['title'] in deck_cards_r.columns) and not(card['title'] in deck_cards_c.columns):
        if card['side_code']=='runner':
            deck_cards_r.insert(len(deck_cards_r.columns), card['title'], 0)
        else:
            deck_cards_c.insert(len(deck_cards_c.columns), card['title'], 0)

k = 0
for deck in decks_r:
    for card in cards:
        if card['title'] in [card_cn[x] for x in [*deck['cards']]] and not card['type_code']=='identity' and card['pack_code']==selected_pack['code'] and (deck['tournament_badge'] if tourna else True):
            deck_cards_r.values[k, deck_cards_r.columns.to_list().index(card['title'])] = 1
    k += 1
 
k = 0
for deck in decks_c:
    for card in cards:
        if card['title'] in [card_cn[x] for x in [*deck['cards']]] and not card['type_code']=='identity' and card['pack_code']==selected_pack['code'] and (deck['tournament_badge'] if tourna else True):
            deck_cards_c.values[k, deck_cards_c.columns.to_list().index(card['title'])] = 1
    k += 1

new_index_r = {}
for idx, deck in enumerate(decks_r):
    temp = {idx:datetime.strptime(deck['date_creation'], '%Y-%m-%dT%H:%M:%S+00:00')}
    new_index_r.update(temp)
    
new_index_c = {}
for idx, deck in enumerate(decks_c):
    temp = {idx:datetime.strptime(deck['date_creation'], '%Y-%m-%dT%H:%M:%S+00:00')}
    new_index_c.update(temp)

deck_cards_r = deck_cards_r.rename(index=new_index_r)                      
deck_cards_c = deck_cards_c.rename(index=new_index_c)                      

stacks = np.zeros((deck_cards_r.shape[0], 0))
for card in deck_cards_r.columns:
    fig,ax1 = plt.subplots()
    fig.set_size_inches(11,8)
    temp = deck_cards_r[card].sort_index().rolling(200, min_periods=1).mean().apply(lambda x: x*100)
    stacks = np.c_[stacks, temp]
    temp.plot()
    time = temp.index.values
    ax1.set_xlabel('Pack')
    ax1.set_ylabel('usage in decks (percentage)')
    ax1.set_title(card)
    plt.ylim(0, 100)
    for card_temp in cards:
        if card_temp['title']==card:
            break
    
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    # set formatter
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    #plt.xticks(x, labels, rotation='vertical')
    plt.xticks(rotation='vertical')
    plt.draw()
    plt.show()
    fig.canvas.draw()
    labels = ax1.get_xticklabels()   
    new_label = []
    for label in labels:
        for pack in packs:
            if pack['date_release']!=None:
                if (pack['date_release'][:-3]== label.get_text()):
                    label.set_text(pack['name'])
        if label.get_text()[-3] == '-':
            label.set_text('')
        new_label.append(label.get_text())
    save_name = pack_path + '\\' + str(card_temp['code']) + '-' + str(card_temp['faction_code']) + '-' + format_filename(card) + '.pdf'
    ax1.set_xticklabels(new_label) 
    plt.savefig(path.join(result_path, save_name), bbox_inches='tight')
    plt.close(fig)

fig,ax2 = plt.subplots()
fig.set_size_inches(11,8)
plt.stackplot(time, np.divide(stacks.T, stacks.sum(1)), labels=deck_cards_r.columns)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'size': 7})
ax2.set_xlabel('Pack')
ax2.set_ylabel('Normalized usage')

ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
# set formatter
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
#plt.xticks(x, labels, rotation='vertical')
plt.xticks(rotation='vertical')
plt.draw()
plt.show()
fig.canvas.draw()
labels = ax2.get_xticklabels()   
new_label = []
for label in labels:
    for pack in packs:
        if pack['date_release']!=None:
            if (pack['date_release'][:-3]== label.get_text()):
                label.set_text(pack['name'])
    if label.get_text()[-3] == '-':
        label.set_text('')
    new_label.append(label.get_text())
ax2.set_xticklabels(new_label) 
        
save_name = pack_path + '-' + 'runner-all.pdf'
plt.savefig(path.join(result_path, save_name), bbox_inches='tight')

stacks = np.zeros((deck_cards_c.shape[0], 0))
for card in deck_cards_c.columns:
    fig,ax1 = plt.subplots()
    fig.set_size_inches(11,8)
    deck_cards_c[card].iloc[0]=0
    temp = deck_cards_c[card].sort_index().rolling(200, min_periods=1).mean().apply(lambda x: x*100)
    stacks = np.c_[stacks, temp]
    temp.plot()
    time = temp.index.values
    ax1.set_xlabel('Pack')
    ax1.set_ylabel('usage in decks (percentage)')
    ax1.set_title(card)
    plt.ylim(0, 100)
    for card_temp in cards:
        if card_temp['title']==card:
            break
    
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    # set formatter
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    #plt.xticks(x, labels, rotation='vertical')
    plt.xticks(rotation='vertical')
    plt.draw()
    plt.show()
    fig.canvas.draw()
    labels = ax1.get_xticklabels()   
    new_label = []
    for label in labels:
        for pack in packs:
            if pack['date_release']!=None:
                if (pack['date_release'][:-3]== label.get_text()):
                    label.set_text(pack['name'])
        if label.get_text()[-3] == '-':
            label.set_text('')
        new_label.append(label.get_text())
    save_name = pack_path + '\\' + str(card_temp['code']) + '-' + str(card_temp['faction_code']) + '-' + format_filename(card) + '.pdf'
    ax1.set_xticklabels(new_label) 
    plt.savefig(path.join(result_path, save_name), bbox_inches='tight')
    plt.close(fig)

fig,ax2 = plt.subplots()
fig.set_size_inches(11,8)
plt.stackplot(time, np.divide(stacks.T, stacks.sum(1)), labels=deck_cards_c.columns)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'size': 7})
ax2.set_xlabel('Pack')
ax2.set_ylabel('Normalized usage')

ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
# set formatter
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
#plt.xticks(x, labels, rotation='vertical')
plt.xticks(rotation='vertical')
plt.draw()
plt.show()
fig.canvas.draw()
labels = ax2.get_xticklabels()   
new_label = []
for label in labels:
    for pack in packs:
        if pack['date_release']!=None:
            if (pack['date_release'][:-3]== label.get_text()):
                label.set_text(pack['name'])
    if label.get_text()[-3] == '-':
        label.set_text('')
    new_label.append(label.get_text())
ax2.set_xticklabels(new_label) 

save_name = pack_path + '-' + 'corp-all.pdf'
plt.savefig(path.join(result_path, save_name), bbox_inches='tight')


