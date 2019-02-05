from api import *
from pprint import pprint

id = 76003
data = get_player_stats(id)

player = 'Tim Duncan'
id = get_player_id(player)
print(id)
