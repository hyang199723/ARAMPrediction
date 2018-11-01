#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 14:57:30 2018

@author: hongjianyang
"""

wk_dir = '/Users/hongjianyang/Desktop/LoL Project/'


import pandas as pd

#version = ['8.1.213.4336', '8.1.214.5847', '8.2.216.1199', '8.2.215.824', '8.3.217.1022', 
#           '8.4.218.8787']
#
#for i in version:
#
#    df = pd.read_csv(wk_dir + 'Summer/InitialData/' + i + '_games.csv')
#
##badmatchid = [2731721397, 2733191913, 2730883053, 2731756981, 2736585580, 2749137922, 2736653434, 2746157274, 2748279568,2747730623, 2747659609, 2747695701]
##df = df[~df['matchId'].isin(badmatchid)]
##df = df.drop('Unnamed: 0', axis = 1)
#    df = df.sort_values(by = ['matchId', 'teamId'])
#    df=pd.get_dummies(df,prefix=[''],prefix_sep='',columns=['championName'])
#    df=df.groupby(['matchId','teamId']).agg('max')
#
#
#    base=df.xs(100,level='teamId')-df.xs(200,level='teamId').astype(int)
#    base['win'] = base['win'].apply(lambda x: max(x,0))
#    base.insert(48, 'Kai\'Sa', [0] * base.shape[0])
#    base.insert(86, 'Pyke', [0] * base.shape[0])
#
#    base.to_csv(wk_dir + 'Summer/Base/' + i + '_games.csv', index = False)
#    
#    
#, '8.10.229.7328', 
#           '8.11.231.7304', '8.11.232.7066', '8.11.232.8721', '8.11.232.4186', '8.13.235.3406'
#           '8.13.235.3406', '8.13.235.9749', '8.14.238.1713'
#    
#    '8.11.231.7304', '8.11.232.7066', '8.11.232.8721', '8.11.232.4186', '8.13.235.3406'
#           '8.13.235.3406', '8.13.235.9749', '8.14.238.1713'
    
    

version = ['8.9.228.4283', '8.10.229.7328', '8.11.231.7304', '8.11.232.7066', '8.11.232.8721', '8.13.235.9749', '8.14.238.1713']
cum = pd.DataFrame()
for i in version:

    df = pd.read_csv(wk_dir + 'Summer/InitialData/' + i + '_games.csv')

#badmatchid = [2731721397, 2733191913, 2730883053, 2731756981, 2736585580, 2749137922, 2736653434, 2746157274, 2748279568,2747730623, 2747659609, 2747695701]
#df = df[~df['matchId'].isin(badmatchid)]
#df = df.drop('Unnamed: 0', axis = 1)
    df = df.sort_values(by = ['matchId', 'teamId'])
    df=pd.get_dummies(df,prefix=[''],prefix_sep='',columns=['championName'])
    df=df.groupby(['matchId','teamId']).agg('max')


    base=df.xs(100,level='teamId')-df.xs(200,level='teamId').astype(int)
    
    base['win'] = base['win'].apply(lambda x: max(x,0))
    cum = pd.concat([cum, base])
    base.to_csv(wk_dir + 'Summer/Base/' + i + '_games.csv', index = False)
    