"""Premier league api."""
from typing import List

import requests

from premierleague.fantasyapi.objects import AllPlayers, Fixture, League, Team


class PremierLeagueAPI:
    """Class to interact with fantasy premier league api."""

    BASE_URL = "https://fantasy.premierleague.com/api"

    @classmethod
    def get_players_raw_data(cls) -> List[dict]:
        """Get raw data for all players."""
        return requests.get(f"{cls.BASE_URL}/bootstrap-static/").json().get("elements")

    @classmethod
    def get_teams_raw_data(cls) -> List[dict]:
        """Get raw data for all teams."""
        return requests.get(f"{cls.BASE_URL}/bootstrap-static/").json().get("teams")

    @classmethod
    def get_fixtures_raw_data(cls) -> List[dict]:
        """Get all raw data for all fixtures."""
        return requests.get(f"{cls.BASE_URL}/fixtures/").json()

    @classmethod
    def get_players(cls) -> AllPlayers:
        """Get all players."""
        players_raw = cls.get_players_raw_data()
        return AllPlayers(players_raw)

    @classmethod
    def get_teams(cls) -> List[Team]:
        """Get all teams."""
        teams_raw = cls.get_teams_raw_data()
        return [Team(**team) for team in teams_raw]

    @classmethod
    def get_fixtures(cls) -> List[Fixture]:
        """Get all fixtures."""
        fixtures_raw = cls.get_fixtures_raw_data()
        return [Fixture(**fixture) for fixture in fixtures_raw]

    @classmethod
    def get_league(cls) -> League:
        """Get the league."""
        return League(
            teams=cls.get_teams(),
            fixtures=cls.get_fixtures(),
            players=cls.get_players(),
        )
