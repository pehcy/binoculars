from datetime import datetime, date, timedelta
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

def export_klines(symbol: str, interval, start, end, show_date, limit=5000):
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
    
    if show_date is True:
        date_filename = str(ms_to_dt_local(start)).replace(' 00:00:00', '')
        df.to_csv(f'src/data/macd_sample/{symbol.lower()}_{date_filename}.csv', index=False)
    else:
        df.to_csv(f'src/data/{symbol.lower()}.csv', index=False)
    print('CSV file has been exported. You can check inside data folder!\n')
    print(df)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

if __name__ == "__main__":
    symbols_list = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "LTCUSDT", "NEOUSDT", "ADAUSDT", "ETHBTC", "BNBBTC"]
    interval = '1d'
    # sample date chosen
    # fromDate = int(datetime.strptime('2022-8-01 00:00:00', '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
    # toDate = int(datetime.strptime('2022-8-20 00:00:00', '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
    
    start_date = datetime.strptime('2022-8-01','%Y-%m-%d')
    end_date = datetime.strptime('2022-8-21','%Y-%m-%d')

    for single_date in daterange(start_date, end_date):
        next_day = single_date + timedelta(1)
        export_klines(symbols_list[0], interval, \
            int(single_date.timestamp() * 1000), \
            int(next_day.timestamp() * 1000), \
            show_date=True)

    # export_klines()

    #for symbol in symbols_list:
    #    export_klines(symbol, interval, fromDate, toDate)