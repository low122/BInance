import asyncio
import pandas as pd
from tradingview_ta import TA_Handler, Exchange, Interval
from lightweight_charts import Chart
from tvDatafeed import TvDatafeed, Interval
from fmp_python.fmp import FMP
import os

USERNAME = os.getenv('USER_NAME_TRADINGVIEW')
PASSWORD = os.getenv('USER_PASSWORD_TRADINGVIEW')
API = os.getenv('TRADINGVIEW_API')

tv = TvDatafeed(USERNAME, PASSWORD)
fmp = FMP(api_key=API)

class TradingViewDataFeed:

    def __init__(self, symbol, exchange):
        self._symbol = symbol
        self._exchange = exchange


    def get_historical_peak(self) -> float:
        btc_data = tv.get_hist(symbol=self._symbol,exchange=self._exchange,interval=Interval.in_monthly,n_bars=1000)

        previous_peak_high = max(map(float, btc_data['high']))
        return previous_peak_high