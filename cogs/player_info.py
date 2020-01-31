from api import get_player_info, get_player_id, get_players, get_games_today, get_games_results
from config import Config

import discord
from discord.ext import commands


class PlayerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="player_info")
    async def hello(self, ctx, *args):

        await ctx.send(embed=player_info(args))


def setup(bot):
    bot.add_cog(PlayerInfo(bot))


def player_info(args):
    try:
        print(args)
        player = ' '.join(args)
        # to-do: mispelling player names returns 400, or names with special characters, i.e. Doncic
        try:
            player_id = get_player_id(player)
        except Exception as e:
            print("ERROR: {}".format(e))

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
