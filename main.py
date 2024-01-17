import discord 
from discord.ext import commands, tasks
import aiohttp
import requests
import asyncio
from asyncio import Queue, run_coroutine_threadsafe
import ollama
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
from utils.utils_api import load_api_config
from modules.news_feed import news_update_channel
import modules.bot_command as bot_command
from modules.ft_api_manager import test42
from modules.intra import ic

#Creer une fonction qui va chercher les clés d'API dans le fichier config.json/ config.yml
discord_api = load_api_config('config/config.yml', 'DISCORD')
if discord_api:
    TOKEN = discord_api.get('key')
else:
    print("Configuration for Discord not found or an error occurred while loading the configuration.")

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
    # new_update_channel.start()

async def chat_wrapper(queue, model, messages, stream):
    async for part in ollama.chat(model=model, messages=messages, stream=stream):
        print(part['message']['content'], end='', flush=True)
        await queue.put(part)

def process_ollama_messages(user_message):
    response_content = ''
    for part in ollama.chat(model='mistral', messages=[user_message], stream=True):
        response_content += part['message']['content']
    return response_content

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return # Ignore messages from the bot itself
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
    else:
        user_message = {'role': 'user', 'content': message.content}

        # Découpage de l'opération pour éviter un blocage prolongé
        response_content = process_ollama_messages(user_message)

        # Utiliser message.channel au lieu de user_message pour envoyer le message dans le canal Discord
        await message.channel.send(response_content)

# @bot.command(name='test42', help='NONE')
# async def test42_command(ctx):
#     """Test the 42 API."""
#     Filter by campus in specified range of updated_at
#     payload = {
#         "filter[campus_id]": 13,
#         "range[updated_at]":"2019-01-01T00:00:00.000Z,2020-01-01T00:00:00.000Z"
#     }

#     GET campus_users of specified campus in range
#     response = ic.get("campus_users", params=payload)
#     if response.status_code == 200: 
#         data = response.json()

#     for user in data:
#         print(user)

@bot.event
async def on_command_error(ctx, error):
    await bot_command.on_command_error(ctx, error)


@bot.command(name='end', hidden=True)
async def shutdown_command(ctx):
    """Shutdown the bot using the imported shutdown function."""
    await bot_command.shutdown(ctx, bot)

@bot.command(name='hello', help='Responds with hello!')
async def hello_command(ctx):
    """Respond to the hello command."""
    await bot_command.hello(ctx)

@bot.command(name='ping', help='Responds with pong!')
async def ping_command(ctx):
    """Respond to the ping command."""
    await bot_command.ping(ctx)

bot.run(TOKEN)