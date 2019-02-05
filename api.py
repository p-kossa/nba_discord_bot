from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd


def get_teams() -> list:
    """
    Uses nba_api to get_teams() and pop information we don't need.
    Returns a list of dictionaries with the following key/value pairs:
    'abbreviation', 'city', 'full_name', 'id', 'nickname'

    :return: list
    """
    all_teams = teams.get_teams()
    keys_to_pop = ['state', 'year_founded']

    for i in range(len(teams)):
        all_teams = {x: teams[i].pop(x) for x in keys_to_pop}

    return all_teams


def get_players() -> list:
    return players.get_players()


def get_player_stats(player_id: int):
    """
    Uses nba_api to get career stats for given player argument

    :param player_id:
    :return:
    """
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    return career.get_data_frames()[0]


def get_player_id(p: str) -> int:
    print(p)
    all_players = get_players()
    p = [player for player in all_players if player['full_name'] == p][0]

    return p['id']
