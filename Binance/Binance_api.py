from dotenv import load_dotenv
from binance.client import Client
import os
import json
from websocket import WebSocketApp
from datetime import datetime
from TradingView.TradingViewDataFeed import TradingViewDataFeed

load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')
client = Client(api_key=API_KEY, api_secret=API_SECRET, testnet=True)

class BinanceTrade:
    def __init__(self, symbol):
        self.symbol = symbol.lower()
        self.trade_socket = f'wss://stream.binance.com:9443/ws/{self.symbol}@trade'
        self.ws = None
        self.curr_mkt_price = 0.0
        self.trading_view_data_feed = TradingViewDataFeed(symbol.upper(), 'BINANCE')
        self.historical_peak = self.trading_view_data_feed.get_historical_peak()

    def on_message(self, ws, message):
        json_message = json.loads(message)
        curr_event_time = json_message['E'] / 1000
        event_time = datetime.utcfromtimestamp(curr_event_time)

        self.curr_mkt_price = float(json_message['p'])


        if self.compareHighestPeak():
            print("CAUTION!!!")
            self.historical_peak = self.curr_mkt_price
        else:
            print(f'Market Price: {self.curr_mkt_price} -- {event_time}')

    def on_error(self, ws, error):
        print("Error encountered:", error)

    def on_close(self, ws, close_status_code, close_msg):
        print('------- CLOSED --------', close_status_code, close_msg)

    def on_open(self, ws):
        print("Opened Connection")

    def compareHighestPeak(self) -> bool:
        return self.historical_peak < self.curr_mkt_price

    def run(self):
        self.ws = WebSocketApp(self.trade_socket,
                               on_open=self.on_open,
                               on_message=self.on_message,
                               on_error=self.on_error,
                               on_close=self.on_close)
        self.ws.run_forever()