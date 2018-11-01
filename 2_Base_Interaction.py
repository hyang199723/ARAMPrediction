#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 12:07:38 2018

@author: hongjianyang
"""

wk_dir = '/Users/hongjianyang/Desktop/LoL Project/'

import pandas as pd
import numpy as np

#'8.1.213.4336', '8.1.214.5847', '8.2.216.1199', '8.2.215.824''8.3.217.1022', 
#           '8.4.218.8787', '8.5.220.3006', '8.6.222.2149', '8.7.223.9264', '8.7.224.5563', 
#           '8.8.225.6906', '8.8.226.7254', '8.9.227.7511', '8.9.228.4283', '8.10.229.7328', 
#           '8.11.231.7304', '8.11.232.7066', '8.11.232.8721', '8.11.232.4186', '8.13.235.9749', '8.14.238.1713'

version = ['8.13.235.9749']
def interact(a,b):
    a
    ab = a*b
    return np.column_stack((np.equal(1,ab)*a,np.equal(-1,ab)*a)) # synergy, counter

n_champ = 141
width = n_champ + n_champ*(n_champ-1)

for c in version:
    df = pd.read_csv(wk_dir + 'Summer/Base/' + c + '_games.csv',)
    base = df.iloc[:,1:].values




    values = np.empty( [len(base), width], dtype =int)
    values[:,0:n_champ] = base
    n_col = n_champ
    for i in range(0,n_champ):
        array1 = base[:,i]
        for j in range(i+1,n_champ):
            array2 = base[:,j]
            values[:,n_col:n_col+2] = interact(array1, array2)
            n_col = n_col + 2

#    std = np.std(values, axis = 0)
#    
#    values = values/std
#    
#    
#    values[values == inf] = 0
#    values[values == nan] = 0
    
    
    
    row = [0] + [55*i for i in range(1,base.shape[0]+1)]
    column = values.nonzero()[1]
    value = values[values.nonzero()]

    row = pd.DataFrame(row)
    column = pd.DataFrame(column)
    value = pd.DataFrame(value)
    win = pd.DataFrame(df['win'])
#    std = pd.DataFrame(std)
    
    

    row.to_csv(wk_dir + 'Summer/CSR/' + c + '_row.csv', index = False)
    column.to_csv(wk_dir + 'Summer/CSR/' + c + '_column.csv', index = False)
    value.to_csv(wk_dir + 'Summer/CSR/' + c + '_value.csv', index = False)
    win.to_csv(wk_dir + 'Summer/CSR/' + c + '_win.csv', index = False)
#    std.to_csv(wk_dir + 'Summer/std.csv', index = False)