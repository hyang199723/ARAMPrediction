#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 12:13:20 2018

@author: hongjianyang
"""

import pandas as pd
import numpy as np
wk_dir = '/Users/hongjianyang/Desktop/LoL Project/'

table = pd.read_csv(wk_dir + 'table.csv')
champ_role = pd.read_csv(wk_dir + 'Data/Champion_Role_Table.csv')
champ_role = champ_role[['Champion', 'Broad_Role']]


main = table[(table.type == 'main') & (table.kept_predictors == 1)]
synergy = table[(table.type == 'synergy') & (table.kept_predictors == 1)]
counter = table[(table.type == 'counter') & (table.kept_predictors == 1)]

main = main[['indicator', 'coefficient']]
main = main.set_index('indicator')
main_dict = main.to_dict()
main_dict = main_dict.get('coefficient')


counter = counter[['champ1', 'champ2', 'coefficient']]
counter1 = counter.copy()
counter1 = counter1.sort_values(by = ['champ1', 'champ2'])
counter1 = counter1.reset_index(drop = True)
champ = 'aa'
counter_dict = {}
for i in range(0,1156):
    next_champ = counter1.loc[i,'champ1']
    if next_champ == champ:
        counter_dict[champ][counter1.loc[i,'champ2']] = counter1.loc[i,'coefficient']
    else:
        champ = next_champ
        counter_dict[champ] = {}
        counter_dict[champ][counter1.loc[i,'champ2']] = counter1.loc[i,'coefficient']


synergy = synergy[['champ1', 'champ2', 'coefficient']]
synergy1 = synergy.copy()
synergy1 = synergy1.sort_values(by = ['champ1', 'champ2'])
synergy1 = synergy1.reset_index(drop = True)
champ = 'aa'
synergy_dict = {}
for i in range(0,1221):
    next_champ = synergy1.loc[i,'champ1']
    if next_champ == champ:
        synergy_dict[champ][synergy1.loc[i,'champ2']] = synergy1.loc[i,'coefficient']
    else:
        champ = next_champ
        synergy_dict[champ] = {}
        synergy_dict[champ][synergy1.loc[i,'champ2']] = synergy1.loc[i,'coefficient']
        
        
        
        
        
        
        
red_team = ['Ashe','Vayne','Alistar','Annie','Amumu']
blue_team = ['Talon','Sejuani','Zed','Lucian','Ezreal']
blue_team.sort()
red_team.sort()

def get_main(blue, red):
    blue_row = []
    red_row = []
    for i in blue:
        blue_row += [str(i) + ': ' + str(main_dict[i])]
    for j in red:
        red_row += [str(j) + ': ' + str(main_dict[j])]
    return (blue_row, red_row)

def get_synergy(blue,red):
    blue_syn = []
    red_syn = []
    for i in range(0,4):
        for m in range(i+1, 5):
            blue_syn += [blue[i] + ' and ' + blue[m] + ': ' + str(synergy_dict[blue[i]][blue[m]])]
            red_syn += [red[i] + ' and ' + red[m] + ': ' + str(synergy_dict[red[i]][red[m]])]
        
    return (blue_syn, red_syn)

def get_counter(blue,red):
    counter_row = []
    for i in range(0,5):
        for j in range(0,5):
            if blue[i] < red[j]:
                if counter_dict[blue[i]][red[j]] > 0:
                    counter_row += [blue[i] + ' counter ' + red[j] + ': ' + str(counter_dict[blue[i]][red[j]])]
                else:
                    counter_row += [red[j] + ' counter ' + blue[i] + ': ' + str(-counter_dict[blue[i]][red[j]])]
            if blue[i] > red[j]:
                if counter_dict[red[j]][blue[i]] > 0:
                    counter_row += [red[j] + ' counter ' + blue[i] + ': ' + str(counter_dict[red[j]][blue[i]])]
                else:
                    counter_row += [blue[i] + ' counter ' + red[j] + ': ' + str(-counter_dict[red[j]][blue[i]])]
    return counter_row

import json

 
with open('main_champ.txt', 'w') as outfile:  
    json.dump(main_dict, outfile)

with open('synergy.txt', 'w') as outfile:  
    json.dump(synergy_dict, outfile)
    


new_counter = {}
for a in counter_dict:
    new_counter[a] = {}
    
new_counter['Zyra'] = {}
new_counter['Zoe'] = {}
new_counter['Zac'] = {}
new_counter['Xin Zhao'] = {}
new_counter['Yasuo'] = {}
new_counter['Zed'] = {}

for a,b in counter_dict.items():
    for k in b:
        if b[k] > 0:
            new_counter[a][k] = b[k]
        else:
            new_counter[k][a] = -b[k]

with open('counter.txt', 'w') as outfile:  
    json.dump(new_counter, outfile)
    
    
    
    
    
    
    
    
    