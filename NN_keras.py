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

model = Sequential()
model.add(Dense(30, activation='relu', input_dim=9))
model.add(Dense(7, activation='softmax'))
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Generate dummy data

with open('glass.csv',newline='') as csvfile:
    raw_data = list(csv.reader(csvfile))

np_data = np.array(raw_data)
header = np_data[0,:]
data = np_data[1:,:9].astype(float)
labels = np_data[1:,9].astype(int) - 1

#data = np.random.random((1000, 100))
#labels = np.random.randint(10, size=(1000, 1))

# Convert labels to categorical one-hot encoding
one_hot_labels = keras.utils.to_categorical(labels, num_classes=7)

# Train the model, iterating on the data in batches of 32 samples
model.fit(data, one_hot_labels, epochs=100, batch_size=32)

