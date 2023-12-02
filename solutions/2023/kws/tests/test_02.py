import pytest
from aoc_2023_kws.day_02 import Colour, Game


def test_parse_game():
    input = "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"

    game = Game(input)

    assert game.game == 3
    assert len(game.rounds) == 3
    assert game.rounds[0] == {Colour.GREEN: 8, Colour.BLUE: 6, Colour.RED: 20}


def test_find_minimum():
    input = "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"

    game = Game(input)

    assert game.find_minimum(Colour.RED) == 20
    assert game.find_minimum(Colour.GREEN) == 13
    assert game.find_minimum(Colour.BLUE) == 6
