import re

EXPECTED_TEST_ANSWER_PART1 = [8]
EXPECTED_TEST_ANSWER_PART2 = [2286]

PART_ONE = {"red": 12, "green": 13, "blue": 14}


def get_phases(row):
    game_parts = row.split(":")
    game_number = int(game_parts[0].split(" ")[1])
    phases = game_parts[1].split(";")
    return game_number, phases


def run(data):
    """
    Takes a list of values in "data" and returns a sum
    of the game numbers that are possible given the
    pieces in PART_ONE variable above
    """
    total = 0
    for row in data:
        game_number, phases = get_phases(row)
        game_ok = True
        for phase in phases:
            groups = phase.strip().split(",")
            for group in groups:
                colours = group.strip().split(" ")
                if PART_ONE[colours[1]] < int(colours[0]):
                    game_ok = False
                    break
        if game_ok:
            total += game_number

    return total


def run_p2(data):
    """
    Takes a list of values in "data" and determines
    the minimum values of each colour needed for each game
    """
    total = 0
    for row in data:
        game_number, phases = get_phases(row)
        game_ok = True

        colours_needed = {"red": 0, "green": 0, "blue": 0}

        for phase in phases:
            groups = phase.strip().split(",")
            for group in groups:
                colours = group.strip().split(" ")
                if colours_needed[colours[1].strip()] < int(colours[0]):
                    colours_needed[colours[1].strip()] = int(colours[0])

        total += (
            colours_needed["red"] * colours_needed["green"] * colours_needed["blue"]
        )

    return total
