"""Setup."""
from setuptools import find_packages, setup

setup(
    name="premierleague",
    version=1.0,
    packages=find_packages(
        where="src",
    ),
    package_dir={"": "src"},
    entry_points={"console_scripts": ["prem=premierleague.cli.app:main"]},
)
