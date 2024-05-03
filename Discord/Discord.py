import discord
import os
from dotenv import load_dotenv
import logging
from Binance.Binance_api import BinanceTrade

load_dotenv('/Users/lowjiatzin/Desktop/myProject/KEY.env')

DISCORD_API = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.messages = True

client = discord.Client(intents=intents)
logging.basicConfig(level=logging.INFO)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message: discord.Message):

    SYMBOL = message.content

    if message.author == client.user:
        return
    
    if "usdt" in SYMBOL:
        if SYMBOL.endswith('usdt'):
            bt = BinanceTrade(SYMBOL.upper())
            bt.run()
            embed = discord.Embed(title='Peak Notification (USDT)', description='track peak', color=0x00ff00)
            embed.add_field(name=SYMBOL.upper(), value=f'${bt.curr_mkt_price}', inline=False)
            embed.add_field(name='Time(UTC): ', value=f'{bt.getEventTime()}', inline=False)
            await message.channel.send(embed=embed)
    else:
        await message.channel.send('Only USDT available for current version')




client.run(DISCORD_API)