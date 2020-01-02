# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 16:33:41 2019

@author: cel-lab
"""

# Load the Pandas libraries with Alias 'pd' 
import pandas as pd 


octgn_data = pd.read_csv("OCTGN_stats_anonymized-2014-01-13.csv") 
octgn_data.insert(3, "Player_Identity", "")
octgn_data.insert(6, "Opponent_Identity", "")

for idx, game in octgn_data.iterrows():
    print(game['Win'])