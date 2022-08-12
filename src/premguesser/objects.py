"""Objects for premier league results guesser."""
# will contain objects used for creating guesses, etc.
from dataclasses import dataclass
from datetime import datetime
from functools import cmp_to_key
from typing import List, Optional

from pydantic import BaseModel

# PremState
# dict containing league positions
# variables holding other statistics


class Player(BaseModel):
    """Hold information about each player."""

    id: int
    first_name: str
    second_name: str
    goals_scored: int
    assists: int
    clean_sheets: int
    element_type: int

    @property
    def name(self):
        """Full name of player."""
        return f"{self.first_name} {self.second_name}"


class AllPlayers:
    """Holds all players."""

    def __init__(self, players_response: dict):
        self.players = [Player(**player) for player in players_response]

    def get_top_goals_scored(self) -> int:
        """Get the highest number of goals scored by a single player.

        Returns:
            int: most goals scored by a single player.
        """
        most_goals = 0
        for player in self.players:
            if player.goals_scored > most_goals:
                most_goals = player.goals_scored
        return most_goals

    def get_top_scorers(self) -> List[dict]:
        """Get list of top scorers.

        Returns:
            List[dict]: list of all players that have the highest number of goals.
        """
        most_goals = self.get_top_goals_scored()
        return [player for player in self.players if player.goals_scored == most_goals]

    def get_top_assists_number(self) -> int:
        """Get the highest number of assists made by a single player.

        Returns:
            int: most assists made by a single player.
        """
        most_assists = 0
        for player in self.players:
            if player.assists > most_assists:
                most_assists = player.assists
        return most_assists

    def get_top_assisters(self) -> List[dict]:
        """Get list of top assisters.

        Returns:
            List[dict]: list of all players that have the highest number of assists.
        """
        most_assists = self.get_top_assists_number()
        return [player for player in self.players if player.assists == most_assists]

    def get_most_clean_sheets_by_keeper(self) -> int:
        """Get the highest number of clean sheets by a single keeper.

        Returns:
            int: highest number of clean sheets kepy by a keeper.
        """
        most_clean_sheets = 0
        for player in self.players:
            if player.element_type == 1 and player.element_type > most_clean_sheets:
                most_clean_sheets = player.element_type
        return most_clean_sheets

    def get_keepers_with_most_clean_sheets(self) -> List[dict]:
        """Get the keepers with the most clean sheets.

        Returns:
            List[dict]: list of all keepers with highest number of clean sheets.
        """

        most_clean_sheets = self.get_most_clean_sheets_by_keeper()
        return [
            player
            for player in self.players
            if player.clean_sheets == most_clean_sheets and player.element_type == 1
        ]


class Team(BaseModel):
    """Hold information about a team."""

    # TODO: add games_played (or equivalent)
    id: int
    name: str
    short_name: str
    points: int
    goals_for: int = 0
    goals_against: int = 0

    def __post_init__(self):
        self.reset_stats()

    @property
    def goal_difference(self):
        """Calculated goal difference."""
        return self.goals_for - self.goals_against

    def reset_stats(self):
        """Reset points and goal statistics."""
        self.points = 0
        self.goals_for = 0
        self.goals_against = 0


class Fixture(BaseModel):
    """Object to represent fixtures."""

    id: int
    team_h: int
    team_h_score: Optional[int]
    team_a: int
    team_a_score: Optional[int]
    minutes: int
    kickoff_time: datetime
    finished: bool


@dataclass
class League:
    """Object to represent a league."""

    teams: List[Team]
    fixtures: List[Fixture]

    def __post_init__(self):
        self.calculate_team_stats()

    def get_table(self):
        """Get the current table."""
        return sorted(self.teams, key=cmp_to_key(self._compare))

    def display_table(self):
        """Display the current table."""
        current_table = self.get_table()
        print("TEAM\tGD\tGF\tGA\tPOINTS")
        print("===============================================")
        for team in current_table:
            print(team.short_name, end="\t")
            print(team.goal_difference, end="\t")
            print(team.goals_for, end="\t")
            print(team.goals_against, end="\t")
            print(team.points)
        print("===============================================")

    def calculate_team_stats(self):
        """Calculate the points and score statistics."""
        for fixture in self.fixtures:
            try:
                home_team = self.get_team_with_id(fixture.team_h)
                away_team = self.get_team_with_id(fixture.team_a)
                # update home team goals for/against
                home_team.goals_for += fixture.team_h_score
                home_team.goals_against += fixture.team_a_score
                # update away team goals for/against
                away_team.goals_for += fixture.team_a_score
                away_team.goals_against += fixture.team_h_score

                if fixture.team_h_score > fixture.team_a_score:
                    home_team.points += 3
                elif fixture.team_h_score < fixture.team_a_score:
                    away_team.points += 3
                else:
                    home_team.points += 1
                    away_team.points += 1
            # TODO: add games played.
            except TypeError:
                pass

    def get_team_with_id(self, team_id: int) -> Team:
        """Get team with given id.

        Args:
            team_id (int): id of a team.

        Returns:
            Team: team with the given id.
        """
        for team in self.teams:
            if team.id == team_id:
                return team

    @staticmethod
    def _compare(team1: Team, team2: Team):
        """Compare teams as leagues do."""

        # compare points
        if team1.points < team2.points:
            return 1
        elif team1.points > team2.points:
            return -1
        else:
            # compare goal difference
            if team1.goal_difference < team2.goal_difference:
                return 1
            elif team1.goal_difference > team2.goal_difference:
                return -1
            else:
                # compare goals for
                if team1.goals_for < team2.goals_for:
                    return 1
                elif team2.goals_for > team2.goals_for:
                    return -1
                else:
                    # compare goals against
                    if team1.goals_against < team2.goals_against:
                        return -1
                    elif team2.goals_against > team2.goals_against:
                        return 1
                    else:
                        # default to alphabet
                        if team1.name < team2.name:
                            return -1
                        else:
                            return 1
