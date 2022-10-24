import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

LINE_COUNT = 5
GRID_SPACE = 0.05

def plot_candlestick(df: pd.DataFrame, buy_prices: list, sell_prices: list):
    plt.figure()
    plt.style.use('fivethirtyeight')
    candle_width = .4
    stick_width = .05

    up = df[df.Close >= df.Open]
    down = df[df.Close < df.Open]
    
    colors = ['green', 'red']
    ax1 = plt.subplot2grid((8,1), (0,0), rowspan = 6, colspan = 1)
    ax2 = plt.subplot2grid((8,1), (7,0), rowspan = 1, colspan = 1)

    # Plotting Up prices
    ax1.bar(up.index, up.Close - up.Open, candle_width, \
        bottom=up.Open, color=colors[0])
    ax1.bar(up.index, up.High - up.Close, stick_width, \
        bottom=up.Close, color=colors[0])
    ax1.bar(up.index, up.Low - up.Open, stick_width, \
        bottom=up.Open, color=colors[0])

    # Plotting Down prices
    ax1.bar(down.index, down.Close - down.Open, candle_width, \
        bottom=down.Open, color=colors[1])
    ax1.bar(down.index, down.High - down.Open, stick_width, \
        bottom=down.Open, color=colors[1])
    ax1.bar(down.index, down.Low - down.Close, stick_width, \
        bottom=down.Close, color=colors[1])

    ax2.plot([i[0] for i in buy_prices], [0.5] * len(buy_prices), marker = 'x', color = 'dodgerblue', \
        markersize = 6, label = 'BUY SIGNAL', linewidth = 0)
    ax2.plot([i[0] for i in sell_prices], [0.5] * len(sell_prices), marker = 'o', color = 'orange', \
        markersize = 6, label = 'SELL SIGNAL', linewidth = 0)
    ax2.get_xaxis().set_ticks([])
    ax2.get_yaxis().set_ticks([])
    plt.legend(loc='best')

    plt.xticks(rotation=45, ha='right')
    plt.show()

def get_grid_lines(current_price):
    stop_loss = current_price - ((LINE_COUNT + 1) * GRID_SPACE)
    take_profit = current_price + ((LINE_COUNT + 1) * GRID_SPACE)

    buy_lines = []
    sell_lines = []

    for i in range(LINE_COUNT):
        buy_lines.append(current_price - (i * GRID_SPACE))
        sell_lines.append(current_price + (i * GRID_SPACE))
         
    return stop_loss, take_profit, buy_lines, sell_lines

def calculate_position_size(acc_size, tick_value=1):
    risk = acc_size * 0.1
    ticks_at_risk = (LINE_COUNT + 1) * GRID_SPACE
    position_size = round(risk / (ticks_at_risk * tick_value), 2)
    return position_size

def calculate_profit(buy_prices: list, sell_prices: list, partial_position):
    profit = sum([y[1] - x[1] for x, y in zip(buy_price, sell_price)])
    print(f"Profit (%): {profit}")
    return profit * partial_position


init_funds = 100000

position_size = calculate_position_size(acc_size=init_funds)
partial_position = position_size / 5

df = pd.read_csv(os.path.join(os.getcwd(), 'src/data/adausdt.csv'))
buy_count = 0
buy_price = []
sell_price = []

stop_loss, take_profit, buy_lines, sell_lines = get_grid_lines(df['Close'][0])

for i in range(0, len(df)):
    if df['Close'][i] > np.min(buy_lines) and df['Close'][i] <= np.max(buy_lines) and buy_count == 0:
        print(f'Buy market price: { df.Close[i] }\t qty: {partial_position}')
        print(f'at time {i}')
        stop_loss, take_profit, buy_lines, sell_lines = get_grid_lines(df['Close'][i])
        print("=======================")
        print("buy lines: ", buy_lines)
        print("sell lines: ", sell_lines)
        print("=======================\n")
        buy_price.append((i, df.Close[i]))
        buy_count += 1

    if df['Close'][i] > np.min(sell_lines) and df['Close'][i] <= np.max(sell_lines) and buy_count > 0:
        print(f'Sell market price: { df.Close[i] }\t qty: {partial_position}')
        print(f'at time {i}')
        stop_loss, take_profit, buy_lines, sell_lines = get_grid_lines(df['Close'][i])
        print("=======================")
        print("buy lines: ", buy_lines)
        print("sell lines: ", sell_lines)
        print("=======================\n")
        sell_price.append((i, df.Close[i]))
        buy_count -= 1

calculate_profit(buy_price, sell_price, partial_position)
plot_candlestick(df.iloc[20:100], buy_price, sell_price)