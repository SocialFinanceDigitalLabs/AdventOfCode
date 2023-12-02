import os

import pandas as pd
from day2.part1 import day2_part1, extract_game_data, find_impossible_games

# from part2 import day2_part2


def test_extract_game_data():
    assert extract_game_data("3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green") == [
        {"blue": 3, "red": 4},
        {"red": 1, "green": 2, "blue": 6},
        {"green": 2},
    ]
    assert extract_game_data(
        "1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue"
    ) == [
        {"blue": 1, "green": 2},
        {"green": 3, "blue": 4, "red": 1},
        {"green": 1, "blue": 1},
    ]
    assert extract_game_data(
        "8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"
    ) == [
        {"green": 8, "blue": 6, "red": 20},
        {"blue": 5, "red": 4, "green": 13},
        {"green": 5, "red": 1},
    ]
    assert extract_game_data(
        "1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red"
    ) == [
        {"green": 1, "red": 3, "blue": 6},
        {"green": 3, "red": 6},
        {"green": 3, "blue": 15, "red": 14},
    ]
    assert extract_game_data("6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green") == [
        {"red": 6, "blue": 1, "green": 3},
        {"blue": 2, "red": 1, "green": 2},
    ]


def test_find_impossible_games():
    game_df = pd.DataFrame(
        [
            {"red": 6, "blue": 1, "green": 3, "game": 1},
            {"blue": 2, "red": 1, "green": 2, "game": 2},
        ]
    )
    available_cubes = {"red": 5}
    assert find_impossible_games(game_df, "red", available_cubes) == [1]


def test_day2_part1():
    test_data = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

    sample_data = "test_day1.txt"
    with open(sample_data, "w") as f:
        f.write(test_data)
    available_cubes = {"red": 12, "green": 13, "blue": 14}
    assert day2_part1(available_cubes, filepath=sample_data) == 8
    os.remove(sample_data)


# def test_day1_part2():
#     test_data = """two1nine
#     eightwothree
#     abcone2threexyz
#     xtwone3four
#     4nineeightseven2
#     zoneight234
#     7pqrstsixteen"""

#     sample_data = "test_day2.txt"
#     with open(sample_data, "w") as f:
#         f.write(test_data)

#     assert day2_part2(filepath=sample_data) == 281
#     os.remove(sample_data)
