from dotenv import load_dotenv
from binance.client import Client
import os
import json
from websocket import WebSocketApp
from datetime import datetime
from TradingView.TradingViewDataFeed import TradingViewDataFeed
import threading

load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')
client = Client(api_key=API_KEY, api_secret=API_SECRET, testnet=True)

class BinanceTrade:
    def __init__(self, symbol):
        self.symbol = symbol.lower()
        self.trade_socket = f'wss://stream.binance.com:9443/ws/{self.symbol}@trade'
        self.ws = None
        self.thread = None
        self.curr_mkt_price = 0.0
        self.trading_view_data_feed = TradingViewDataFeed(symbol.upper(), 'BINANCE')
        self.historical_peak = self.trading_view_data_feed.get_historical_peak()
        self.event_time = datetime

    def on_message(self, ws, message):
        json_message = json.loads(message)
        curr_event_time = json_message['E'] / 1000
        self.event_time = datetime.utcfromtimestamp(curr_event_time)

        self.curr_mkt_price = float(json_message['p'])

        print(f'Market Price: {self.curr_mkt_price} -- {self.event_time}')

    def on_error(self, ws, error):
        print("Error encountered:", error)

    def on_close(self, ws, close_status_code, close_msg):
        print('------- CLOSED --------')

    def on_open(self, ws):
        print("Opened Connection")

    def note_highest_peak(self):
        return self.historical_peak < self.curr_mkt_price

    def note_specific_price(self, specificPrice):
        return specificPrice <= self.curr_mkt_price
    
    def getEventTime(self):
        return self.event_time
    
    def getHistoricalPeak(self):
        return self.historical_peak

    def run(self):
        self.ws = WebSocketApp(self.trade_socket,
                               on_open=self.on_open,
                               on_message=self.on_message,
                               on_error=self.on_error,
                               on_close=self.on_close)
        self.ws.run_forever()

    def start(self):
        self.thread = threading.Thread(target = self.run)
        self.thread.start()