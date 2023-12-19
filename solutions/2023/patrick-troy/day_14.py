from aocd import get_data
from pprint import pprint

session = "53616c7465645f5f5e959babee3b98732450e5a8dc2320e845ed91c80b7f39fe01f7" \
          "c01baa3710d5d1e1f631fe6c9f768fc1a035e9c3d5cd00e23c7ea0637cae"

data = get_data(day=14, year=2023, session=session).split("\n")

test = [
    "O....#....",
    "O.OO#....#",
    ".....##...",
    "OO.#O....O",
    ".O.....O#.",
    "O.#..O.#.#",
    "..O..#O..O",
    ".......O..",
    "#....###..",
    "#OO..#....",
]

north_solve = [
    'OO.O.O..##',
    '...OO....O',
    '.O...#O..O',
    '.O.#......',
    '.#.O......',
    '#.#..O#.##',
    '..#...O.#.',
    '....O#.O#.',
    '....#.....',
    '.#.O.#O...'
]


west = [
    '....#..OO#',
    '..###....#',
    '..O.......',
    'O..O#..O..',
    '#.#.O..#.O',
    '.#O.....O.',
    'O....O#.OO',
    '...##.....',
    '#....#OO.O',
    '....#....O'
]


def _rotator(puzzle_input):
    return map("".join, zip(*puzzle_input))


def _tilter(puzzle_input):
    rotated = _rotator(puzzle_input)
    for _ in range(len(puzzle_input)):
        rotated = map(lambda s: s.replace(".O", "O."), rotated)
    return rotated


def load_calculator(puzzle_input):
    tilted = _tilter(puzzle_input)
    return sum(i * (c == 'O') for col in tilted for i, c in enumerate(col[::-1], 1))


assert load_calculator(test) == 136
# print(load_calculator(data))


def _cycle(puzzle_input):
    north = map("".join, zip(*puzzle_input))
    # pprint(list(north))
    west = map("".join, zip(*list(north)[::-1]))
    pprint(list(west)[::-1])


_cycle(test)
