from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()


class Config:

    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    BOT_COMMAND_PREFIX = '!'
    NBA_IMAGE_URL = 'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/'
    NBA_CURRENT_SEASON = '2018-19'
    YESTERDAY = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
