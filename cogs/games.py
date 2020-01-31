from api import get_player_info, get_player_id, get_players, get_games_today, get_games_results
from config import Config
from datetime import datetime as dt

import discord
from discord.ext import commands


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="results")
    async def results(self, ctx):

        await ctx.send(embed=results())

    @commands.command(name="games_today")
    async def games_today(self, ctx):

        await ctx.send(embed=games_today())


def setup(bot):
    bot.add_cog(Games(bot))


def suffix(d):
    return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')


def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))


def games_today():
    try:
        games_today = get_games_today()

        embed = discord.Embed(
            title=custom_strftime('**%B {S}, %Y**', dt.now()),  # Month_name DD, YYYY
            description='\u200b',
            color=discord.Color.blue()
        )

        for i in games_today:
            embed.add_field(name='{} @ {}'.format(i['VISITOR_TEAM'], i['HOME_TEAM']),
                            value='({}) - ({})'.format(i['VISITOR_TEAM_RECORD'], i['HOME_TEAM_RECORD']),
                            inline=False)

        return embed

    except Exception as e:
        print(e)


def results():
    try:
        results = get_games_results()

        embed = discord.Embed(
            title='Results for {}'.format(Config.YESTERDAY),
            description='\u200b',
            color=discord.Color.blue()
        )

        for i in results:
            embed.add_field(name='{} @ {}'.format(i['AWAY_TEAM'], i['HOME_TEAM']),
                            value='{} - {}'.format(i['AWAY_POINTS'], i['HOME_POINTS']),
                            inline=False)

        return embed

    except Exception as e:
        print(e)