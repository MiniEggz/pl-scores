"""Objects for premier league results guesser."""
# will contain objects used for creating guesses, etc.
from functools import cmp_to_key

# PremState
# dict containing league positions
# variables holding other statistics


class Table:
    """Object to represent a league table."""

    def __init__(self, teams: dict):
        self.teams = teams.copy()

    def get_table(self):
        """Get the current table."""
        return sorted(self.teams, key=cmp_to_key(self._compare))

    def display_table(self):
        """Display the current table."""
        current_table = self.get_table()
        print("TEAM\tGD\tGF\tGA\tPOINTS")
        print("===============================================")
        for team in current_table:
            print(team["short_name"], end="\t")
            print(team["goal_difference"], end="\t")
            print(team["goals_for"], end="\t")
            print(team["goals_against"], end="\t")
            print(team["points"])
        print("===============================================")

    @staticmethod
    def _compare(team1, team2):
        """Compare teams as leagues do."""
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
