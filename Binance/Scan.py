import asyncio
import aiohttp
from dotenv import load_dotenv
from binance.client import Client
import os
import json
from websocket import WebSocketApp
import datetime
from TradingView.TradingViewDataFeed import TradingViewDataFeed
import threading

load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')
client = Client(api_key=API_KEY, api_secret=API_SECRET, testnet=True)

trade_socket = 'https://api.binance.com/api/v3/klines'

all_tickers = client.get_all_tickers()

# for ticker in all_tickers:
#     print(ticker)

usdt_tickers = [ticker for ticker in all_tickers if ticker['symbol'].endswith('USDT')]

class Scan_api:
    def __init__(self) -> None:
        self.current_vol = None
        self.previous_vol = None
        self.current_time = None
        self.eligible_coins = []
        self.eligible_coin = None
        self.results_without_duplication = []

    async def fetch_klines(self, session, symbol, interval, limit):
        url = "https://api.binance.com/api/v3/klines"
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        async with session.get(url, params=params) as response:
            return await response.json()

    async def seven_days_old(self, session, symbol):
        try:
            # Fetch historical klines (candlesticks) data
            klines = await self.fetch_klines(session, symbol, '1d', 8)
            if klines:
                kline_start_time = klines[0][0]
                kline_start_dateTime = datetime.datetime.utcfromtimestamp(kline_start_time / 1000)
                print(f'{symbol}: First kline datetime: {kline_start_dateTime}')
                days_old = (datetime.datetime.utcnow() - kline_start_dateTime).days
                print(f'{symbol}: Days old: {days_old}')
                return days_old >= 7
            return False
        except Exception as e:
            print(f'Error fetching historical data for {symbol}: {e}')
            return False

    async def get_volume(self, session, symbol):
        try:
            klines = await self.fetch_klines(session, symbol, '1h', 2)
            return float(klines[-1][5]), float(klines[-2][5])  # Last and second last volume
        except Exception as e:
            print(f'Error fetching volume for {symbol}: {e}')
            return None, None

    async def scan_eligible_coins(self):
        async with aiohttp.ClientSession() as session:
            # Filter coins based on age
            tasks = [self.seven_days_old(session, ticker['symbol']) for ticker in usdt_tickers]
            results = await asyncio.gather(*tasks)
            for i, result in enumerate(results):
                if result:
                    self.eligible_coins.append(usdt_tickers[i]['symbol'])

            print(f'Eligible coins: {self.eligible_coins}')
            print(len(self.eligible_coins))

    async def scan_volume(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.get_volume(session, symbol) for symbol in self.eligible_coins]
            volumes = await asyncio.gather(*tasks)
            for i, (current_volume, previous_volume) in enumerate(volumes):
                if current_volume is not None and previous_volume is not None:
                    if current_volume > 3.0 * previous_volume:
                        if self.eligible_coins[i] not in self.results_without_duplication:
                            self.results_without_duplication.append(self.eligible_coins[i])
                            self.eligible_coin = self.eligible_coins[i]
                            print(self.eligible_coin)

