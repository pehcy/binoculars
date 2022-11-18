import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

import tensorflow as tf
from keras.layers import Bidirectional, Dense, Dropout, LSTM 

import os
import matplotlib.pyplot as plt

class EarlyStopping(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if logs.get('mae') < 0.02:
            print('\nMAE threshold reached. Training stopped')
            self.model.stop_training = True

class LSTMBotModel(tf.keras.Model):
    def __init__(self, *args, **kwargs) -> None:
        super(LSTMBotModel, self).__init__(*args, **kwargs)

    def call(self, X_train):
        self.model = tf.keras.models.Sequential([
            Bidirectional(LSTM(50, return_sequences=True, input_shape = (X_train.shape[1], 1))),
            Dropout(0.2),
            Bidirectional(LSTM(50, return_sequences=True)),
            Dropout(0.2),
            Bidirectional(LSTM(50, return_sequences=True)),
            Dropout(0.2),
            Bidirectional(LSTM(50)),
            Dense(units=1, activation='linear')
        ])
        
        self.model.compile(optimizer='adam', \
            loss=tf.keras.losses.MeanSquaredError(),\
            metrics=['mae'])
    
    def fit(self, X_train, y_train, epochs=100, callbacks=[EarlyStopping()]):
        history = self.model.fit(X_train, y_train, epochs=epochs, callbacks=callbacks)
        return history

    def predict(self, X_test):
        predicted_stock_price = self.model.predict(X_test)
        return predicted_stock_price