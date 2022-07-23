from datetime import datetime
import pandas as pd
import time

"""
exporting historical klines/candlestick data
to csv file.
Response: [Open time, Open, High, Low, Close, Volume]

Reference: https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#klinecandlestick-data
"""

# local readable time format to UTC timestamp
def ms_to_dt_utc(ms: int) -> datetime:
    return datetime.utcfromtimestamp(ms / 1000)

# UTC timestamp to local readable time format
def ms_to_dt_local(ms: int) -> datetime:
    return datetime.fromtimestamp(ms / 1000)

def export_klines(symbol: str, interval, start, end, limit=5000):
    df = pd.DataFrame()
    start_iter_date = end
    while start_iter_date > start:
        url = 'https://api.binance.com/api/v3/klines?symbol=' + \
            symbol + '&interval=' + interval + '&limit=' + str(limit)
        if start_iter_date is not None:
            url += '&endTime=' + str(start_iter_date)

        df_query = pd.read_json(url)
        df_query.columns = [
            'Opentime', 
            'Open', 
            'High', 
            'Low', 
            'Close', 
            'Volume', 
            'Closetime', 
            'Quote asset volume', 
            'Number of trades',
            'Taker by base', 
            'Taker buy quote', 
            'Ignore' ]
        

        df = pd.concat([df_query, df], axis=0, ignore_index=True, keys=None)
        start_iter_date = df['Opentime'][0]
    
    df.reset_index(drop=True, inplace=True)
    df['Opentime'] = df['Opentime'].apply(lambda x: ms_to_dt_local(x))
    
    df.to_csv(f'src/data/{symbol.lower()}.csv', index=False)
    print('CSV file has been exported. You can check inside data folder!\n')
    print(df)

if __name__ == "__main__":
    symbols_list = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "LTCUSDT", "NEOUSDT", "ADAUSDT", "ETHBTC", "BNBBTC"]
    interval = '1m'
    #print(fromDate)
    fromDate = int(datetime.strptime('2021-12-15 00:00:00', '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
    toDate = int(datetime.strptime('2021-12-16 00:00:00', '%Y-%m-%d %H:%M:%S').timestamp() * 1000)

    for symbol in symbols_list:
        export_klines(symbol, interval, fromDate, toDate)