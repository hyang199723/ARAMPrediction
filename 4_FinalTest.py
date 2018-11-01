#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 13:42:06 2018

@author: hongjianyang
"""

import pandas as pd
import scipy.sparse as sp
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split



wk_dir = '/Users/hongjianyang/Desktop/LoL Project/'



version = ['8.9.228.4283', '8.10.229.7328', '8.11.231.7304', '8.11.232.7066', '8.11.232.8721', '8.13.235.9749', '8.14.238.1713']
#version = ['8.9.228.4283', '8.10.229.7328', '8.11.231.7304', 
#'8.11.232.7066', '8.11.232.8721', '8.13.235.9749', '8.14.238.1713']


csrdata1 = sp.csr_matrix([0]*19881)
win1 = pd.DataFrame()
for c in version:
    row = pd.read_csv(wk_dir + 'Summer/CSR/' + c + '_row.csv')
    column = pd.read_csv(wk_dir + 'Summer/CSR/' + c + '_column.csv')
    value = pd.read_csv(wk_dir + 'Summer/CSR/' + c + '_value.csv')
    win = pd.read_csv(wk_dir + 'Summer/CSR/' + c + '_win.csv')

    row = np.transpose(row)
    column = np.transpose(column)
    value = np.transpose(value)

    row = np.array(row)[0]
    column = np.array(column)[0]
    value = np.array(value)[0]
    

    csrdata = sp.csr_matrix((value, column, row))
    csrdata1 = sp.vstack((csrdata1, csrdata), format = 'csr')
    
    win1 = pd.concat((win1, win))
    
    
    
print(1)




csrdata = sp.vstack([csrdata1[1:,:]])




#data = pd.read_csv(wk_dir + 'Summer/category.csv')
coef = pd.read_csv(wk_dir + 'Summer/coef.csv')
#
#sparse_data = sp.csr_matrix(data)
#
#full_data = sp.hstack((csrdata, sparse_data), format = 'csr')
full_data = csrdata
#
#
#
#
name = pd.read_csv(wk_dir + 'Summer/name.csv', nrows = 19881)
name.columns = ['position', 'indicator']

#
#
coef = np.transpose(coef)
#
table = name.copy()
table['coefficient'] = list(coef[0])
#
table['kept_predictors'] = [1] * 141 + [0] * 19740 
#+ [1] * 12 + [0] * 15
table['abs_coef'] = np.absolute(table.coefficient)
table['type'] = ['main'] * 141 + (['synergy'] + ['counter']) * 9870
# + ['category'] * 27
#
champ1 = []
split = table['indicator'][141:19881].str.split(',')
for i in range(141,19881):
    champ1 += [split[i][1]]

champ2 = []
for i in range(141,19881):
    champ2 += [split[i][2]]


table['champ1'] = [0] * 141 + champ1
# + [0] * 27
table['champ2'] = [0] * 141 + champ2
# + [0] * 27
table = table.sort_values(by = 'abs_coef', ascending = False)
print(2)


my_row = []
for i in [2500]:

    table['kept_predictors'][0:i] = 1

    kept = table[table['kept_predictors'] == 1]
    position = kept['position']






    indicator = full_data.tocsc()[:,position]

    data_train, data_test, win_train, win_test = train_test_split(indicator, win1, test_size = .1, random_state = 42)
    model = LogisticRegression(C = 1e-1)
    model.fit(data_train, win_train)
#    std = pd.read_csv(wk_dir + 'Summer/std.csv')
#    
#    model.coef_ = model.coef_/std

    score_test = model.score(data_test, win_test)
#    score_train = model.score(data_train, win_train)
    my_row += [(i, score_test)]
    print(i)

my_row = pd.DataFrame(my_row)
my_row.columns = ['num_of_predictors', 'test_accuracy']

my_row.plot(x = 'num_of_predictors')
 




#my_row = []
#powers = [0,1,2,3,4,8,12,19]
#for c in powers:
#
#
#    data_train, data_test, win_train, win_test = train_test_split(full_data, win1, test_size = .1, random_state = 42)
#
#
#    model = LogisticRegression(C = 10**(-c), solver = 'saga')
#    model.fit(data_train, win_train)
##    std = pd.read_csv(wk_dir + 'Summer/std.csv')
##    std = np.transpose(std)
##    model.coef_[:, 0:19881] = model.coef_[:, 0:19881] / std
#    
#    score_test = model.score(data_test, win_test)
#    score_train = model.score(data_train, win_train)
#    my_row += [(c, score_test, score_train)]
#    print(c)
#my_row = pd.DataFrame(my_row)
#my_row.columns = ['regularization_strength', 'test_accuracy', 'training_accuracy']
#
#my_row.plot(x = 'regularization_strength', title = 'with scaling, saga')








