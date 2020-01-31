from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()


class Config:

    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    BOT_COMMAND_PREFIX = '-'
    NBA_IMAGE_URL = 'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/'
    NBA_CURRENT_SEASON = '2019-20'
    YESTERDAY = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

    team_emoji = {'Knicks': ':knicks:641277524076265472',
                  'Celtics': ':celtics:641280631728504852',
                  'Trail Blazers': ':blazers:641283281937104897',
                  'Lakers': ':lakers:641284090292862976',
                  'Raptors': ':raptors:641284160849444882',
                  'Pistons': ':pistons:641283441849008129',
                  'Bulls': ':bulls:641283298643017728',
                  'Nets': ':nets:641283365688967188',
                  'Mavericks': ':mavericks:641281835158077470',
                  'Rockets': ':rockets:641283387675508756',
                  'Grizzlies': ':grizzlies:641284032398622735',
                  'Pelicans': ':pelicans:641283423243206656',
                  'Nuggets': ':nuggets:641281932310741003',
                  'Bucks': ':bucks:641280570294534155',
                  'Thunder': ':thunder:641285545770614794',
                  'Suns': ':suns:641303412004225030'}
