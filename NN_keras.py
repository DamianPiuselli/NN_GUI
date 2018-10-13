#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 21:59:36 2018

@author: damian
"""
import numpy as np
import keras as keras
import csv
from keras.models import Sequential
from keras.layers import Dense, Activation


import keras.backend as K

def mean_pred(y_true, y_pred):
    return K.mean(y_pred)



model = Sequential()
model.input
model.add(Dense(1, kernel_initializer='normal', activation='linear', input_dim=1))
model.add(Dense(1,activation='relu'))
model.compile(optimizer='rmsprop',
              loss='mean_squared_error',metrics=['mse'])

# Generate dummy data

#data = np.random.random((1000, 10))
#labels = np.random.randint(10, size=(1000, 1))
data = np.linspace(-50, 100, 200)
labels = 2*data + +1000

# Train the model, iterating on the data in batches of 32 samples
model.fit(data, labels, epochs=500, batch_size=32)

