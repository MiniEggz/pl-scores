"""Premier league predictions."""

from dataclasses import dataclass, field
from typing import List, Optional

from pydantic import BaseModel

from premierleague.fantasyapi.api import PremierLeagueAPI as pl_api
from premierleague.fantasyapi.objects import Player, Team


class Validator:
    """Validate input for players and teams."""

    def __init__(self):
        self.players = pl_api.get_players()
        self.teams = pl_api.get_teams()

    @staticmethod
    def _get_close_player_names(
        player_name: str, valid_player_names: List[str]
    ) -> List[str]:
        """Get close matches for player names."""
        return [
            name for name in valid_player_names if player_name.lower() in name.lower()
        ]

    @staticmethod
    def _get_close_team_names(team_name: str, valid_team_names: List[str]) -> List[str]:
        """Get close matches for team names."""
        return [name for name in valid_team_names if team_name.lower() in name.lower()]

    # TODO: make the lower case checking work everywhere
    def validate_player_name(self, player_name: str, keepers_only=False) -> bool:
        """Validate the name of a player."""
        if keepers_only:
            valid_player_names = self.players.get_player_names(self.players.keepers)
        else:
            valid_player_names = self.players.get_player_names()
        if player_name in valid_player_names:
            return True
        else:
            close_matches = self._get_close_player_names(
                player_name, valid_player_names
            )
            if close_matches:
                print("Did you mean...")
                for match in close_matches:
                    print(f"\t{match}")
            else:
                print("No matches found.")
            return False

    def validate_team_name(self, team_name: str) -> bool:
        """Validate the name of a team."""
        valid_team_names = [team.name for team in self.teams]
        if team_name in valid_team_names:
            return True
        else:
            close_matches = self._get_close_team_names(team_name, valid_team_names)
            if close_matches:
                print("Did you mean...")
                for match in close_matches:
                    print(f"\t{match}")
            else:
                print("No matches found.")
            return False


class Prediction(BaseModel):
    """Prediction of the state of the league."""

    table: List[Team]
    top_scorer: Player
    top_assister: Player
    top_keeper: Player

    @staticmethod
    def _correctness_message(correct: bool) -> str:
        """Get string from bool.
        
        Args:
            correct (bool): whether answer is correct.

        Returns:
            str: string to output to user.
        """
        if correct:
            return "Yes"
        else:
            return "No"

    @property
    def teams_in_correct_position(self) -> int:
        """Get the correctness score for the table."""
        teams_correct = 0
        for prediction_team, result_team in zip(self.table, pl_api.get_league().table):
            if prediction_team.id == result_team.id:
                teams_correct += 1
        return teams_correct

    @property
    def is_top_scorer_correct(self) -> bool:
        """Check if top scorer is correct."""
        return self.top_scorer in pl_api.get_players().get_top_scorers()

    @property
    def is_top_assister_correct(self) -> bool:
        """Check if top assister is correct."""
        return self.top_assister in pl_api.get_players().get_top_assisters()

    @property
    def is_top_keeper_correct(self) -> bool:
        """Check if top keeper is correct."""
        return self.top_keeper in pl_api.get_players().get_keepers_with_most_clean_sheets()

    def display_correctness(self):
        """Output how correct the prediction was."""
        print(f"Number of teams in correct position: {self.teams_in_correct_position}")
        print(f"Is {self.top_scorer.name} top scorer? "
        f"{self._correctness_message(self.is_top_scorer_correct)}")
        print(f"Does {self.top_assister.name} have the most assists? "
        f"{self._correctness_message(self.is_top_assister_correct)}")
        print(f"Does {self.top_keeper.name} have the most clean sheets? "
        f"{self._correctness_message(self.is_top_keeper_correct)}")


@dataclass
class PredictionReader:
    """Read in predictions from the terminal."""

    table: List[Team] = field(default_factory=list)
    top_scorer: Optional[Player] = None
    top_assister: Optional[Player] = None
    top_keeper: Optional[Player] = None
    validator: Validator = field(default_factory=Validator)

    def _team_with_name(self, team_name: str) -> Team:
        """Get team with specific name.

        Args:
            team_name (str): team name.

        Returns:
            Team: team with given team name.
        """
        for team in self.validator.teams:
            if team.name == team_name:
                return team

    def _player_with_name(self, player_name: str) -> Player:
        """Get player with specific name.

        Args:
            player_name (str): player name.

        Returns:
            Player: player with given name.
        """
        for player in self.validator.players.players:
            if player.name == player_name:
                return player

    def read_table_prediction(self):
        """Read predictions for the table state."""
        team_names = []
        for i in range(1, 21):
            while True:
                next_team = input(f"{i}. ")
                if self.validator.validate_team_name(next_team):
                    if next_team in team_names:
                        print("Team has already been inputted.")
                    else:
                        team_names.append(next_team)
                        break
        self.table = [self._team_with_name(team_name) for team_name in team_names]

    def read_top_scorer_prediction(self):
        """Read prediction for top scorer."""
        while True:
            player_name = input("Top scorer: ")
            if self.validator.validate_player_name(player_name):
                self.top_scorer = self._player_with_name(player_name)
                break

    def read_top_assister_prediction(self):
        """Read prediction for top assister."""
        while True:
            player_name = input("Top assister: ")
            if self.validator.validate_player_name(player_name):
                self.top_assister = self._player_with_name(player_name)
                break

    def read_top_keeper_prediction(self):
        """Read prediction for keeper with most clean sheets."""
        while True:
            player_name = input("Top keeper: ")
            if self.validator.validate_player_name(player_name, keepers_only=True):
                self.top_keeper = self._player_with_name(player_name)
                break


    def read_predictions(self) -> Prediction:
        """Read all predictions.

        Returns:
            Prediction: premier league outcome prediction.
        """
        self.read_table_prediction()
        self.read_top_scorer_prediction()
        self.read_top_assister_prediction()
        self.read_top_keeper_prediction()
        return Prediction(**self.__dict__)
