import discord
from discord import Embed
from discord.ext import commands, tasks
from utils.utils_api import load_api_config
import http.client
import urllib.parse
import json

# Créer un package pour les tâches planifiées
# Tâche planifiée pour envoyer des mises à jour de nouvelles

def fetch_news(api_config):
    """
    Récupère les nouvelles à partir de l'API Mediastack.

    Parameters:
        api_config (dict): Configuration de l'API contenant la clé d'accès.

    Returns:
        list: Liste des informations sur les nouvelles.
    """
    try:
        # Connexion à l'API Mediastack
        conn = http.client.HTTPConnection('api.mediastack.com')
        params = urllib.parse.urlencode({
            'access_key': f"{api_config.get('key')}",
            'categories': 'technology, science',
            'languages': 'en',
            'sort': 'published_desc',
            'limit': "5"
        })
        conn.request('GET', '/v1/news?{}'.format(params))
        res = conn.getresponse()

        if res.status == 200:
            data = res.read()
            # Convertir les données JSON en un objet Python
            json_data = json.loads(data)
            print(data.decode('utf-8'))
            return json_data.get('data', [])
        else:
            print(f"La requête a échoué avec le code de statut : {res.status}")
            return []

    except ValueError as e:
        print(f"Erreur : {e}")

def build_news_embed(info):
    """
    Construit un objet Embed à partir des informations sur une nouvelle.

    Parameters:
        info (dict): Informations sur une nouvelle.

    Returns:
        Embed: Objet Embed pour une nouvelle.
    """
    embed = Embed(
        title=info['title'],
        description=info['description'],
        url=info['url'],
        colour=discord.Colour.blue()
    )
    embed.set_author(name=info["author"])
    embed.set_image(url=info["image"])
    embed.set_footer(text=f"Source: {info['source']} | Published at: {info['published_at']}")
    return embed

async def send_news(channel, news_data):
    """
    Envoie les nouvelles à un canal Discord.

    Parameters:
        channel (discord.TextChannel): Canal Discord où envoyer les nouvelles.
        news_data (list): Liste des informations sur les nouvelles.
    """
    for info in news_data:
        embed = build_news_embed(info)
        await channel.send(embed=embed)


@tasks.loop(minutes=30)
async def news_update_channel():
    """
    Tâche planifiée pour mettre à jour un canal Discord avec les dernières nouvelles.
    """
    try:
        # Charger la configuration de l'API Mediastack depuis le fichier de configuration
        api_config = await load_api_config('config.yml', 'MEDIASTACKS')
        if api_config is None:
            print(f"API Mediastacks not found in the config file.")
            return

        # Récupérer les nouvelles
        news_data = fetch_news(api_config)

        # Récupérer l'ID du canal Discord depuis la configuration
        channel_id = api_config.get('channel')
        channel = bot.get_channel(int(channel_id))

        # Envoyer les nouvelles au canal Discord
        await send_news(channel, news_data)

    except ValueError as e:
        print(f"Erreur : {e}")
