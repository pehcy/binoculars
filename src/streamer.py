import websocket
import datetime
import duck

def on_message(ws, message):
    print(str(datetime.datetime.now()) + ': ')
    print(type(message))
    duck.log_duckdb(message)

def on_error(ws, error):
    print(error)

def on_close(close_msg):
    print('### Closed ###' + close_msg)

def stream_kline(symbol: str):
    websocket.enableTrace(False)
    # socket = f'wss://stream.binance.com:9443/ws/{symbol.lower()}@kline_{interval}'
    socket = f'wss://stream.binance.com:9443/ws/{symbol.lower()}@depth5'
    ws = websocket.WebSocketApp(socket,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()

duck.init_duckdb()

if __name__ == '__main__':
    print("start server")
    stream_kline('bnbbtc')