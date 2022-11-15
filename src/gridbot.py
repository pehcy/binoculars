import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

class GridBot:
    '''
     Gridbot strategy class
    '''
    
    def __init__(self, df: pd.DataFrame) -> None:
        self.stop_loss = 0
        self.take_profit = 0
        self.buy_lines = np.array([])
        self.sell_lines = np.array([])
        self.df = df

        self.LINE_COUNT = 5
        self.GRID_SPACE = 0.05

        position_size = self.calculate_position_size(acc_size=10000)
        self.partial_position = position_size / 5

        # Buy and Sell prices after running strategy
        self.buy_prices = []
        self.sell_prices = []
        self.profits = []

    def calculate_position_size(self, acc_size, tick_value=1) -> float:
        risk = acc_size * 0.1
        ticks_at_risk = (self.LINE_COUNT + 1) * self.GRID_SPACE
        position_size = round(risk / (ticks_at_risk * tick_value), 2)
        return position_size

    def plot_candlestick(self) -> None:
        df = self.df
        buy_prices = self.buy_prices
        sell_prices = self.sell_prices
        
        plt.figure()
        plt.style.use('bmh')
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

        plt.xticks(rotation=45, ha='right')
        plt.show()

    def get_grid_lines(self, current_price) -> tuple([float, float, list, list]):
        stop_loss = current_price - ((self.LINE_COUNT + 1) * self.GRID_SPACE)
        take_profit = current_price + ((self.LINE_COUNT + 1) * self.GRID_SPACE)

        buy_lines = []
        sell_lines = []

        for i in range(self.LINE_COUNT):
            buy_lines.append(current_price - (i * self.GRID_SPACE))
            sell_lines.append(current_price + (i * self.GRID_SPACE))
            
        return stop_loss, take_profit, buy_lines, sell_lines

    def run_strategy(self) -> None:
        buy_count = 0
        buy_prices = []
        sell_prices = []
        df = self.df

        self.stop_loss, self.take_profit, self.buy_lines, self.sell_lines = self.get_grid_lines(df['Close'][0])

        for i in range(0, len(df)):
            if df['Close'][i] > np.min(self.buy_lines) and df['Close'][i] <= np.max(self.buy_lines) \
                    and buy_count == 0:
                print(f'Buy market price: { df.Close[i] }\t qty: {self.partial_position}')
                print(f'at time {i}')
                self.stop_loss, self.take_profit, self.buy_lines, self.sell_lines = self.get_grid_lines(df['Close'][i])
                print("=======================")
                print("buy lines: ", self.buy_lines)
                print("sell lines: ", self.sell_lines)
                print("=======================\n")
                buy_prices.append((i, df.Close[i]))
                buy_count += 1

            if df['Close'][i] > np.min(self.sell_lines) and df['Close'][i] <= np.max(self.sell_lines) \
                    and buy_count > 0:
                print(f'Sell market price: { df.Close[i] }\t qty: {self.partial_position}')
                print(f'at time {i}')
                self.stop_loss, self.take_profit, self.buy_lines, self.sell_lines = self.get_grid_lines(df['Close'][i])
                print("=======================")
                print("buy lines: ", self.buy_lines)
                print("sell lines: ", self.sell_lines)
                print("=======================\n")
                sell_prices.append((i, df.Close[i]))
                buy_count -= 1
        
        self.buy_prices = buy_prices
        self.sell_prices = sell_prices
        self.profits = [y[1] - x[1] for x, y in zip(self.buy_prices, self.sell_prices)]

    def calculate_profit(self) -> float:
        total_profit = sum([y[1] - x[1] for x, y in zip(self.buy_prices, self.sell_prices)])
        print(f"Profit (%): {total_profit}")
        return total_profit * self.partial_position

# 2020: Profit (%): 0.009880000000000003     pnl: 13.173332016000007
# 2022: Profit (%): 0.10099999999999976     pnl: 224.44442199999946

df = pd.read_csv(os.path.join(os.getcwd(), 'src/data/adausdt_2020.csv'))
gridbot = GridBot(df)
gridbot.run_strategy()
gridbot.calculate_profit()
print(gridbot.profits)
gridbot.plot_candlestick()