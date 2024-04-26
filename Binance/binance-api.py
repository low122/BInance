import pandas as pd
from dotenv import load_dotenv
import os
from binance.client import Client
import requests
import json
import websocket
from websocket import WebSocketApp
from datetime import datetime

load_dotenv()

api_key = 'NQbQTdz3KpUDvbGau9ranZUS7LxogPwuKERQ0Lf822OccIwzBdWXdzhSah9UApTG'
api_secret = 'XSbXZPnIl4K6lolkjc9dN0PCvRyS9JFgJCKx0bsXQUhV6PnqRP77bOh1eS7UNM3e'

client = Client(api_key=api_key, api_secret=api_secret, testnet=True)

socket = 'wss://stream.binance.com:9443/ws/btcusdt@trade'
klineSocket = 'wss://nbstream.binance.com/eoptions/ws/btcusdt/@kline_1m'

def on_message(ws, message):
    jsonMessage = json.loads(message)
    currEventTime = jsonMessage['E'] / 1000
    event_time = datetime.utcfromtimestamp(currEventTime)

    currMktPrice = jsonMessage['p']
    print(f'Market Price: {currMktPrice} -- {event_time}')

def on_error(ws, error):
    print("Error encountered:", error)

def on_close(ws, close_status_code, close_msg):
    print('------- CLOSED --------', close_status_code, close_msg)

def on_open(ws):
    print("Opened Connections")
    


if __name__ == '__main__':
    ws = WebSocketApp(url=socket,
                        on_open=on_open,
                        on_message=on_message,
                        on_error=on_error,
                        on_close=on_close)
    
    ws.run_forever()