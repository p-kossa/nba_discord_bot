from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import playercareerstats, \
    commonplayerinfo, playerawards, scoreboard, \
    boxscoresummaryv2, teamdetails, leaguestandings
from objectpath import *
import json
from pprint import pprint
from config import Config


def get_teams() -> list:
    """
    Uses nba_api to get_teams() and pop information we don't need.
    Returns a list of dictionaries with the following key/value pairs:
    'abbreviation', 'city', 'full_name', 'id', 'nickname'

    :return: list
    """
    all_teams = teams.get_teams()

    return all_teams


def get_players() -> list:
    """
    Uses nba_api to get all NBA players

    :return: list of players and detailed data
    """
    return players.get_players()


def get_player_info(player_id: int) -> list:
    """
    Uses nba_api to get career stats for given player argument

    :param player_id: Player id from nba_api
    :return: list of a single dictionary with player information
    """
    # to-do: shooting pct%, team colors for embed

    player = list()
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    player_info_tree = Tree(json.loads(player_info.get_normalized_json()))
    player_info_tree_top = player_info_tree.execute("$.CommonPlayerInfo")
    player_info_tree_top_two = player_info_tree.execute("$.PlayerHeadlineStats")
    for i in range(len(player_info_tree_top)):
        data = {
            'TEAM': player_info_tree_top[i]['TEAM_CITY'] + ' ' + player_info_tree_top[i]['TEAM_NAME'],
            'PLAYER_NAME': player_info_tree_top[i]['DISPLAY_FIRST_LAST'],
            'SCHOOL': player_info_tree_top[i]['SCHOOL'],
            'POS': player_info_tree_top[i]['POSITION'],
            'YEARS_ACTIVE': player_info_tree_top[i]['SEASON_EXP'],
            'HEIGHT': player_info_tree_top[i]['HEIGHT'],
            'WEIGHT': player_info_tree_top[i]['WEIGHT'],
            'YEAR_DRAFTED': player_info_tree_top[i]['DRAFT_YEAR'],
            'DRAFT_RD': player_info_tree_top[i]['DRAFT_ROUND'],
            'DRAFT_PICK': player_info_tree_top[i]['DRAFT_NUMBER'],
            'CURRENT_SEASON': player_info_tree_top_two[i]['TimeFrame'],
            'PTS': player_info_tree_top_two[i]['PTS'],
            'AST': player_info_tree_top_two[i]['AST'],
            'REB': player_info_tree_top_two[i]['REB']
        }
        player.append(data)

    return player


def get_games_today() -> list:
    """
    Gets list of game_ids for the current day

    :return: list of game_ids
    """
    games = scoreboard.Scoreboard()
    games_tree = Tree(json.loads(games.get_normalized_json()))
    games_today = games_tree.execute("$.LastMeeting")

    games_today_teams = list()
    team_records = get_team_records()
    for i in range(len(games_today)):
        data = {
            'HOME_TEAM': games_today[i]['LAST_GAME_HOME_TEAM_NAME'],
            'VISITOR_TEAM': games_today[i]['LAST_GAME_VISITOR_TEAM_NAME'],
            'HOME_TEAM_RECORD': team_records[games_today[i]['LAST_GAME_HOME_TEAM_NAME']],
            'VISITOR_TEAM_RECORD': team_records[games_today[i]['LAST_GAME_VISITOR_TEAM_NAME']]
        }
        games_today_teams.append(data)

    return games_today_teams


def get_team_records() -> dict:
    team_records = leaguestandings.LeagueStandings(season=Config.NBA_CURRENT_SEASON, season_type='Regular Season')
    team_records_tree = Tree(json.loads(team_records.get_normalized_json()))
    team_records = team_records_tree.execute("$.Standings")

    data = dict()
    for i in range(len(team_records)):
        data[team_records_tree.execute("$.Standings[{}].TeamName".format(i))] = \
            team_records_tree.execute("$.Standings[{}].Record".format(i))

    return data


def get_standings():
    pass


def get_player_id(p: str) -> int:
    all_players = get_players()
    p = [player for player in all_players if player['full_name'] == p][0]

    return p['id']
