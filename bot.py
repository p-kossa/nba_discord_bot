from config import Config

import discord
from discord.ext import commands

import logging
import sys, traceback

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


def get_prefix(bot, message):
    prefixes = ['-']

    if not message.guild:
        return '?'

    return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = ['cogs.commands',
                      'cogs.player_info',
                      'cogs.games',
                      'cogs.predictions']

bot = commands.Bot(command_prefix=get_prefix, description='r/nba discord bot v2')

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()


@bot.event
async def on_ready():
    print(f'\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    await bot.change_presence(activity=discord.Game(name='as nooky'))
    print(f'Successfully logged in and booted...!')


bot.run(Config.DISCORD_TOKEN, bot=True, reconnect=True)
