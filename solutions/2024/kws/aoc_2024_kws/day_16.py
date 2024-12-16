from enum import Enum
from typing import Iterator, List, Tuple

import click
from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config
from aocd import submit
from rich.progress import Progress
from sortedcontainers import SortedSet


class Heading(Enum):
    EAST = "E", (1, 0)
    SOUTH = "S", (0, 1)
    WEST = "W", (-1, 0)
    NORTH = "N", (0, -1)

    def __init__(self, symbol: str, delta: Tuple[int, int]):
        self.symbol = symbol
        self.delta = delta
        self.index = len(list(self.__class__))

    def move(self, x, y):
        return x + self.delta[0], y + self.delta[1]

    @property
    def clockwise(self):
        return list(self.__class__)[(self.index + 1) % len(list(self.__class__))]

    @property
    def counterclockwise(self):
        return list(self.__class__)[(self.index - 1) % len(list(self.__class__))]

    def __repr__(self):
        return self.symbol


class Grid:
    def __init__(self, map: List[str]):
        self.width = len(map[0])
        self.height = len(map)
        self.map = map

    def __getitem__(self, pos: Tuple[int, int]) -> str:
        x, y = pos
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return "#"
        return self.map[y][x]

    def find(self, symbol: str) -> Tuple[int, int]:
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell == symbol:
                    return x, y
        return None

    def move(self, x, y, heading: Heading) -> Tuple[int, int, str]:
        pos = heading.move(x, y)
        return *pos, self[pos]

    def get_options(
        self, x, y, heading: Heading, start_score: int
    ) -> Iterator[Tuple[int, int, int, Heading]]:
        forward = self.move(x, y, heading)
        if forward[2] != "#":
            yield start_score + 1, forward[0], forward[1], heading

        cw = self.move(x, y, heading.clockwise)
        if cw[2] != "#":
            yield start_score + 1001, cw[0], cw[1], heading.clockwise

        cc = self.move(x, y, heading.counterclockwise)
        if cc[2] != "#":
            yield start_score + 1001, cc[0], cc[1], heading.counterclockwise


def walk_grid(map: Grid, start: Tuple[int, int], start_heading: Heading):
    scores = {start: 0}
    options = list(map.get_options(*start, start_heading, 0))

    while options:
        score, x, y, heading = options.pop(0)
        if score < scores.get((x, y), float("inf")):
            scores[(x, y)] = score
            options.extend(map.get_options(x, y, heading, score))

    return scores


def backtrack(scores: dict, start: Tuple[int, int], target_score: int):
    """
    To backtrack, we can only move to a square if the score of getting there + the lowest score of that square is less than or equal to the target score.

    The less than is because we only store the lowest core for each square, but we may have a valid path where that square has a higher score.

    This can happen of you have two paralell paths that then both turn and merge:

             ^
             ║
             ║
    > =======╗ <- the score of this tile will be lower than the tile below,
             ║    but the cost of the turn means the square above will have the same score.
             ║
    > =======╝
    """

    def get_score(x, y):
        return scores.get((x, y), float("inf"))

    options = [
        (0, start, Heading.EAST),
        (0, start, Heading.SOUTH),
        (0, start, Heading.WEST),
        (0, start, Heading.NORTH),
    ]
    visited = set()
    while options:
        score, (x, y), heading = options.pop(0)
        visited.add((x, y))

        if (
            score + 1 + get_score(x + heading.delta[0], y + heading.delta[1])
            <= target_score
        ):
            options.append(
                (score + 1, (x + heading.delta[0], y + heading.delta[1]), heading)
            )

        if (
            score
            + 1001
            + get_score(x + heading.clockwise.delta[0], y + heading.clockwise.delta[1])
            <= target_score
        ):
            options.append(
                (
                    score + 1001,
                    (x + heading.clockwise.delta[0], y + heading.clockwise.delta[1]),
                    heading.clockwise,
                )
            )

        if (
            score
            + 1001
            + get_score(
                x + heading.counterclockwise.delta[0],
                y + heading.counterclockwise.delta[1],
            )
            <= target_score
        ):
            options.append(
                (
                    score + 1001,
                    (
                        x + heading.counterclockwise.delta[0],
                        y + heading.counterclockwise.delta[1],
                    ),
                    heading.counterclockwise,
                )
            )

    return visited


def dump_scores(scores: dict, map: Grid):
    for y in range(map.height):
        for x in range(map.width):
            if (x, y) in scores:
                print(scores[(x, y)], end=",")
            else:
                print("", end=",")
        print()


@main.command()
@click.option(
    "--sample",
    "-s",
    type=click.Choice(["s", "l"]),
    help="Use small or large sample input",
)
def day16(sample):
    if sample:
        print(f"Using {'large' if sample == 'l' else 'small'} sample input")
        input_data = (
            config.SAMPLE_DIR / f"day16_{'large' if sample == 'l' else 'small'}.txt"
        ).read_text()
    else:
        input_data = (config.USER_DIR / "day16.txt").read_text()

    input_data = input_data.strip().splitlines()

    map = Grid(input_data)

    start = map.find("S")
    end = map.find("E")

    print("Starting at", start)

    scores = walk_grid(map, start, Heading.EAST)

    target_score = scores[end]
    print(target_score)

    if not sample:
        submit(target_score, part="a", day=16, year=2024)

    tiles = backtrack(scores, end, target_score)

    print(len(tiles))

    if not sample:
        submit(len(tiles), part="b", day=16, year=2024)
