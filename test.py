from api import *
from pprint import pprint

player = 'LeBron James'
id = get_player_id(player)
awards = get_player_awards(id)

pprint(awards)


"""
TO DO: 

search player function in case of typos

"""