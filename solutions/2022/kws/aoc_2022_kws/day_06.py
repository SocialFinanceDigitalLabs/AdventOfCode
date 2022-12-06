from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config


@main.command()
def day06():
    input_data = (config.USER_DIR / "day06.txt").read_text()
    part1(input_data)
    part2(input_data)


def part1(input_data):
    p = find_unique_char_substring(input_data)
    print("Part 1:", p)
    return p


def part2(input_data):
    p = find_unique_char_substring(input_data, substring_length=14)
    print("Part 2:", p)
    return p


def find_unique_char_substring(input_data, substring_length=4):
    p = -1
    for p in range(substring_length, len(input_data)):
        section = input_data[p - substring_length : p]
        if len(set(section)) == substring_length:
            break

    assert p >= substring_length

    return p
