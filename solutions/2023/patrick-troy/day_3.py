from aocd import get_data
import re
import math

session = "53616c7465645f5f5e959babee3b98732450e5a8dc2320e845ed91c80b7f39fe01f7" \
          "c01baa3710d5d1e1f631fe6c9f768fc1a035e9c3d5cd00e23c7ea0637cae"

data = get_data(day=3, year=2023, session=session).split("\n")

test = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",
]


def _get_symbol_co_ords(puzzle_input):
    return {(r, c): [] for r in range(len(puzzle_input)) for c in range(len(puzzle_input))
            if puzzle_input[r][c] not in '01234566789.'}


def _get_star_co_ords(puzzle_input):
    return {(r, c): [] for r in range(len(puzzle_input)) for c in range(len(puzzle_input))
            if puzzle_input[r][c] == '*'}


def _get_numbers_next_to_symbols(puzzle_input, stars_only=False):
    if stars_only:
        symbol_co_ords = _get_star_co_ords(puzzle_input)
    else:
        symbol_co_ords = _get_symbol_co_ords(puzzle_input)

    numbers = {}
    for r, row in enumerate(puzzle_input):
        for n in re.finditer(r'\d+', row):
            numbers[(r, n)] = n.group()
            edge = {(r, c) for r in (r-1, r, r+1) for c in range(n.start()-1, n.end()+1)}

            for overlap in edge & symbol_co_ords.keys():
                if (r, n) in numbers:
                    symbol_co_ords[overlap].append(int(n.group()))
                    numbers.pop((r, n))

    return symbol_co_ords


def solve_1(puzzle_input):
    numbers = _get_numbers_next_to_symbols(puzzle_input)
    return sum(sum(p) for p in numbers.values())


def solve_2(puzzle_input):
    numbers = _get_numbers_next_to_symbols(puzzle_input, stars_only=True)
    return sum(math.prod(p) for p in numbers.values() if len(p) == 2)


assert solve_1(test) == 4361
print(solve_1(data))

assert solve_2(test) == 467835
print(solve_2(data))
