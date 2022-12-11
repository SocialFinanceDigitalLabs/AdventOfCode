import os
from enum import Enum

from util import FileParser

dir_path = os.path.dirname(os.path.realpath(__file__))


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Result(Enum):
    LOSE = 0
    DRAW = 3
    WIN = 6


map_shape = {
    "A": Shape.ROCK,
    "B": Shape.PAPER,
    "C": Shape.SCISSORS,
    "X": Shape.ROCK,
    "Y": Shape.PAPER,
    "Z": Shape.SCISSORS,
}

map_result = {
    "X": Result.LOSE,
    "Y": Result.DRAW,
    "Z": Result.WIN,
}

wins = {
    Shape.SCISSORS: Shape.PAPER,
    Shape.PAPER: Shape.ROCK,
    Shape.ROCK: Shape.SCISSORS,
}

reverse_wins = {v: k for k, v in wins.items()}


def get_round_result(opponent: Shape, user: Shape) -> int:
    if opponent == user:
        return Result.DRAW.value
    if wins[user] == opponent:
        return Result.WIN.value
    return Result.LOSE.value


def get_shape_to_choose(opponent: Shape, user_result: Result) -> Shape:
    if user_result == Result.DRAW:
        return opponent
    if user_result == Result.LOSE:
        return wins[opponent]
    if user_result == Result.WIN:
        return reverse_wins[opponent]


def part_1(file: str):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    game = parser.read()
    result = 0
    for round in game:
        opponent, user = [map_shape[shape] for shape in round.split()]
        result += user.value + get_round_result(opponent, user)
    return result


def part_2(file):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    game = parser.read()
    result = 0
    for round in game:
        round = round.split()

        opponent = map_shape[round[0]]
        user_result = map_result[round[1]]

        user = get_shape_to_choose(opponent, user_result)

        result += user.value + get_round_result(opponent, user)

    return result
