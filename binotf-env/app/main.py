from fastapi import FastAPI
from pydantic import BaseModel
from uvicorn import run

import numpy as np
from typing import List, Union
from sklearn.preprocessing import MinMaxScaler
import os

from lstm import *

app = FastAPI()

class ClosePrices(BaseModel):
    prices: List[Union[float, None]]

@app.get("/")
def read_root():
    return {"message": "Hello World for Close Price prediction API for Binance."}

@app.post("/pred1d")
async def predict_prices(data: ClosePrices):
    data = data.dict()
    input = np.array(data['prices'])

    split = int(len(input) * 0.8)
    scaler = MinMaxScaler(feature_range=(0,1))
    training_set_scaled = scaler.fit_transform(input.reshape(-1,1))

    X_train, y_train = [], []

    for i in range(14, split):
        X_train.append(training_set_scaled[i-14:i, 0])
        y_train.append(training_set_scaled[i, 0])
    
    X_train, y_train = np.array(X_train), np.array(y_train)

    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    lstm_model = LSTMBotModel()
    lstm_model.call(X_train)
    history = lstm_model.fit(X_train, y_train, epochs=100)

    real_prices = input[split - 14:]
    inputs = scaler.transform(real_prices.reshape(-1,1))
    X_test = []
    for i in range(14, len(inputs)):
        X_test.append(inputs[i-14:i, 0])

    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    predicted_stock_price = scaler.inverse_transform(lstm_model.predict(X_test))

    return {'prediction': predicted_stock_price.flatten().tolist()}

if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 5000))
    run(app, host="0.0.0.0", port=8000)