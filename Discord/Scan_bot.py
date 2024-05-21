import asyncio
import discord
import os
from dotenv import load_dotenv
import logging
from Binance.Scan import Scan_api

load_dotenv('/Users/lowjiatzin/Desktop/myProject/KEY.env')

DISCORD_API = os.getenv('DISCORD_TOKEN_SCANBOT')

intents = discord.Intents.all()
intents.messages = True

client = discord.Client(intents=intents)
logging.basicConfig(level=logging.INFO)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    
    latest_coins = []
    
    if message.content.startswith('!'):
        if message.content.startswith('!scan'):
            await message.channel.send('Scanning.....')
            scan = Scan_api()
            await scan.scan_eligible_coins()
            while True:
                await scan.scan_volume()

                for result in scan.results_without_duplication:
                    if result not in latest_coins:
                        latest_coins.append(result)
                        await message.channel.send(f'Coin {result} has increased 300% volume in the last hour')

                await asyncio.sleep(120)

            # if scan.eligible_coin:
            #     await message.channel.send(f'Coin {scan.eligible_coin} has increased volume in the last hour')
            # else:
            #     await message.channel.send('No coin met the criteria during this scan.')


client.run(DISCORD_API)
