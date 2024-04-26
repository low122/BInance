import pandas as pd
from dotenv import load_dotenv
import os
from binance.client import Client
import requests
import json

load_dotenv() # read file from local .env

api_key = 'NQbQTdz3KpUDvbGau9ranZUS7LxogPwuKERQ0Lf822OccIwzBdWXdzhSah9UApTG'
api_secret = 'XSbXZPnIl4K6lolkjc9dN0PCvRyS9JFgJCKx0bsXQUhV6PnqRP77bOh1eS7UNM3e'

client = Client(api_key=api_key, api_secret=api_secret, testnet=True)

# tickers = client.get_all_tickers()

# df = pd.DataFrame(tickers)
# df.head()

### Creating GET request
url = 'https://api1.binance.com'
api_call = '/api/v3/ticker/price'
headers = {'X-MBX-APIKEY': api_key}

response = requests.get(url + api_call, headers=headers)
response = json.loads(response.text) # convert json into python
# print(response)

df = pd.DataFrame(response)
print(df.head())


### General Request (ping)
client.ping()