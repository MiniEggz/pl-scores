# contain methods used to pull data from FPL api.
from typing import List

import requests

from objects import AllPlayers, Fixture, League, Player, Team

response = requests.get(url="https://fantasy.premierleague.com/api/bootstrap-static/")

teams_raw = response.json().get("teams")
fixtures_raw = requests.get("https://fantasy.premierleague.com/api/fixtures/").json()
players_raw = response.json().get("elements")

teams = [Team(**team) for team in teams_raw]
fixtures = [Fixture(**fixture) for fixture in fixtures_raw]
league = League(teams=teams, fixtures=fixtures)
league.display_table()

players = AllPlayers(players_raw)

print(f"Top goal scorer(s) with {players.get_top_goals_scored()} goal(s): ")
for player in players.get_top_scorers():
    print("\t" + player.name)

print(f"Top assister(s) with {players.get_top_assists_number()} assist(s):")
for player in players.get_top_assisters():
    print("\t" + player.name)

print(
    f"Keeper(s) with the most clean sheets with {players.get_most_clean_sheets_by_keeper()} clean sheet(s):"
)
for keeper in players.get_keepers_with_most_clean_sheets():
    print("\t" + keeper.name)
