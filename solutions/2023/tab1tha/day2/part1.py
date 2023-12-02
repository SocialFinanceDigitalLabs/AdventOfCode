import re

import pandas as pd


def extract_game_data(rounds_str: str) -> list:
    # "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    # {"blue": 3, "red": 4}, {"red": 1, "green": 2, "blue": 6}, {"green": 2}
    round_data = []
    for round in rounds_str.split(";"):
        # pattern: number followed by a word
        pattern = re.compile(r"(\d+) (\w+)")
        matches = pattern.findall(round)
        round_dict = {color: int(count) for count, color in matches}
        round_data.append(round_dict)
    return round_data


def create_game_df(filepath: str) -> pd.DataFrame:
    with open(filepath, "r") as f:
        game_df_lst = []
        for line in f.readlines():
            # index 0 gets inner tuple from the list returned by findall
            game_no, rounds_str = re.compile(r"Game (\d+): (.*)").findall(line)[0]
            round_data = extract_game_data(rounds_str)
            round_df = pd.DataFrame(round_data)
            round_df["game"] = game_no
            game_df_lst.append(round_df)

        game_df = pd.concat(game_df_lst)
        game_df.fillna(0, inplace=True)
        game_df["game"] = game_df["game"].astype(int)
        return game_df


def find_impossible_games(
    game_df: pd.DataFrame, cube: str, available_cubes: dict
) -> list:
    fail_df = game_df[game_df[cube] > available_cubes[cube]]
    fail_games = list(set(fail_df["game"]))
    return fail_games


def day2_part1(available_cubes: dict, filepath: str):
    game_df = create_game_df(filepath)
    fails = []
    for cube_type in available_cubes:
        fails.extend(find_impossible_games(game_df, cube_type, available_cubes))
    all_games = game_df["game"].unique()
    possible_games = set(all_games) - set(fails)
    return sum(possible_games)


if __name__ == "__main__":
    available_cubes = {"red": 12, "green": 13, "blue": 14}
    result = day2_part1(available_cubes, filepath="day2\input.txt")
    print(result)
