"""Cli application."""
import argparse

from premierleague.fantasyapi.api import PremierLeagueAPI

pl_api = PremierLeagueAPI()


def display_table():
    """Display premier league table."""
    pl_api.get_league().display_table()


def top_scorers():
    """Display top scorers."""
    pl_api.get_players().display_top_scorers()


def top_assisters():
    """Display top assisters."""
    pl_api.get_players().display_top_assisters()


def top_keepers():
    """Display keepers with most clean sheets."""
    pl_api.get_players().display_keepers_with_most_clean_sheets()


def league(args):
    """Handles league commands."""
    if args.option == "table":
        display_table()
    elif args.option == "topscorer":
        top_scorers()
    elif args.option == "topassister":
        top_assisters()
    elif args.option == "topkeeper":
        top_keepers()
    else:
        print(f"{args.option} is an invalid argument.")


def prediction(args):
    """Handles predictions."""
    if args.option == "add":
        print("This would do something...")


def main():
    """Main method accessed by cli."""
    # top-level parser
    parser = argparse.ArgumentParser(description="View premier league statistics.")
    subparsers = parser.add_subparsers(help="sub-command help")

    # league sub-command parser
    league_parser = subparsers.add_parser("league", help="TODO: add league help")
    league_parser.add_argument("option", help="TODO: list options")
    league_parser.set_defaults(func=league)

    # predictions sub-command parser
    prediction_parser = subparsers.add_parser("prediction")
    prediction_parser.add_argument("option", help="TODO: add help for predictions")
    prediction_parser.set_defaults(func=prediction)

    # handle args
    args = parser.parse_args()
    args.func(args)
