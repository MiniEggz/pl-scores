# contain methods used to pull data from FPL api.
from typing import List

import requests

from objects import Table

response = requests.get(url="https://fantasy.premierleague.com/api/bootstrap-static/")

# events looks like gameweeks
events = response.json().get("events")

# teams
teams = response.json().get("teams")


def strip_keys(dict_list: List[dict], key_whitelist: List[str]):
    """Strip back to only relevant team data.

    Args:
        dict_list (List[dict]): list of dicts to strip.
        key_whitelist (List[str]): list of keys that are relevant.

    Returns:
        List[dict]: stripped back list of dicts.
    """
    # get keys to remove
    remove_keys = [key for key in dict_list[0].keys() if key not in key_whitelist]

    # remove keys
    for dic in dict_list:
        for key in remove_keys:
            del dic[key]


def reset_stats(teams: List[dict]):
    """Set all points/goals to 0.

    Args:
        teams (List[dict]): list of teams to have stats added.
    """
    for team in teams:
        team["points"] = 0
        team["goals_for"] = 0
        team["goals_against"] = 0


# get all the team names
team_names = {team.get("name"): team.get("id") for team in teams}


team_points = [team.get("points") for team in teams]

# fixtures
fixtures = requests.get("https://fantasy.premierleague.com/api/fixtures/").json()

# element = player?
# element type 1, 2, 3, 4 == gk, def, mid, for
players = response.json().get("elements")
strip_keys(
    players,
    [
        "id",
        "first_name",
        "second_name",
        "goals_scored",
        "assists",
        "clean_sheets",
        "element_type",
    ],
)


def get_top_goals_scored(players: List[dict]) -> int:
    """Get the highest number of goals scored by a single player.

    Args:
        players (List[dict]): list of all players and their data.

    Returns:
        int: most goals scored by a single player.
    """
    most_goals = 0
    for player in players:
        if player["goals_scored"] > most_goals:
            most_goals = player["goals_scored"]
    return most_goals


def get_top_scorers(players: List[dict]) -> List[dict]:
    """Get list of top scorers.

    Args:
        players (List[dict]): list of all players and their data.

    Returns:
        List[dict]: list of all players that have the highest number of goals.
    """
    most_goals = get_top_goals_scored(players)
    return [player for player in players if player["goals_scored"] == most_goals]


def get_top_assists_number(players: List[dict]) -> int:
    """Get the highest number of assists made by a single player.

    Args:
        players (List[dict]): list of all players and their data.

    Returns:
        int: most assists made by a single player.
    """
    most_assists = 0
    for player in players:
        if player["assists"] > most_assists:
            most_assists = player["assists"]
    return most_assists


def get_top_assisters(players: List[dict]) -> List[dict]:
    """Get list of top assisters.

    Args:
        players (List[dict]): list of all players and their data.

    Returns:
        List[dict]: list of all players that have the highest number of assists.
    """
    most_assists = get_top_assists_number(players)
    return [player for player in players if player["assists"] == most_assists]


def get_most_clean_sheets_by_keeper(players: List[dict]) -> int:
    """Get the highest number of clean sheets by a single keeper.

    Args:
        players (List[dict]): list of all players and their data.

    Returns:
        int: highest number of clean sheets kepy by a keeper.
    """
    most_clean_sheets = 0
    for player in players:
        if player["element_type"] == 1 and player["clean_sheets"] > most_clean_sheets:
            most_clean_sheets = player["clean_sheets"]
    return most_clean_sheets


def get_keepers_with_most_clean_sheets(players: List[dict]) -> List[dict]:
    """Get the keepers with the most clean sheets.

    Args:
        players (List[dict]): list of all players and their data.

    Returns:
        List[dict]: list of all keepers with highest number of clean sheets.
    """

    most_clean_sheets = get_most_clean_sheets_by_keeper(players)
    return [
        player
        for player in players
        if player["clean_sheets"] == most_clean_sheets and player["element_type"] == 1
    ]


def rip_player_names(players: List[dict]) -> List[str]:
    """Get list of player names from player dictionary.

    Args:
        players (List[dict]): list of all players and their data.

    Returns:
        List[str]: list of player names.
    """
    return [f"{player['first_name']} {player['second_name']}" for player in players]


# premier league website and fpl use different names for teams...
team_points = [0 for i in range(20)]
strip_keys(teams, ["id", "name", "short_name"])
reset_stats(teams)

for fixture in fixtures:
    try:
        # update home team goals for/against
        teams[fixture["team_h"] - 1]["goals_for"] += fixture["team_h_score"]
        teams[fixture["team_h"] - 1]["goals_against"] += fixture["team_a_score"]
        # update away team goals for/against
        teams[fixture["team_a"] - 1]["goals_for"] += fixture["team_a_score"]
        teams[fixture["team_a"] - 1]["goals_against"] += fixture["team_h_score"]

        if fixture["team_h_score"] > fixture["team_a_score"]:
            teams[fixture["team_h"] - 1]["points"] += 3
        elif fixture["team_h_score"] < fixture["team_a_score"]:
            teams[fixture["team_a"] - 1]["points"] += 3
        else:
            teams[fixture["team_h"] - 1]["points"] += 1
            teams[fixture["team_a"] - 1]["points"] += 1
    except TypeError:
        pass

# calculate goal difference for each team
for team in teams:
    team["goal_difference"] = team["goals_for"] - team["goals_against"]


league_table = Table(teams)
league_table.display_table()

print(f"Top goal scorer(s) with {get_top_goals_scored(players)} goal(s): ")
for player_name in rip_player_names(get_top_scorers(players)):
    print("\t" + player_name)

print(f"Top assister(s) with {get_top_assists_number(players)} assist(s):")
for player_name in rip_player_names(get_top_assisters(players)):
    print("\t" + player_name)

print(
    f"Keeper(s) with the most clean sheets with {get_most_clean_sheets_by_keeper(players)} clean sheet(s):"
)
for keeper_name in rip_player_names(get_keepers_with_most_clean_sheets(players)):
    print("\t" + keeper_name)
