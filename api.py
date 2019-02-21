from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import playercareerstats, \
    commonplayerinfo, playerawards, scoreboard, \
    boxscoresummaryv2, teamdetails, leaguestandings, scoreboardv2, playerprofilev2
from objectpath import *
import json
from datetime import datetime, timedelta
from pprint import pprint
from config import Config

# to do: tip off times/final scores


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
    common = player_info_tree.execute("$.CommonPlayerInfo")
    headline = player_info_tree.execute("$.PlayerHeadlineStats")

    for i in range(len(common)):
        data = {
            'TEAM': common[i]['TEAM_CITY'] + ' ' + common[i]['TEAM_NAME'],
            'PLAYER_NAME': common[i]['DISPLAY_FIRST_LAST'],
            'SCHOOL': common[i]['SCHOOL'],
            'POS': common[i]['POSITION'],
            'YEARS_ACTIVE': common[i]['SEASON_EXP'],
            'HEIGHT': common[i]['HEIGHT'],
            'WEIGHT': common[i]['WEIGHT'],
            'YEAR_DRAFTED': common[i]['DRAFT_YEAR'],
            'DRAFT_RD': common[i]['DRAFT_ROUND'],
            'DRAFT_PICK': common[i]['DRAFT_NUMBER'],
            'CURRENT_SEASON': headline[i]['TimeFrame'],
            'PTS': headline[i]['PTS'],
            'AST': headline[i]['AST'],
            'REB': headline[i]['REB']
        }
        player.append(data)

    return player


def get_player_info_detailed(player_id: int) -> list:

    player = list()
    player_info = playerprofilev2.PlayerProfileV2(player_id=player_id)
    player_info_tree = Tree(json.loads(player_info.get_normalized_json()))
    career_highs = player_info_tree.execute("$.CareerHighs")

    if career_highs[0]['STAT'] == 'PTS':
        data = {
            'PTS': career_highs[0]['STAT_VALUE'],
            'DATE': career_highs[0]['GAME_DATE'],
            'OPP': career_highs[0]['VS_TEAM_NAME']
        }
    player.append(data)

    return player


def get_player_awards(player_id: int):
    pass


def get_games_today() -> list:
    """
    Gets list of game_ids for the current day

    :return: list of game_ids
    """
    games = scoreboardv2.ScoreboardV2()  # to do: option for game dates
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


def get_games_results() -> list:
    """
    Gets game results from given date (right now, only 'yesterday')

    :return: list of game results
    """
    games = scoreboardv2.ScoreboardV2(game_date=Config.YESTERDAY)
    games_tree = Tree(json.loads(games.get_normalized_json()))
    games_yesterday = games_tree.execute("$.LineScore")

    results = list()
    for i in range(0, len(games_yesterday), 2):
        data = {
            'AWAY_TEAM': games_yesterday[i]['TEAM_ABBREVIATION'],
            'AWAY_POINTS': games_yesterday[i]['PTS'],
            'HOME_TEAM': games_yesterday[i+1]['TEAM_ABBREVIATION'],
            'HOME_POINTS': games_yesterday[i+1]['PTS']
        }
        results.append(data)

    return results


def get_team_records() -> dict:
    """
    Gets current win/loss records for each team

    :return: dict of win/loss records for each team
    """
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
    """
    Gets a player_id for given player argument

    :param p: player name
    :return: player_id
    """
    all_players = get_players()
    p = [player for player in all_players if player['full_name'] == p][0]

    return p['id']
