from config import Config
from api import get_player_info, get_player_id, get_players, get_games_today
import discord
from datetime import datetime as dt
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')


def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))


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
                    if command['args_num'] == 0 or len(args) >= command['args_num']:
                        if command['is_embed'] is True:
                            return self.client.send_message(message.channel,
                                                            embed=command['function'](message, self.client, args))
                            break
                        else:
                            return self.client.send_message(message.channel,
                                                            str(command['function'](message, self.client, args)))
                    else:
                        return self.client.send_message(
                            message.channel,
                            'command "{}" requires {} argument(s) "{}"'.format(command['trigger'],
                            command['args_num'], ', '.join(command['args_name'])))
                        break
                else:
                    break


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
    'description': 'Prints a list of all the commands.',
    'is_embed': False
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
        # to-do: mispelling player names returns 400, need to add something for this
        try:
            player_id = get_player_id(player)
        except Exception as e:
            print("hello {}".format(e))

        info = get_player_info(player_id)

        embed = discord.Embed(
            title='**{}**'.format(info[0]['PLAYER_NAME']),
            description='{} - {}'.format(info[0]['TEAM'], info[0]['POS']),
            color=discord.Color.blue()  # to-do: add functionality for color based on teams
        )

        embed.add_field(name='{} Statistics (PTS/REB/AST):'.format(info[0]['CURRENT_SEASON']),
                        value='{}/{}/{}'.format(info[0]['PTS'], info[0]['REB'], info[0]['AST']),
                        inline=False)
        embed.add_field(name='Height/Weight:', value='{} - {} lbs'.format(info[0]['HEIGHT'], info[0]['WEIGHT']))
        embed.add_field(name='School/Country:', value=info[0]['SCHOOL'], inline=False)
        embed.add_field(name='Year Drafted:',
                        value='{} - Rd: {} Pick: {}'.format(info[0]['YEAR_DRAFTED'],
                                                            info[0]['DRAFT_RD'],
                                                            info[0]['DRAFT_PICK']))
        embed.add_field(name='Years Active:', value=info[0]['YEARS_ACTIVE'])
        embed.set_thumbnail(url=Config.NBA_IMAGE_URL + '{}.png'.format(player_id))

        return embed

    except Exception as e:
        print(e)


ch.add_command({
    'trigger': '!player_info',
    'function': player_info_command,
    'args_num': 2,
    'args_name': ['FirstName LastName'],
    'description': 'Basic player information',
    'is_embed': True
})


def games_today_command(message, client, args):
    try:
        games_today = get_games_today()

        embed = discord.Embed(
            title=custom_strftime('**%B {S}, %Y**', dt.now()),  # Month_name DD, YYYY
            description='\u200b',  # zero width space
            color=discord.Color.blue()
        )

        for i in games_today:
            embed.add_field(name='{} @ {}'.format(i['VISITOR_TEAM'], i['HOME_TEAM']),
                            value='({}) - ({})'.format(i['VISITOR_TEAM_RECORD'], i['HOME_TEAM_RECORD']),
                            inline=False)

        return embed

    except Exception as e:
        print(e)


ch.add_command({
    'trigger': '!games',
    'function': games_today_command,
    'args_num': 0,
    'args_name': [],
    'description': 'Lists today\'s scheduled games',
    'is_embed': True
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
    if message.author == client.user:
        pass
    else:
        try:
            await ch.command_handler(message)
        except TypeError as e:
            pass
        except Exception as e:
            print(e)


client.run(token)
