from util import FileParser
import os
from dataclasses import dataclass
from typing import Literal
from functools import reduce
dir_path = os.path.dirname(os.path.realpath(__file__))

@dataclass
class Cubes:
    color: Literal["red", "green", "blue"]
    count: int

@dataclass
class Game:
    id: int
    name: str



color_max_count = {
    "red": 12,
    "green": 13,
    "blue": 14
}



def remove_game_prefix(text: str, nr: int) -> str:
    return text.replace(f"Game {nr}:", "")


def check_game(game: str) -> bool:
    for round in game.strip().split(";"):
            cubes_with_count = round.split(",")
            for cube_count in cubes_with_count:
                count, color = cube_count.strip().split(" ")
                if int(count)>color_max_count[color]:
                    raise ValueError(f"Game {game} is not valid")
    return True

def get_game_power(game: str) -> int:
    _color_max_count = {
        "red": 0,
        "green": 0,
        "blue": 0
    }
    for round in game.strip().split(";"):
        cubes_with_count = round.split(",")
        for cube_count in cubes_with_count:
            count, color = cube_count.strip().split(" ")
            _color_max_count[color] = max(_color_max_count[color], int(count))
    return reduce(lambda x,y: x*y, _color_max_count.values())


def part_1(file: str):
    """should return the solution"""
    parser  = FileParser(dir_path, file)
    games = parser.read()
    possible_games = []
    for i, game in enumerate(games):
        game = remove_game_prefix(game, i+1)
        try:
            check_game(game)
        except ValueError:
            continue
        else:
            possible_games.append(i+1)


    print(possible_games)
    return sum(possible_games)
                

                
            

def part_2(file):
    """should return the solution"""
    parser  = FileParser(dir_path, file)
    games = parser.read()
    powers = []
    for i, game in enumerate(games):
        game = remove_game_prefix(game, i+1)
        powers.append(get_game_power(game))
    return sum(powers)
                

