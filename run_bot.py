from config import Config
from api import get_player_info, get_player_id, get_players
import discord
import requests
import json
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class CommandHandler:

    def __init__(self, client):
        self.client = client
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def command_handler(self, message):
        for command in self.commands:
            if message.content.startswith(command['trigger']):
                args = message.content.split(' ')
                if args[0] == command['trigger']:
                    args.pop(0)
                    if command['args_num'] == 0:
                        return self.client.send_message(
                            message.channel,
                            str(command['function'](message, self.client, args)))
                        break
                    else:
                        if len(args) >= command['args_num']:
                            return self.client.send_message(
                                message.channel,
                                str(command['function'](message, self.client, args))
                            )
                            break
                        else:
                            return self.client.send_message(
                                message.channel,
                                'command "{}" requires {} argument(s) "{}"'.format(command['trigger'],
                                command['args_num'], ', '.join(command['args_name']))
                            )
                            break
                else:
                    break

    def embed_handler(self, message, title, description, color, text):
        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )

        embed.set_footer(text=text)

        return self.client.send_message(message.channel, embed=embed)


client = discord.Client()
token = Config.DISCORD_TOKEN

ch = CommandHandler(client)


def commands_command(message, client, args):
    try:
        count = 1
        coms = '**Commands List**\n'
        for command in ch.commands:
            coms += '{}.) {} : {}\n'.format(count, command['trigger'], command['description'])
            count += 1
        return coms
    except Exception as e:
        print(e)


ch.add_command({
    'trigger': '!commands',
    'function': commands_command,
    'args_num': 0,
    'args_name': [],
    'description': 'Prints a list of all the commands.'
})


def player_info_command(message, client, args):
    """
    Displays basic player information in Discord server

    :param message:
    :param client:
    :param args:
    :return: Discord message
    """
    try:
        player = ' '.join(args)
        player_id = get_player_id(player)
        info = get_player_info(player_id)

        template = 'Name: {}\n' \
                   'Team: {}\n' \
                   'College/Country: {}\n' \
                   '{} season stats: {} PTS - {} REB - {} AST\n' \
                   'Position: {}\n' \
                   'Years active: {}\n' \
                   'Height: {}\n' \
                   'Year drafted: {}\n'

        out = template.format(info['player_name'],
                              info['team'],
                              info['college'],
                              info['current_season'],
                              info['points'],
                              info['rebounds'],
                              info['assists'],
                              info['position'],
                              info['years_active'],
                              info['height'],
                              info['year_drafted'])

        return out
    except Exception as e:
        print(e)


ch.add_command({
    'trigger': '!player_info',
    'function': player_info_command,
    'args_num': 2,
    'args_name': ['FirstName LastName'],
    'description': 'Basic player information'
})


def embed(message, client, args):
    try:
        embed = discord.Embed(
            title='Title',
            description='Embed test',
            color=discord.Color.blue()
        )

        embed.set_footer(text='This is a footer')
        embed.add_field(name='Field name', value='Field value', inline=False)
        embed.add_field(name='field name 2', value='value 2', inline=True)
        embed.add_field(name='name 3', value='value 3', inline=True)

        return embed
    except Exception as e:
        print(e)


ch.add_command({
    'trigger': '!embed',
    'function': embed,
    'args_num': 0,
    'args_name': [],
    'description': 'Embed testing'
})


@client.event
async def on_ready():
    try:
        print(client.user.name)
        print(client.user.id)
    except Exception as e:
        print(e)


@client.event
async def on_message(message):
    # if the message is from the bot itself ignore it
    if message.author == client.user:
        pass
    else:
        # try to evaluate with the command handler
        try:
            await ch.command_handler(message)
        # message doesn't contain a command trigger
        except TypeError as e:
            pass
        # generic python error
        except Exception as e:
            print(e)


client.run(token)
