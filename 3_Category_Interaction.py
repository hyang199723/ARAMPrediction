#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 14:18:22 2018

@author: hongjianyang
"""
wk_dir = '/Users/hongjianyang/Desktop/LoL Project/'



import pandas as pd
import numpy as np
import scipy.sparse as sp
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
version = ['8.9.228.4283', '8.10.229.7328', '8.11.231.7304', '8.11.232.7066', '8.11.232.8721', '8.13.235.9749', '8.14.238.1713']


#'8.1.213.4336', '8.1.214.5847', '8.2.216.1199', '8.2.215.824', '8.3.217.1022', 
#           '8.4.218.8787', '8.5.220.3006', '8.6.222.2149', '8.7.223.9264', '8.7.224.5563', 
#           '8.8.225.6906', '8.8.226.7254', '8.9.227.7511', '8.9.228.4283',  '8.10.229.7328', 
#           '8.11.231.7304', 




val_var = 'Broad_Role'

df1 = pd.read_csv(wk_dir + 'Data/Champion_Role_Table.csv', index_col = 'Champion')
role = ['Artillery', 'Controller', 'Fighter', 'Mage', 'Marksmen', 'Slayer', 'Tank', 'Unique']


my_dict = df1[val_var].to_dict()
base_array1 = np.array([[0]*12])
interaction1 = np.array([[0]*15])
win1 = pd.DataFrame()
dataset1 = sp.csr_matrix([0]*19881)
for c in version:
    df = pd.read_csv(wk_dir + 'Summer/InitialData/' + c + '_games.csv')
    df['championName'] = df['championName'].map(my_dict)
    df_dummies = pd.get_dummies(df)

    df_dummies.columns = ['matchId', 'teamId', 'win'] + role
    df_dummies = df_dummies.groupby(['matchId', 'teamId']).agg({'Artillery': 'sum','Fighter': 'sum','Mage': 'sum','Marksmen': 'sum','Slayer': 'sum','Tank': 'sum','win': 'max'})

    difference = df_dummies.xs(100, level = 'teamId') - df_dummies.xs(200, level = 'teamId').astype(int)
    num_games = difference.shape[0]
    win = difference['win'].replace(to_replace = -1, value = 0)
    difference = difference.drop('win', axis = 1)

    square_diff = (df_dummies.xs(100, level = 'teamId')**2 - df_dummies.xs(200, level = 'teamId')**2).astype(int)
    square_diff = square_diff.drop('win', axis = 1)
    square_diff.columns = ['Square_' + str(col) for col in square_diff.columns]

    base_role = pd.concat([difference, square_diff], axis = 1)

    base_array = base_role.values
    base_array[base_array > 150] = base_array[base_array > 150] - 256
    win_array = win.values

    diff_array = difference.values
    interaction = np.empty([num_games,15], dtype = int)
    col_num = 0
    for i in range(0,6):
        list1 = diff_array[:,i]
        m = i + 1
        for j in range(m, 6):
            list2 = diff_array[:,j]
            interaction[:,col_num] = list1 * list2
            col_num = col_num + 1
    
    base_array1 = np.concatenate((base_array1, base_array))
    interaction1 = np.concatenate((interaction1, interaction))
    	
    
    

        
        
        
    value = pd.read_csv(wk_dir + 'Summer/CSR/' + c + '_value.csv')
    row = pd.read_csv(wk_dir + 'Summer/CSR/' + c + '_row.csv')
    column = pd.read_csv(wk_dir + 'Summer/CSR/' + c + '_column.csv')
    win = pd.read_csv(wk_dir + 'Summer/CSR/' + c + '_win.csv')
    
    win1 = pd.concat([win1, win])
    row = row.transpose()
    column = column.transpose()
    value = value.transpose()

    row = np.array(row)[0]
    column = np.array(column)[0]
    value = np.array(value)[0]

    dataset = sp.csr_matrix((value, column, row), shape=(num_games, 19881))
    
    dataset1 = sp.vstack([dataset1, dataset], format = 'csr')
    
    

#data = sp.hstack((dataset1,base_array1, interaction1), format = 'csr')
data = dataset1



#data1 = np.concatenate((base_array1, interaction1), axis = 1)
#data1 = data1[1:, :]
#data1 = pd.DataFrame(data1)
#data1.to_csv(wk_dir + 'Summer/category.csv', index = False)


    	

#data = diff_array

data = sp.vstack([data[1:, :]])
data_train, data_test, win_train, win_test = train_test_split(data, win1, test_size = .1, random_state = 42)



model = LogisticRegression(C = 1e-3)
model.fit(data_train, win_train)
score = model.score(data_test, win_test)

coef = model.coef_

coef = pd.DataFrame(coef)
coef.to_csv(wk_dir + 'Summer/coef.csv', index = False)






        
        
        
        
        
        
        
        
        
        
    
        
        

#df1 = df1.reset_index()
#champion = df1['Champion']
#
#champ_interaction = []
#
#
#for i in range(0,141):
#    champ1 = champion[i]
#    for j in range(i+1, 141):
#        champ2 = champion[j]
#        champ_interaction += ['Synergy,' + champ1 + ','+ champ2]
#        champ_interaction += ['Counter,' + champ1 + ','+ champ2]
#
#champion = list(champion)
#name = champion + champ_interaction
#
#role = ['Controller', 'Fighter', 'Mage', 'Marksmen', 'Slayer', 'Tank']
#square_role = ['Square_' + x for x in role]
#cate_interaction = []
#for a in range(0,6):
#    cate1 = role[a]
#    for b in range(a+1,6):
#        cate2 = role[b]
#        cate_interaction += [cate1 + ',' + cate2]
#
#name += role + square_role + cate_interaction
#name = pd.DataFrame(name)
#name.to_csv(wk_dir + 'Summer/name.csv')

    

