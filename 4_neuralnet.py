
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 18:07:57 2018

@author: hongjianyang
"""

wk_dir = '/Users/hongjianyang/Desktop/LoL Project/'

import numpy as np

import pandas as pd
from keras.models import Model, Sequential
from sklearn.cross_validation import train_test_split
from keras.layers import Dense
from keras import regularizers

df = pd.read_csv(wk_dir + "data.csv")
df = df.fillna(0)
data = df.iloc[:,0:-1]

win = df['win']
train_data, test_data, win_train, win_test = train_test_split(data, win, test_size = 0.1, random_state = 42)

model = Sequential()
model.add(Dense(2000, kernel_initializer='normal'
                    ,activation='sigmoid', input_dim = 141))
model.add(Dense(400, kernel_initializer='normal'
                    ,activation='sigmoid'))
#model.add(Dense(50, kernel_initializer='normal'
#                    ,kernel_regularizer=regularizers.l1(5)
#                    ,activation='sigmoid'))
model.add(Dense(1, kernel_initializer='normal'
                    ,activation='sigmoid'))
model.compile(loss="binary_crossentropy", optimizer='adam', metrics = ["accuracy"])

model.fit(train_data.values, win_train.values, batch_size = 64, epochs=40)

accuracy = model.evaluate(test_data.values, win_test.values)