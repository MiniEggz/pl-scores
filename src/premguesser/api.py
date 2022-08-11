# contain methods used to pull data from FPL api.
from typing import List

import requests

from objects import AllPlayers, Player, Table

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
players_response = response.json().get("elements")
players = AllPlayers(players_response)


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


print(f"Top goal scorer(s) with {players.get_top_goals_scored()} goal(s): ")
for player in players.get_top_scorers():
    print("\t" + player.name)

print(f"Top assister(s) with {players.get_top_assists_number()} assist(s):")
for player in players.get_top_assisters():
    print("\t" + player.name)

print(
    f"Keeper(s) with the most clean sheets with {players.get_top_assists_number()} clean sheet(s):"
)
for keeper in players.get_keepers_with_most_clean_sheets():
    print("\t" + keeper.name)
