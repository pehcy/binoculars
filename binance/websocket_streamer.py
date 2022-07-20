import websocket
import json
from utils.Logger import Logger

'''
Established connection to Binance Kline/Candlestick Streams
references: https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#klinecandlestick-streams

Usage:
>>> kstreamer = KlineStreamer('btcusdt', '1m')
>>> kstreamer.start_socket()

result:
{
  "e": "kline",     // Event type
  "E": 123456789,   // Event time
  "s": "BNBBTC",    // Symbol
  "k": {
    "t": 123400000, // Kline start time
    "T": 123460000, // Kline close time
    "s": "BNBBTC",  // Symbol
    "i": "1m",      // Interval
    "f": 100,       // First trade ID
    "L": 200,       // Last trade ID
    "o": "0.0010",  // Open price
    "c": "0.0020",  // Close price
    "h": "0.0025",  // High price
    "l": "0.0015",  // Low price
    "v": "1000",    // Base asset volume
    "n": 100,       // Number of trades
    "x": false,     // Is this kline closed?
    "q": "1.0000",  // Quote asset volume
    "V": "500",     // Taker buy base asset volume
    "Q": "0.500",   // Taker buy quote asset volume
    "B": "123456"   // Ignore
  }
}
'''

class KlineStreamer:
    def __init__(self, symbol: str, interval: str) -> None:
        websocket.enableTrace(True)
        socketEndpoint = f'wss://stream.binance.us:9443/ws/{symbol}@kline_{interval}'
        self.ws = websocket.WebSocketApp(socketEndpoint,
                                    on_message=lambda ws, msg: self.onMessage(ws, msg),
                                    on_error=lambda ws, error: self.onError(ws, error),
                                    on_close=lambda close_msg: self.onClose(close_msg))

    def onMessage(self, ws, msg):
        data = json.loads(msg)
        Logger.log(timestamp=data['E'], klines=data['k'])

    def onError(self, ws, error):
        print(error)

    def onClose(self, close_msg):
        print(close_msg)

    def start_socket(self):
        self.ws.run_forever()