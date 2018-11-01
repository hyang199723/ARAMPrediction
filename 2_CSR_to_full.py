#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 14:47:58 2018

@author: hongjianyang
"""

wk_dir = '/Users/hongjianyang/Desktop/LoL Project/'

import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.linear_model import LogisticRegression

row = pd.read_csv(wk_dir + 'Summer/CSR/large_row.csv')
column = pd.read_csv(wk_dir + 'Summer/CSR/large_column.csv')
value = pd.read_csv(wk_dir + 'Summer/CSR/large_value.csv')
#row = row.drop('Unnamed: 0', axis = 1)
#column = column.drop('Unnamed: 0', axis = 1)
#value = value.drop('Unnamed: 0', axis = 1)

row = row.transpose()
column = column.transpose()
value = value.transpose()

row = np.array(row)[0]
column = np.array(column)[0]
value = np.array(value)[0]

dataset = csr_matrix((value, column, row), shape=(61047, 19601)).toarray()
dataset1 = pd.DataFrame(dataset)
champion = pd.read_csv('/Users/hongjianyang/Desktop/LoL Project/Data/Champion_Role_Table.csv')
champion = champion['Champion']

my_rows = []
dataset1 = np.absolute(dataset1) 
aggregate = dataset1.agg(['sum'])
aggregate = aggregate.drop('Unnamed: 0', axis = 1)
for i in [5 * a for a in range(24, 40)]:
    
    aggregate = aggregate[aggregate[aggregate.columns] >= i]
    aggregate = aggregate.dropna(axis = 1)
    number_of_inter = aggregate.shape[1]
    
    columns = aggregate.columns
    columns = champion + columns
    dataset = dataset[columns]
    dataset = dataset.drop('Aatrox', axis = 1)
    dataset['Intercept'] = 1
#separate the dataset into two parts: 1 stands for sample, 0 stands for test. Ratio: 9 : 1

    np.random.seed(0)
    dataset['Test'] = np.random.choice([0, 1], size=61047, p=[.1, .9])

    test = dataset[dataset['Test'] == 0]
    dataset = dataset[dataset['Test'] == 1]
    
    
    dataset = dataset.drop('Test', axis = 1)
    test = test.drop('Test', axis = 1)
#Edit the format of 'test' for prediction
#test = test.drop('Unnamed: 0', axis = 1)

#Prepare x and y for regression
    y = dataset.Y.copy()
    x = dataset.copy()
#x = x.drop('Unnamed: 0', axis = 1)
    x = x.drop('Y', axis = 1)
    
    
    
    actual = np.array(test['Y'])
    test = test.drop('Y', axis = 1)
    
    for c in [1, 1e1, 1e2, 1e3, 1e4]:
        model = LogisticRegression(C=c)
        model.fit(x, y)
        print(model)

        print (model.intercept_, model.coef_)


        result = model.coef_
        
        score = model.score(test, actual)
        my_rows.append((number_of_inter, c, score))
        
my_rows = pd.DataFrame.from_records(my_rows)
my_rows.to_csv(path_or_buf=wk_dir + "Larger_PredictorsVSAccuracy.csv", index = True)
    
    
    
