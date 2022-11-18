import os
import sys
here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, '..'))

from lstm import *
from macd import *

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

    macd_input = pd.Series(predicted_stock_price.flatten())

    macd_bot = MACDStrategy(macd_input)
    total, rate = macd_bot.get_return_rates(investment_value=1e5)
    print(f'Total investment: {total}')
    print(f'Total profit percentage: {rate}')
    macd_bot.plot_macd()