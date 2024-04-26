import pandas as pd
from dotenv import load_dotenv
from binance.client import Client
import requests
import os
import json
import websocket
from websocket import WebSocketApp
from datetime import datetime

load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')
client = Client(api_key=API_KEY, api_secret=API_SECRET, testnet=True)

class BinanceTrade:
    def __init__(self, symbol):
        self.symbol = symbol.lower()
        self.trade_socket = f'wss://stream.binance.com:9443/ws/{self.symbol}@trade'
        self.kline_socket = f'wss://nbstream.binance.com/eoptions/ws/{self.symbol}@kline_1m'
        self.ws = None

    def on_message(self, ws, message):
        json_message = json.loads(message)
        curr_event_time = json_message['E'] / 1000
        event_time = datetime.utcfromtimestamp(curr_event_time)

        curr_mkt_price = json_message['p']
        print(f'Market Price: {curr_mkt_price} -- {event_time}')

    def comparePrice():
        pass

    def on_error(self, ws, error):
        print("Error encountered:", error)

    def on_close(self, ws, close_status_code, close_msg):
        print('------- CLOSED --------', close_status_code, close_msg)

    def on_open(self, ws):
        print("Opened Connection")

    def run(self):
        self.ws = WebSocketApp(self.trade_socket,
                               on_open=self.on_open,
                               on_message=self.on_message,
                               on_error=self.on_error,
                               on_close=self.on_close)
        self.ws.run_forever()

if __name__ == '__main__':
    symbol = 'btcusdt'  # Example symbol, can be replaced with any other
    ws_client = BinanceTrade(symbol)
    ws_client.run()