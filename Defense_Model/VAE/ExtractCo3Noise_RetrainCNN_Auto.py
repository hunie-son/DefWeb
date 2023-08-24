#!/usr/bin/env python
# coding: utf-8

'''
' This code is for Automatically extracting only noise, our case CO3 noise (Details in our paper)
' We re-train the CNN model to determine whether our dynamic noise can fool the attacker's CNN model
' Input  : Preprocessed WFs (train_o), reconstructed WFs (re_gen_train_x), noisy WFs (Noise_data)
' Output : accuracy
' Author : Seonghun Son (S.H, Son)
' Last updated: 8/24/23 
'''

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from csv import writer

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import datasets, layers, models
from tensorflow.keras.layers import Dense, Activation, Flatten, Dropout, Conv1D,MaxPooling1D,BatchNormalization
from tensorflow.keras.models import Sequential 

from sklearn.model_selection import train_test_split


import numpy as np
import pandas as pd

import matplotlib
from matplotlib import ticker as ticker
import matplotlib.pyplot as plt

import h5py
import os
from sklearn.metrics import f1_score


#Input Data
train_o =pd.read_csv('/DefWeb/Data_Collection/Chrome/Collected_100/trainX_100_US_Chrome.csv', header=None)
train_Y = pd.read_csv('/DefWeb/Data_Collection/Chrome/Collected_100/trainY_100_US_Chrome.csv', header=None)

re_gen_train_x = pd.read_csv('Reconstructed_x_100_6000_100D_GC.csv', header=None)
Noise_data = pd.read_csv('NoisyDataset_x_100_6000_100D_GC.csv', header=None)


trainO = train_o.to_numpy()
regen_trainX = re_gen_train_x.to_numpy()
trainY = train_Y.to_numpy()
Noise_data = Noise_data.to_numpy()

minimum = np.amin(trainO)
maximum = np.amax(trainO)

# Denormaloized Noisy Data
denormalized_Noise_data = Noise_data * (maximum-minimum) + minimum
#print(denormalized_Noise_data.shape)



print('-------------------')
print('Original Train X')
#print(trainO.shape)
print(trainO.min(),trainO.max())
print(trainO.shape)

print('-------------------')
print('Regen Train X')
#print(regen_trainX.shape)
print(regen_trainX.min(),regen_trainX.max())
print(regen_trainX.shape)

print('-------------------')
print('Train X with Noise Added')
print(denormalized_Noise_data.shape)
print(denormalized_Noise_data.min(),denormalized_Noise_data.max())



######Calculate Only Noise part######
Only_noise =denormalized_Noise_data-trainO

print('-------------------')
print('Only Noise')
print(Only_noise.shape)
print(Only_noise.min(), Only_noise.max() )


temp = np.ones((10000,6000))

# We set shift value as 1/3 amount based on the min value of dataset (see details in our paper)
co_value = 3


# Some few experiments we've conducted 
trainO_shift_up = trainO - (Only_noise.min()/co_value * temp)
print('-------------------')
print('Original Train X Shift')
print(trainO_shift_up.shape)
print(trainO_shift_up.min(),trainO_shift_up.max())
print('-------------------')
print('Noise_data min and Max')
print(Noise_data.min(),Noise_data.max())
print('-------------------')
print('Noise_data Denormalized min and Max')
print(denormalized_Noise_data.min(),denormalized_Noise_data.max())


####### This part Zeroized for the minus value ###########
print('-------------------')
print('Only Noise min and Max removed minus')
Only_noise_zeroized = np.where(Only_noise<0, 0, Only_noise)
print(Only_noise_zeroized.max())
print(Only_noise_zeroized.min())
print('-------------------')


###### Total Minus amount Shifted Up, but too much ######
print('-------------------')
print('Only Noise Total Shifted Up')

shift_up_total = Only_noise.min() * temp
print(shift_up_total.shape)
Only_noise_shift_total = Only_noise - shift_up_total

print('After Only Noise Minus amout total Shifted Up')
print(Only_noise_shift_total.shape)
print(Only_noise_shift_total.min(),Only_noise_shift_total.max())


###### Minus part only shifted up ######
print('-------------------')
print('Only Noise minus part Shifted Up')

minus_shift_up = np.where(Only_noise<0, Only_noise - (Only_noise.min()/co_value * temp), Only_noise)

print(minus_shift_up.shape)
print(minus_shift_up.min(),minus_shift_up.max())

minus_shift_up_zero = np.where(minus_shift_up<0, 0 ,minus_shift_up)
print(minus_shift_up_zero.shape)
print(minus_shift_up_zero.min(),minus_shift_up_zero.max())



########### Shift up 1/3 and Zeroized part ###########
print('-------------------')
print('Only Noise 1/co_value Shifted Up')
temp = np.ones((10000,6000))
shift_up_co = Only_noise.min()/co_value * temp
print(shift_up_co.shape)
Only_noise_shift_co = Only_noise - shift_up_co
Only_noise_shift_co = np.where(Only_noise_shift_co<0, 0, Only_noise_shift_co)

print(Only_noise_shift_co.shape)
print(Only_noise_shift_co.min(),Only_noise_shift_co.max())


# Three different experiments conducted above 
print('-------------------')
X_noise_shift = trainO + Only_noise_shift_total
X_noise_shift_minus = trainO + minus_shift_up_zero
X_noise_shift_co = trainO+ Only_noise_shift_co

print('-------------------')
print('Original')
print(trainO.shape)

print('minus_shift_up_zero')
print(minus_shift_up_zero.shape)
print(minus_shift_up_zero.min(),minus_shift_up_zero.max())

print('-------------------')
print('X_noise_shift_minus')
print(X_noise_shift_minus.shape)
print(X_noise_shift_minus.min(),X_noise_shift_minus.max())

print('-------------------')
print('Only noise amount')
print(Only_noise_shift_co.shape)
print(Only_noise_shift_co.min(),Only_noise_shift_co.max())

print('-------------------')
print('Noise added co3 shift noise')
print(X_noise_shift_co.shape)
print(X_noise_shift_co.min(),X_noise_shift_co.max())


trainY= keras.utils.to_categorical(trainY)
print(trainY.shape)


## From here we can change the input

# Normalizing the Training Data

minimum_n1 = np.amin(X_noise_shift)
maximum_n1 = np.amax(X_noise_shift)
X_noise_shift_total_norm = (X_noise_shift-minimum_n1)/(maximum_n1-minimum_n1)
print(X_noise_shift_total_norm.shape)
print(X_noise_shift_total_norm.min(),X_noise_shift_total_norm.max())

minimum_n2 = np.amin(X_noise_shift_co)
maximum_n2 = np.amax(X_noise_shift_co)
X_noise_shift_co_norm = (X_noise_shift_co-minimum_n2)/(maximum_n2-minimum_n2)
print(X_noise_shift_co_norm.shape)
print(X_noise_shift_co_norm.min(),X_noise_shift_co_norm.max())


minimum_n3 = np.amin(X_noise_shift_minus)
maximum_n3 = np.amax(X_noise_shift_minus)
X_noise_shift_minus_norm = (X_noise_shift_minus-minimum_n3)/(maximum_n3-minimum_n3)
print(X_noise_shift_minus_norm.shape)
print(X_noise_shift_minus_norm.min(),X_noise_shift_minus_norm.max())

print(Noise_data.min(),Noise_data.max())
print(re_gen_train_x.min(),re_gen_train_x.max())

test= denormalized_Noise_data - Only_noise 

minimum_t = np.amin(test)
maximum_t = np.amax(test)

test_norm = (test-minimum_t)/(maximum_t-minimum_t)
print(test_norm.shape)


'''
# We can test with five different Inputs for retraining CNN: 
# re_gen_train_x, Noise_data, X_noise_shift , X_noise_shift_minus_norm , ***X_noise_shift_co_norm**** 
# We use X_noise_shift_co_norm, which is we mentioned in our paper (DefWef)
'''

input_data =X_noise_shift_co_norm
# set aside 20% of train and test data for evaluation
X_train, X_test, y_train, y_test = train_test_split(input_data, trainY ,test_size=0.2, shuffle = True, random_state = None)

# Use the same function above for the validation set
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state= None) # 0.25 x 0.8 = 0.2

print("--------------Data--------------")
print("Orignal X shape: {}".format(trainO.shape))
print("Origianl Y shape: {}".format(trainY.shape))

print("--------------Train Data--------------")
print("X_train shape: {}".format(X_train.shape))
print("y_train shape: {}".format(y_train.shape))

print("--------------Validation Data--------------")
print("X_val shape: {}".format(X_val.shape))
print("y val shape: {}".format(y_val.shape))

print("--------------Test Data--------------")
print("X_test shape: {}".format(X_test.shape))
print("y_test shape: {}".format(y_test.shape))



def model_create(x=None):
  numberOfWebsite=100

  input = keras.Input(shape = (6000,1))
  x = layers.Conv1D(32, 3, activation="relu", padding="same")(input)
  x = layers.Conv1D(64, 3, activation="relu", padding="same")(x)
  x = MaxPooling1D(pool_size=3)(x)

    x = layers.Conv1D(128, 3, activation="relu", padding="same")(x)
  x = MaxPooling1D(pool_size=3)(x)
  
  x = layers.Dropout(0.3)(x)
  x = layers.Flatten()(x)

  x = layers.Dense(256, activation='relu')(x)
  x = layers.Dropout(0.3)(x)

  x = layers.Dense(128, activation='relu')(x)
  x = layers.Dropout(0.3)(x)
  
  x = Dense(numberOfWebsite,activation='softmax')(x)
  
  model = keras.Model(inputs = input, outputs = x)

  return model


model = model_create()
model.summary()

model.compile(loss="categorical_crossentropy",optimizer='adam',metrics=["accuracy"])

print(X_train.shape, y_train.shape)
print(X_val.shape, y_val.shape)
history = model.fit(X_train,y_train, epochs=40, validation_data=(X_val,y_val))

# Retrained CNN accuracy
cnn_score = model.evaluate(X_test, y_test, verbose=0)
print("Test loss:", cnn_score[0])
print("Test accuracy:", cnn_score[1])
ac_cnn=cnn_score[1]

# Save the Accuracy Results
with open('CNN_Retrain_NoisyData_co3_accuracy.txt', 'a',encoding='utf-8') as f:
    f.write(str(ac_cnn)+'\n')

