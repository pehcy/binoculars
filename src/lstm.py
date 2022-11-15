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

if __name__ == '__main__':
    df = pd.read_csv(os.path.join(os.getcwd(), 'src/data/adausdt_2020.csv'))
    split = int(len(df['Close']) * 0.8)
    training_set = df.loc[:split,['Close']].values

    scaler = MinMaxScaler(feature_range=(0,1))
    training_set_scaled = scaler.fit_transform(training_set)

    X_train, y_train = [], []

    for i in range(14, split):
        X_train.append(training_set_scaled[i-14:i, 0])
        y_train.append(training_set_scaled[i, 0])

    X_train, y_train = np.array(X_train), np.array(y_train)

    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    lstm_model = LSTMBotModel()
    lstm_model.call(X_train)
    history = lstm_model.fit(X_train, y_train, epochs=100)

    real_prices = df.loc[split - 14:, ['Close']].values
    inputs = scaler.transform(real_prices)
    X_test = []
    for i in range(14, len(inputs)):
        X_test.append(inputs[i-14:i, 0])

    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    predicted_stock_price = scaler.inverse_transform(lstm_model.predict(X_test))

    plt.style.use('bmh')
    plt.plot(df.loc[split:,['Close']].values, color = 'black', label = 'Real Close Price')
    plt.plot(predicted_stock_price, color = 'green', label = 'Predicted Close Price')
    plt.title('Close Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('Close Price')
    plt.legend()
    plt.show()