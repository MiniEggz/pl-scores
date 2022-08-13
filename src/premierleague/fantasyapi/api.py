# contain methods used to pull data from FPL api.
from typing import List

import requests

from src.premierleague.fantasyapi.objects import (AllPlayers, Fixture, League,
                                                  Team)


class PremierLeagueAPI:
    """Class to interact with fantasy premier league api."""

    BASE_URL = "https://fantasy.premierleague.com/api"

    def get_players_raw_data(self) -> List[dict]:
        """Get raw data for all players."""
        return requests.get(f"{self.BASE_URL}/bootstrap-static/").json().get("elements")

    def get_teams_raw_data(self) -> List[dict]:
        """Get raw data for all teams."""
        return requests.get(f"{self.BASE_URL}/bootstrap-static/").json().get("teams")

    def get_fixtures_raw_data(self) -> List[dict]:
        """Get all raw data for all fixtures."""
        return requests.get(f"{self.BASE_URL}/fixtures/").json()

    def get_players(self) -> AllPlayers:
        """Get all players."""
        players_raw = self.get_players_raw_data()
        return AllPlayers(players_raw)

    def get_teams(self) -> List[Team]:
        """Get all teams."""
        teams_raw = self.get_teams_raw_data()
        return [Team(**team) for team in teams_raw]

    def get_fixtures(self) -> List[Fixture]:
        """Get all fixtures."""
        fixtures_raw = self.get_fixtures_raw_data()
        return [Fixture(**fixture) for fixture in fixtures_raw]

    def get_league(self) -> League:
        """Get the league."""
        return League(
            teams=self.get_teams(),
            fixtures=self.get_fixtures(),
            players=self.get_players(),
        )
