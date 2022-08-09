# contain methods used to pull data from FPL api.
from typing import List

import requests
from functools import cmp_to_key

response = requests.get(url="https://fantasy.premierleague.com/api/bootstrap-static/")

# events looks like gameweeks
events = response.json().get("events")
# print(events[0])

# teams
teams = response.json().get("teams")
# print(teams[0])


def strip_teams(teams: List[dict], key_whitelist: List[str]):
    """Strip back to only relevant team data.

    Args:
        teams (List[dict]): list of team's data.
        key_whitelist (List[str]): list of keys that are relevant.

    Returns:
        List[dict]: stripped back team data.
    """
    # get keys to remove
    remove_keys = []
    for key in teams[0].keys():
        if key not in key_whitelist:
            remove_keys.append(key)

    # remove keys
    for team in teams:
        for key in remove_keys:
            del team[key]


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
# print(team_names)


team_points = [team.get("points") for team in teams]
# print(team_points)

# fixtures
fixtures = requests.get("https://fantasy.premierleague.com/api/fixtures/").json()
# print(f_response[0])

# element = player?
el_response = requests.get("https://fantasy.premierleague.com/api/element-summary/2/")
# print(el_response.json().get("history"))

# might have to do some webscraping...
# class="tableDark"
# data-filtered-table-row-name="Team Name"
# this is all inside <tbody class="tableBodyContainer isPL"

# premier league website and fpl use different names for teams...
team_points = [0 for i in range(20)]

strip_teams(teams, ["id", "name"])
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


class Table:
    def __init__(self, teams):
        self.teams = teams.copy()

    def get_table(self):
        """Get the current table."""
        # for i in range (1, len(teams)):
        #     for j, team in enumerate(teams):

        return sorted(self.teams, key=cmp_to_key(self._compare))

    @staticmethod
    def _compare(team1, team2):
        # compare points
        if team1["points"] < team2["points"]:
            return 1
        elif team1["points"] > team2["points"]:
            return -1
        else:
            # compare goal difference
            if team1["goal_difference"] < team2["goal_difference"]:
                return 1
            elif team1["goal_difference"] > team2["goal_difference"]:
                return -1
            else:
                # compare goals for
                if team1["goals_for"] < team2["goals_for"]:
                    return 1
                elif team2["goals_for"] > team2["goals_for"]:
                    return -1
                else:
                    # compare goals against
                    if team1["goals_against"] < team2["goals_against"]:
                        return -1
                    elif team2["goals_against"] > team2["goals_against"]:
                        return 1
                    else:
                        # default to alphabet
                        if team1["name"] < team2["name"]:
                            return -1
                        else:
                            return 1


league_table = Table(teams)
# print(league_table.sort())
for i in league_table.get_table():
    print(i)

# for i in range(20):
#     print(teams[i]["name"], end="")
#     print(" - ", end="")
#     print(team_points[i])

# teams
