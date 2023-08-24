#!/usr/bin/env python
# coding: utf-8

'''
' This code is for Automatically run our DefWeb (VAE potion)
' We created 100-dimensional latent space for 100 website cluster 
' (DefWeb_VAE_Demp.ipynb contains detailed explanation)
'
' Input  : Preprocessed WFs
' Output : Reconstructed WFs and Noisy WFs
' Author : Seonghun Son (S.H, Son)
' Last updated: 8/24/23 
'''



import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['MPLCONFIGDIR'] = os.getcwd() + "/configs/"
import csv
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from scipy.stats import norm

import keras
from keras.datasets import mnist
from keras.layers import Input, Reshape, Conv1D, Conv1DTranspose,  Flatten, Dense, Lambda, MaxPooling1D, BatchNormalization, Dropout, Activation, UpSampling1D
from keras.models import Sequential
from keras.callbacks import EarlyStopping


from collections import Counter
from tensorflow import keras

from keras.models import Model
from keras import metrics
from keras import backend as K   # 'generic' backend so code works with either tensorflow or theano

from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


K.clear_session()


#Input data
train_X = pd.read_csv('/DefWeb/Data_Collection/Chrome/Collected_100/trainX_100_US_Chrome.csv', header=None)
train_Y = pd.read_csv('/DefWeb/Data_Collection/Chrome/Collected_100/trainY_100_US_Chrome.csv', header=None)

trainX = train_X.to_numpy()
trainY = train_Y.to_numpy()

websites_test = [trainX[i:i + 100] for i in range(0, len(trainX), 100)]
websites_test=np.asarray(websites_test)

web_num =0
for web_num in range (0,100):
       np.random.shuffle(websites_test[web_num])

websites_shuffled=np.reshape(websites_test,(10000,6000))

trainX = np.expand_dims(trainX,axis=2)
websites_shuffled = np.expand_dims(websites_shuffled,axis=2)



# Normalize Input Data
minimum = np.amin(trainX)
maximum = np.amax(trainX)

trainX_normalized = (trainX-minimum)/(maximum-minimum)
trainX_test = trainX_normalized

minimum_s = np.amin(websites_shuffled)
maximum_s = np.amax(websites_shuffled)

Shuffled_train_normalized = (websites_shuffled-minimum_s)/(maximum_s-minimum_s)
trainX_Shuffled = Shuffled_train_normalized



# Latend space Dimension
latent_dim = 100

# sampling function
def sampling(args):
    z_mu, z_log_sigma = args
    epsilon = K.random_normal(shape=(K.shape(z_mu)[0], latent_dim),
                              mean=0., stddev=1.)
    return z_mu + K.exp(z_log_sigma) * epsilon

# VAE Encoder
inputs_shape = (6000,1)
encoder_inputs = Input(shape=inputs_shape)

x = layers.Conv1D(32, 3, activation="relu", padding="same")(encoder_inputs)
x = layers.Conv1D(64, 3, activation="relu", padding="same")(x)
x = layers.Conv1D(128, 3, activation="relu", padding="same")(x)


shape_before_flattening = K.int_shape(x)

x = layers.Flatten()(x)


z_mean = layers.Dense(latent_dim, name="z_mean")(x)
z_log_var = layers.Dense(latent_dim, name="z_log_var")(x)


z = Lambda(sampling)([z_mean, z_log_var])
encoder = keras.Model(encoder_inputs, [z_mean, z_log_var, z], name="encoder")
encoder.summary()


# VAE Decoder
print(K.int_shape(z)[1:])
decoder_input = Input(K.int_shape(z)[1:])

x = Dense(np.prod(shape_before_flattening[1:]), activation="relu")(decoder_input)

# reshape
x = Reshape(shape_before_flattening[1:])(x)
# use Conv1DTranspose to reverse the conv layers from the encoder
x = Conv1DTranspose(128, 3, padding='same', activation='relu')(x)
x = Conv1DTranspose(64, 3, padding='same', activation='relu')(x)
x = Conv1DTranspose(32, 3, padding='same', activation='relu')(x)

x = Conv1D(1, 1, padding='same', activation='sigmoid')(x)


decoder = Model(decoder_input, x)
z_decoder = decoder(z)
decoder.summary()



class VAE(keras.Model):
    def __init__(self, encoder, decoder, **kwargs):
        super(VAE, self).__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder
        self.total_loss_tracker = keras.metrics.Mean(name="total_loss")
        self.reconstruction_loss_tracker = keras.metrics.Mean(
            name="reconstruction_loss"
        )
        self.kl_loss_tracker = keras.metrics.Mean(name="kl_loss")

    @property
    def metrics(self):
        return [
            self.total_loss_tracker,
            self.reconstruction_loss_tracker,
            self.kl_loss_tracker,
        ]

    def train_step(self, data):
        with tf.GradientTape() as tape:
            z_mean, z_log_var, z = self.encoder(data)
            reconstruction = self.decoder(z)
            reconstruction_loss = tf.reduce_mean(tf.reduce_sum(keras.losses.binary_crossentropy(data, reconstruction), axis =(1))
            )
            kl_loss = -0.5 * (1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var))
            kl_loss = tf.reduce_mean(tf.reduce_sum(kl_loss, axis=0))
            total_loss = reconstruction_loss + kl_loss
        grads = tape.gradient(total_loss, self.trainable_weights)
        self.optimizer.apply_gradients(zip(grads, self.trainable_weights))
        self.total_loss_tracker.update_state(total_loss)
        self.reconstruction_loss_tracker.update_state(reconstruction_loss)
        self.kl_loss_tracker.update_state(kl_loss)
        return {
            "loss": self.total_loss_tracker.result(),
            "reconstruction_loss": self.reconstruction_loss_tracker.result(),
            "kl_loss": self.kl_loss_tracker.result(),
        }


# Define Batch Size
batchSize = 2

vae = VAE(encoder, decoder)
print(vae)
vae.compile(optimizer=keras.optimizers.Adam())
#callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3)
early_stopping = EarlyStopping(monitor='reconstruction_loss', min_delta=0, patience=10, verbose=5, mode='auto')
###########
#print(X_train.shape)
#print(trainX_test.shape)
#print(trainX_Shuffled.shape)
###########
vae.fit(trainX_Shuffled, epochs=300, batch_size=batchSize)

encoder = Model(encoder_inputs, z_mean)
X_valid_encoded_ori = encoder.predict(trainX_test, batch_size=batchSize)


# Translate into the latent space
Encoder_spread = Model(encoder_inputs, z_mean)
X_valid_encoded_new = Encoder_spread.predict(trainX_test, batch_size=batchSize)

step = 100
Num_websites = 100
measurement = 100

websites = [X_valid_encoded_new[i:i + step] for i in range(0, len(X_valid_encoded_new), step)]
websites=np.asarray(websites)


print('----------------------------------------------------------------')
#Each Websites Mean
mean = [np.mean(websites[i,:],axis=0) for i in range(0, Num_websites)]
mean=np.asarray(mean)

print('----------------------------------------------------------------')
#Total Mean (1, 100)
total_mean = 0
for i in range (0,Num_websites):
    total_mean += np.mean(websites[i,:],axis=0)
    
total_mean= total_mean/Num_websites

print('----------------------------------------------------------------')

#Distance from total mean 
Distance = np.ones((Num_websites,latent_dim))
for i in range (0,Num_websites):
    Distance[i,:] = total_mean - mean[i,:]
    

#Distance expand
Dis_ex = np.ones((Num_websites,measurement,latent_dim))
for i in range (0,Num_websites):
    for k in range (0,measurement):
        Dis_ex[i,k,:]=Distance[i]
print('----------------------------------------------------------------')

# Calculating distance between each website cluster
print('----------------------------------------------------------------')
dist = np.ones((Num_websites,Num_websites,latent_dim))
print(dist.shape)

for i in range (0,Num_websites):
    for k in range (0,Num_websites):
        dist[i,k,:] = mean[i,:] - mean[k,:]
        
dist=np.asarray(dist)

Dis_ex_each = np.zeros((Num_websites,measurement,latent_dim))
print('----------------------------------------------------------------')
for i in range (0,100,Num_websites):
    Dis_ex_each[:,0+i:Num_websites+i,:] = dist
  

print('----------------------------------------------------------------')

Website_Noise_mean =  websites + Dis_ex
#If size are not matched use Dis_ex_each to expand the size (See DefWeb_VAE_Demo.
Website_Noise_each_web = websites - dist


'''
print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')  
#print('test----------------------------------------------------------------')    
#print(dist)
print(dist[0,1,:])

ex = np.zeros((measurement,latent_dim))

test_website = 0
test_measure  = 5

for i in range (0,100):
    ex[i,:] = dist[test_website,test_measure,:]

ex_total= np.zeros((Num_websites,measurement,latent_dim))    
print('----------------------------------------------------------------')
for k in range (0,100,Num_websites):
    ex_total[:,0+k:Num_websites+i,:] = ex

    

Website_Noise_each_web_test = websites - ex
Website_Noise_each_web_test=np.reshape(Website_Noise_each_web_test,(Num_websites*measurement,latent_dim))

'''

#Reshaping
Website_Noise_mean=np.reshape(Website_Noise_mean,(Num_websites*measurement,latent_dim))
Website_Noise_each_web=np.reshape(Website_Noise_each_web,(Num_websites*measurement,latent_dim))

z_mean, z_log_var, z = vae.encoder.predict(trainX_test)
re_generated_x = vae.decoder.predict(z)

# Loade Pre-trained CNN model
classification_model = tf.keras.models.load_model('home/seonghun/Research/WebsiteFingerPrinting/CNN/CNN_Pretrained_Model_chrome_W2.h5')
re_generated_x_save = np.squeeze(re_generated_x)
trainY_ca= keras.utils.to_categorical(trainY)
prediction = np.argmax(classification_model.predict(re_generated_x_save), axis=1)

test = classification_model.predict(re_generated_x_save)

score = classification_model.evaluate(re_generated_x_save, trainY_ca, verbose=0)
print(" loss:", score[0])
print("accuracy:", score[1])

# Reconstructed WF Dataset Accuracy 
print(score)
ac_vae=score[1]

dist_re=np.reshape(dist,(Num_websites*measurement,latent_dim))
new_z = Lambda(sampling)([Website_Noise_mean, z_log_var])
np.array(new_z)
generated_x_noise = vae.decoder.predict(new_z)

generated_x_noise_save = np.squeeze(generated_x_noise)
prediction_new = np.argmax(classification_model.predict(generated_x_noise_save), axis=1)
score = classification_model.evaluate(generated_x_noise_save, trainY_ca, verbose=0)


######From here with the Each Spreaded Noise ##########i

new_z_each = Lambda(sampling)([Website_Noise_each_web, z_log_var])
np.array(new_z_each)
generated_x_noise_each = vae.decoder.predict(new_z_each)
generated_x_noise_each_save = np.squeeze(generated_x_noise_each)
prediction_new = np.argmax(classification_model.predict(generated_x_noise_each_save), axis=1)
prediction_new_score = classification_model.predict(generated_x_noise_each_save)


score_noise = classification_model.evaluate(generated_x_noise_each_save, trainY_ca, verbose=0)
print(" loss:", score_noise[0])
print("accuracy:", score_noise[1])

# Noisy WF Dataset Accuracy
print(score_noise)
ac_noise=score_noise[1]

trainY_test = np.ones((10000,1))

for k in range (0,100):
    for i in range (0,100):
        trainY_test[i+k*100]=int(i)

trainY_test_ca= keras.utils.to_categorical(trainY_test)

score_noise_test = classification_model.evaluate(generated_x_noise_each_save, trainY_test_ca, verbose=0)
print(" loss:", score_noise_test[0])
print("accuracy:", score_noise_test[1])
print(score_noise_test)
ac_noiseWithNewY=score_noise_test[1]


#Saving accuracy Result
with open('AutomationCNNResult/VAE_accuracy_GC.txt', 'a',encoding='utf-8') as f:
    f.write(str(ac_vae)+'\n')
        
with open('RegeneratedNoiseAccuracy_GC.txt', 'a',encoding='utf-8') as f:
    f.write(str(ac_noise)+'\n')
    
with open('RegeneratedNoiseAccuracy_withNewLableY_GC.txt', 'a',encoding='utf-8') as f:
    f.write(str(ac_noiseWithNewY)+'\n')


# Saving reconstructed WF Dataset
with open('Reconstructed_x_100_6000_100D_GC.csv', 'w', newline='') as file:
    mywriter = csv.writer(file, delimiter=',')
    mywriter.writerows(re_generated_x_save)



with open('NoisyDataset_x_100_6000_100D_GC.csv', 'w', newline='') as file:
    mywriter = csv.writer(file, delimiter=',')
    mywriter.writerows(generated_x_noise_each_save)
    
    
    
print("END VAE")

