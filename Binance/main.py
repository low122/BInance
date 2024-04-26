from Binance_api import BinanceTrade

if __name__ == '__main__':
    symbol = 'btcusdt'
    ws_client = BinanceTrade(symbol)
    ws_client.run()