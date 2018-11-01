#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 13:40:23 2018

@author: hongjianyang
"""
wk_dir = '/Users/hongjianyang/Desktop/LoL Project/'

import pandas as pd
import numpy as np
dataset = pd.read_csv(wk_dir + 'Summer/Base_Interaction_60000.csv')

#dataset = dataset.drop('Unnamed: 0', axis = 1)
dataset_array = np.array(dataset)
row = [0] + [55*i for i in range(1,61047)]
column = dataset_array.nonzero()[1]
value = dataset_array[dataset_array.nonzero()]

row = pd.DataFrame(row)
column = pd.DataFrame(column)
value = pd.DataFrame(value)


row.to_csv(wk_dir + 'Summer/CSR/large_row.csv', index = False)
column.to_csv(wk_dir + 'Summer/CSR/large_column.csv', index = False)
value.to_csv(wk_dir + 'Summer/CSR/large_value.csv', index = False)