from api import get_player_info, get_player_id, get_players, get_games_today, get_games_results
from config import Config
from datetime import datetime as dt

import discord
from discord.ext import commands


def suffix(d):
    return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')


def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))


class Predictions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="predictions")
    async def post_predictions(self, ctx):
        games = get_games_today()

        date = custom_strftime('**%B {S}, %Y**', dt.now())
        await ctx.send(date)
        await ctx.send('================')

        for game in games:
            data = '\n\n**{} @ {}** \n({}) - ({})'.format(
                                     game['VISITOR_TEAM'], game['HOME_TEAM'],
                                     game['VISITOR_TEAM_RECORD'], game['HOME_TEAM_RECORD'])
            msg = await ctx.send(data)

            await msg.add_reaction(Config.team_emoji[game['VISITOR_TEAM']])
            await msg.add_reaction(Config.team_emoji[game['HOME_TEAM']])


def setup(bot):
    bot.add_cog(Predictions(bot))
