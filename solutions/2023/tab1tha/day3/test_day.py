import os

from day3.part1 import day3_part1, get_adjacent_values, get_num_indices, get_numbers

# from day3.part2 import day2_part2


def test_get_numbers():
    input = """467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598.."""
    assert get_numbers(input) == [
        "467",
        "114",
        "35",
        "633",
        "617",
        "58",
        "592",
        "755",
        "664",
        "598",
    ]


def test_get_num_indices():
    input = ["467..114..", "...*......", "..35..633."]
    assert get_num_indices(input, "114") == [(0, 5)]


def test_get_adjacent_values():
    input = ["467..114..", "...*......", "..35..633."]
    # unique neighbors of the 1 in 114
    assert get_adjacent_values(input, (0, 5), 1) == [".", "1"]
    # unique neighbors of 467
    assert get_adjacent_values(input, (0, 0), 3) == ["*", ".", "6", "7"]
    # check that the location itself is not included
    assert get_adjacent_values(input, (0, 0), 1) == [".", "6"]


def test_day3_part1():
    test_data = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

    sample_data = "test_part1.txt"
    with open(sample_data, "w") as f:
        f.write(test_data)
    assert day3_part1(filepath=sample_data) == 4361
    os.remove(sample_data)


# def test_day3_part2():
#     test_data = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
#     Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
#     Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
#     Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
#     Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

#     sample_data = "test_part2.txt"
#     with open(sample_data, "w") as f:
#         f.write(test_data)

#     assert day3_part2(filepath=sample_data) == 2286
#     os.remove(sample_data)
