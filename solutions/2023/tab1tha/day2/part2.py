from part1 import create_game_df


def day2_part2(filepath: str):
    game_df = create_game_df(filepath)
    result = game_df.groupby("game").max()
    return result


if __name__ == "__main__":
    result = day2_part2(filepath="day1\input1.txt")
    print(result)
