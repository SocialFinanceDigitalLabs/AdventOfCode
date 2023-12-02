from enum import Enum

import click
from aoc_2023_kws.cli import main
from aoc_2023_kws.config import config
from aocd import submit


class Colour(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class Game:
    def __init__(self, game_string):
        self.game_string = game_string
        game, rounds = game_string.split(":", 1)
        rounds = rounds.split(";")

        self.game = int(game.split(" ")[1])
        self.rounds = [self._parse_round(r) for r in rounds]

    @staticmethod
    def _parse_round(round_string):
        parts = round_string.split(",")
        parts = [part.strip() for part in parts]

        colours = {}
        for part in parts:
            count, colour = part.split(" ")
            colour = Colour(colour)
            colours[colour] = colours.get(colour, 0) + int(count)

        return colours

    def is_possible(self, red, green, blue):
        for round in self.rounds:
            if round.get(Colour.RED, 0) > red:
                return False
            if round.get(Colour.GREEN, 0) > green:
                return False
            if round.get(Colour.BLUE, 0) > blue:
                return False

        return True

    def find_minimum(self, colour):
        colour_values = [round.get(colour, 0) for round in self.rounds]
        return max(colour_values)


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day02(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day02.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day02.txt").read_text()

    games = [Game(g) for g in input_data.splitlines()]
    possible_game_sum = 0
    red = 12
    green = 13
    blue = 14
    for game in games:
        if game.is_possible(red, green, blue):
            print("Game {} is possible".format(game.game))
            possible_game_sum += game.game
        else:
            print("Game {} is not possible".format(game.game))

    print("Sum of possible games: {}".format(possible_game_sum))

    power_sum = 0
    for game in games:
        r = game.find_minimum(Colour.RED)
        g = game.find_minimum(Colour.GREEN)
        b = game.find_minimum(Colour.BLUE)
        power = r * g * b
        print(f"Game {game.game} {r} red, {g} green, {b} blue, power: {power}")
        power_sum += power

    print("Sum of power: {}".format(power_sum))
