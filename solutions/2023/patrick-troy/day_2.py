from aocd import get_data
import re
import numpy as np

session = "53616c7465645f5f5e959babee3b98732450e5a8dc2320e845ed91c80b7f39fe01f7" \
          "c01baa3710d5d1e1f631fe6c9f768fc1a035e9c3d5cd00e23c7ea0637cae"

data = get_data(day=2, year=2023, session=session).split("\n")

test = [
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
    "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
    "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
]


test_cubes = {"red": 12, "green": 13, "blue": 14}


def find_possible_games(puzzle_input, cubes):
    failed_games = set()
    total_games = set()
    for row in puzzle_input:
        game = re.search(r"\d+", row.split(":")[0]).group(0)
        total_games.add(int(game))
        row = row.split(":")[1].split(";")
        for games in row:
            games = games.split(",")
            for values in games:
                number = int(re.search(r"\d+", values).group(0))
                colour = re.search(r"[A-Za-z]+", values).group(0)
                game_dict = {colour: number}
                for cube in game_dict:
                    if game_dict[cube] > cubes[cube]:
                        failed_games.add(int(game))

    successful_games = (total_games-failed_games)
    sum_of_ids = sum(successful_games)
    return sum_of_ids


assert find_possible_games(test, test_cubes) == 8
print(find_possible_games(data, test_cubes))


def find_power(puzzle_input):
    powers = []
    for row in puzzle_input:
        new_row = {"red": 0, "green": 0, "blue": 0}
        row = row.split(":")[1].split(";")
        for games in row:
            games = games.split(",")
            for values in games:
                number = int(re.search(r"\d+", values).group(0))
                colour = re.search(r"[A-Za-z]+", values).group(0)
                if new_row[colour] < number:
                    new_row[colour] = number

        powers.append(np.prod(list(new_row.values())))
    return sum(powers)


assert find_power(test) == 2286
print(find_power(data))
