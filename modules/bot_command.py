import discord
from utils.utils_api import load_api_config
from discord.ext import commands, tasks
from modules.news_feed import news_update_channel



async def shutdown(ctx, bot):
    """Shutdown the bot.

    This function sends a 'Shutting down...' message to the Discord channel
    from which the command was invoked and then closes the bot.

    Args:
        ctx (commands.Context): The context object representing the invocation.

    Returns:
        None
    """

    ID = load_api_config('config/config.yml', 'DISCORD').get('ID')
    # Sending a message to indicate that the bot is shutting down
    if ctx.author.id == ID:
        print("Commande de déconnexion reçue. Déconnexion du bot...")
        await ctx.send("Shutting down...")
        # Stopping any ongoing processes, if needed (commented out in this example)
        # new_update_channel.stop()
        # Closing the bot
        await bot.close()
    else:
        print("Tentative non autorisée de déconnexion par un utilisateur non autorisé.")
        await ctx.send("You are not authorized to use this command.")


async def on_command_error(ctx, error):
    """
    Gère les erreurs lors de l'exécution d'une commande.

    Args:
        ctx (commands.Context): Le contexte de la commande.
        error (Exception): L'erreur qui s'est produite.

    Returns:
        None
    """
    if isinstance(error, commands.CommandNotFound):
        # Si la commande n'est pas trouvée, informez l'utilisateur.
        await ctx.send("Command not found. Type `$help` for a list of available commands.")
    else:
        # Gérer d'autres erreurs si nécessaire
        print(f"An error occurred: {error}")


async def hello(ctx):
    await ctx.send('Hello!')

async def ping(ctx):
    await ctx.send('pong')