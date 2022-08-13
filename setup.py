"""Setup."""
from setuptools import find_packages, setup

setup(
    name="premierleague",
    version=1.0,
    packages=find_packages(
        include=[
            "src.premierleague",
            "src.premierleague.fantasyapi",
            "src.premierleague.cli",
        ]
    ),
    entry_points={"console_scripts": ["prem=src.premierleague.cli.app:main"]},
)
