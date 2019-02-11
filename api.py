from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo, playerawards
from objectpath import *
import json
from pprint import pprint


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
    """
    Uses nba_api to get all NBA players

    :return: list of players and detailed data
    """
    return players.get_players()


def get_player_info(player_id: int) -> dict:
    """
    Uses nba_api to get career stats for given player argument

    :param player_id:
    :return:
    """
    data = dict()
    career = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    pprint(json.loads(career.get_normalized_json()))
    career_tree = Tree(json.loads(career.get_normalized_json()))
    team_city = career_tree.execute("$.CommonPlayerInfo[0].TEAM_CITY")
    team_name = career_tree.execute("$.CommonPlayerInfo[0].TEAM_NAME")
    data['team'] = team_city + ' ' + team_name
    data['player_name'] = career_tree.execute("$.CommonPlayerInfo[0].DISPLAY_FIRST_LAST")
    data['college'] = career_tree.execute("$.CommonPlayerInfo[0].SCHOOL")
    data['current_season'] = career_tree.execute("$.PlayerHeadlineStats[0].TimeFrame")
    data['points'] = career_tree.execute("$.PlayerHeadlineStats[0].PTS")
    data['assists'] = career_tree.execute("$.PlayerHeadlineStats[0].AST")
    data['rebounds'] = career_tree.execute("$.PlayerHeadlineStats[0].REB")
    data['position'] = career_tree.execute("$.CommonPlayerInfo[0].POSITION")
    data['years_active'] = career_tree.execute("$.CommonPlayerInfo[0].SEASON_EXP")
    data['height'] = career_tree.execute("$.CommonPlayerInfo[0].HEIGHT")
    data['year_drafted'] = career_tree.execute("$.CommonPlayerInfo[0].DRAFT_YEAR")

    return data


def get_games_today():
    pass


def get_standings():
    pass


def get_player_awards(player_id: int) -> dict:
    data = dict()
    awards = playerawards.PlayerAwards(player_id=player_id)
    pprint(json.loads(awards.get_normalized_json()))


def get_player_id(p: str) -> int:
    all_players = get_players()
    p = [player for player in all_players if player['full_name'] == p][0]

    return p['id']
