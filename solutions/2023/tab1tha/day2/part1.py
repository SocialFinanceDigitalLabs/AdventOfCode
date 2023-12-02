import re


def extract_game_data(game: str) -> list:
    # "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    # {"blue": 3, "red": 4}, {"red": 1, "green": 2, "blue": 6}, {"green": 2}

    game_no, rounds_str = re.compile(r"Game (\d+): (.*)").findall(game)[0]
    round_data = []
    for round in rounds_str.split(";"):
        print(round)
        # pattern: number followed by a word
        pattern = re.compile(r"(\d+) (\w+)")
        matches = pattern.findall(round)
        round_dict = {color: int(count) for count, color in matches}
        round_data.append(round_dict)
    print("+++++++++++++++++++++++++++++++++++++++++++++++")
    print(round_data)
    print(game_no)
    return round_data


def day2_part1(filepath: str):
    with open(filepath, "r") as f:
        pass
    return


if __name__ == "__main__":
    result = day2_part1(filepath="day2\input1.txt")
    print(result)
