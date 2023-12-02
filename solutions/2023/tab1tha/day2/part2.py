from day2.part1 import create_game_df


def day2_part2(filepath: str):
    game_df = create_game_df(filepath)
    min_cubes = game_df.groupby("game").max()
    min_cubes["power"] = min_cubes["red"] * min_cubes["green"] * min_cubes["blue"]
    return int(min_cubes["power"].sum())


if __name__ == "__main__":
    result = day2_part2(filepath="day2\input.txt")
    print(result)
