# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 17:30:56 2019

@author: cel-lab
"""
import csv
import pandas as pd
import os.path as path
import numpy as np


db_path = path.join(path.abspath(path.join(__file__ ,"../..")),"db")
csv_file = "OCTGN_stats_anonymized-2014-01-13.csv"

games_list = pd.read_csv(path.join(db_path, csv_file))
games_list.insert(3, "Corp_ID","")
games_list.insert(6, "Runner_ID","")

for index, game in games_list.iterrows():
    game["Corp_ID"]=game['Player_Faction'].split('|')[0]
    game["Runner_ID"]=game['Opponent_Faction'].split('|')[0]