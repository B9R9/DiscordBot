import discord 
from discord.ext import commands, tasks
import aiohttp
import requests
import asyncio
import json
from datetime import datetime, timedelta

TOKEN = "MTE4MjM3NDY1MzE3NjU5NDU5NQ.GKaNyf.S_ag4GsMbCGrKqNGmc2E8C3D6BL06Ng0_SdXOk"

# Définissez les intentions appropriées
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.reactions = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():    
    print(f'Logged in as: {bot.user.name} (ID: {bot.user.id})')
    print('------ Servers and Channels ------')
    
    for server in bot.guilds:
        print(f'\nServer: {server.name} (ID: {server.id})')
        for channel in server.channels:
            print(f'  Channel: {channel.name} (ID: {channel.id}, Type: {channel.type})')
    
    print('----------------------------------')
    new_update_channel.start()

async def get_api_keys(api_name):
    with open('/Users/briffard/Desktop/testAPibard/testBot/config.json') as config_file:
        config_data = json.load(config_file)

    for api_info in config_data:
        if api_info['name'] == api_name:
            return api_info
    print(f"API '{api_name}' not found in the config file.")
    return None

@tasks.loop(minutes=1)
async def new_update_channel():
    api_name = "NYT_API"
    try:
        api = await get_api_keys(api_name)
        if api is None:
            print(f"API '{api_name}' not found in the config file.")
            return
        keywords = ['IA', 'Technologie']
        # Période n'excédant pas trois mois
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        if api:
            channel_id = api['channel_id']
            url = f"{api['url']}?api-key={api['key']}&q={' OR '.join(keywords)}&begin_date={start_date.strftime('%Y%m%d')}&end_date={end_date.strftime('%Y%m%d')}"
            #url = f"{api['url']}?fq=Technology&fq={filter}&api-key={api['key']}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        for article in data.get('response', {}).get('docs', []):
                            title = article.get('abstract', '')
                            url = article.get('web_url', '')
                            await bot.get_channel(int(channel_id)).send(f"Titre: {title}\nURL: {url}\n")
                    else:
                        print(f"Erreur lors de la requête à l'API. Code de statut : {response.status}")
    except ValueError as e:
        print(f"Erreur : {e}")
    
@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command(name='end', hidden=True)
async def shutdown(ctx):
    """Shutdown the bot."""
    await ctx.send("Shutting down...")
    new_update_channel.stop()
    await bot.close()

bot.run(TOKEN)

