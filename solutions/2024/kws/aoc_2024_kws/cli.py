import importlib
import os
from pathlib import Path

import click

from .config import settings


@click.group()
@click.option("--user", "-u", type=str)
def main(user):
    if user:
        settings.username = user
        settings.save_settings()

    if not settings.username:
        user = click.prompt("Username", type=str, default=os.getlogin())
        settings.username = user
        settings.save_settings()


for name in Path(__file__).parent.glob("day*.py"):
    module = name.stem
    mod = importlib.import_module(f"aoc_2024_kws.{module}")

mod = importlib.import_module(f"aoc_2024_kws.setup")
