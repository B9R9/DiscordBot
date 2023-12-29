import discord 
from discord.ext import commands, tasks
from discord import Embed
import aiohttp
import requests
import asyncio
import json
from datetime import datetime, timedelta
import http.client,urllib.parse
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

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
    #new_update_channel.start()

async def get_api_keys(api_name):
    with open('.config.json') as config_file:
        config_data = json.load(config_file)

    for api_info in config_data:
        if api_info['name'] == api_name:
            return api_info
    print(f"API '{api_name}' not found in the config file.")
    return None

# @tasks.loop(minutes=30)
# async def new_update_channel():
#     api_name = "MEDIASTACKS_API"
#     try:
#         api = await get_api_keys(api_name)
#         if api is None:
#             print(f"API '{api_name}' not found in the config file.")
#             return
#         keywords = ['IA', 'Technologie']
#         # Période n'excédant pas trois mois
#         end_date = datetime.now()
#         start_date = end_date - timedelta(days=90)
#         if api:
#             channel_id = api['channel_id']
#             conn = http.client.HTTPConnection('api.mediastack.com')
#             params = urllib.parse.urlencode ({
#             'access_key': f"{api['key']}",
#             'categories': 'technology, science',
#             'languages': 'en',
#             'sort': 'published_desc',
#             'limit': "5"     
#             })
#             conn.request('GET', '/v1/news?{}'.format(params))
#             res = conn.getresponse()
#             if res.status == 200:
#                 data = res.read()
#                 # Convertir les données JSON en un objet Python
#                 json_data = json.loads(data)
#                 channel_id = api['channel_id']
#                 channel = bot.get_channel(int(channel_id))
#                 for info in json_data['data']:
#                     embed = Embed(
#                         title = info['title'],
#                         description = info['description'],
#                         url = info['url'],
#                         colour = discord.Colour.blue()
#                     )
#                     embed.set_author(name=info["author"])
#                     embed.set_image(url=info["image"])
#                     embed.set_footer(text=f"Source: {info['source']} | Published at: {info['published_at']}")
#                     await channel.send(embed=embed)
#                 print(data.decode('utf-8'))
#             else:
#                 print(f"La requête a échoué avec le code de statut : {res.status}")
#             conn.close()
#     except ValueError as e:
#         print(f"Erreur : {e}")
    
@bot.command(help='Responds with hello!')
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command(help='Responds with pong!')
async def ping(ctx):
    await ctx.send('pong')

@bot.command(name='whoisoncampus', help='Get a list of users present on the campus')
async def who_is_on_campus(ctx):
    # Configuration de l'API 42
    API_BASE_URL = 'https://api.intra.42.fr'
    UID = 'u-s4t2ud-7f180e4d5901b1f75047caac1a1119057519a9a3e0dc60b0204abed85b33840d'
    SECRET = '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'
    YOUR_CAMPUS_ID = '29'


    client = OAuth2Session(client_id=UID, client_secret=SECRET, token_endpoint_auth_method='client_secret_post')
    token_url = f'{API_BASE_URL}/oauth/token'
    # auth = HTTPBasicAuth(UID, SECRET)

    # Configuration pour le flux client credentials
    # token = client.fetch_token(token_url=token_url, auth=auth)
    # ACCESS_TOKEN = token['access_token']

    # Utiliser le jeton pour faire une requête à l'API
    response = client.get(f'{API_BASE_URL}/v2/cursus')
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f'Error: {response.status_code}')
    # # Utilisez le jeton pour faire des requêtes à l'API
    # response = client.get(f'{API_BASE_URL}/v2/campus')
    # if response.status_code == 200:
    #     data = response.json()
    #     print(data)
    # else:
    #     print(f'Error: {response.status_code}')

    # # Appel de l'API 42 pour obtenir la liste des utilisateurs présents sur le campus
    # headers = {'Authorization': f'Bearer {API_TOKEN}'}
    # response = requests.get(f'{API_BASE_URL}/v2/campus/{YOUR_CAMPUS_ID}/locations', headers=headers)

    # if response.status_code == 200:
    #     data = response.json()
    #     users_on_campus = [user['user']['login'] for user in data]
    #     await ctx.send(f'Users on campus: {", ".join(users_on_campus)}')
    # else:
    #     await ctx.send('Error fetching data from 42 API')

@bot.command(name='end', hidden=True)
async def shutdown(ctx):
    """Shutdown the bot."""
    await ctx.send("Shutting down...")
    #new_update_channel.stop()
    await bot.close()

bot.run(TOKEN)



            # url = f"{api['url']}?api-key={api['key']}&q={' OR '.join(keywords)}&begin_date={start_date.strftime('%Y%m%d')}&end_date={end_date.strftime('%Y%m%d')}"
            #url = f"{api['url']}?fq=Technology&fq={filter}&api-key={api['key']}"
            # async with aiohttp.ClientSession() as session:
            #     async with session.get(url) as response:
            #         if response.status == 200:
            #             data = await response.json()
            #             for article in data.get('response', {}).get('docs', []):
            #                 title = article.get('abstract', '')
            #                 url = article.get('web_url', '')
            #                 await bot.get_channel(int(channel_id)).send(f"Titre: {title}\nURL: {url}\n")
            #         else:
            #             print(f"Erreur lors de la requête à l'API. Code de statut : {response.status}")