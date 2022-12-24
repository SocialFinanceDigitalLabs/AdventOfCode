from collections import Counter, deque
from typing import Iterable, NamedTuple, Set, Tuple

import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config
from aocd import submit

prange = (-1, 0, 1)


class Coordinate(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)


class Move(NamedTuple):
    label: str
    direction: Coordinate
    to_consider: Tuple[Coordinate, ...]


default_move_order = (
    Move("north", Coordinate(0, -1), tuple(Coordinate(x, -1) for x in prange)),
    Move("south", Coordinate(0, 1), tuple(Coordinate(x, 1) for x in prange)),
    Move("west", Coordinate(-1, 0), tuple(Coordinate(-1, y) for y in prange)),
    Move("east", Coordinate(1, 0), tuple(Coordinate(1, y) for y in prange)),
)


class Elf:
    def __init__(self, position: Coordinate):
        self.position = position
        self.move_order = deque(default_move_order)

    def __repr__(self):
        return f"Elf({self.position.x}, {self.position.y})"

    def proposed_move(self, elf_map: Set[Coordinate]) -> Coordinate | None:
        # Check if there are any elves around me
        if len(elf_map & set(self.surrounding_coordinates)) == 0:
            return None

        # Consider the move order
        for move in self.move_order:
            to_consider = {self.position + c for c in move.to_consider}
            if len(elf_map & to_consider) == 0:
                return self.position + move.direction

        return None

    @property
    def surrounding_coordinates(self) -> Tuple[Coordinate]:
        return tuple(
            [
                Coordinate(self.position.x + x, self.position.y + y)
                for x in prange
                for y in prange
                if not (x == y == 0)
            ]
        )


def parse_input(input_data):
    for y, line in enumerate(input_data.splitlines()):
        for x, char in enumerate(line):
            if char == "#":
                yield Elf(Coordinate(x, y))


def print_map(elves, top_left=Coordinate(0, 0), width=6, height=6):
    map = {(e.position.x, e.position.y): e for e in elves}

    for y in range(top_left.y, top_left.y + height):
        for x in range(top_left.x, top_left.x + width):
            if Coordinate(x, y) in map:
                print("#", end="")
            else:
                print(".", end="")
        print()


def move_elves(elves):
    elf_map = {e.position for e in elves}
    proposed_moves = {e: e.proposed_move(elf_map) for e in elves}
    move_counter = Counter(proposed_moves.values())
    for e in elves:
        move = proposed_moves[e]
        if move:
            if move_counter[move] == 1:
                e.position = move
        e.move_order.rotate(-1)

    return proposed_moves


@main.command()
@click.option("--sample", "-s", is_flag=True)
@click.option("--simple-sample", "-ss", is_flag=True)
def day23(sample, simple_sample):
    width = height = None

    if simple_sample:
        input_data = (config.SAMPLE_DIR / "day23-simple.txt").read_text()
        width = height = 6
    elif sample:
        input_data = (config.SAMPLE_DIR / "day23.txt").read_text()
        width, height = 15, 12
    else:
        input_data = (config.USER_DIR / "day23.txt").read_text()

    elves = list(parse_input(input_data))

    print(f"------------ Initial State ------------")
    if width:
        print_map(elves, width=width, height=height)

    for round in range(10):
        move_elves(elves)
        print(f"------------ End of Round {round + 1} ------------")
        if width:
            print_map(elves, width=width, height=height)

    min_x, max_x = min(e.position.x for e in elves), max(e.position.x for e in elves)
    min_y, max_y = min(e.position.y for e in elves), max(e.position.y for e in elves)

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    print("---------------")
    print_map(elves, top_left=Coordinate(min_x, min_y), width=width, height=height)
    print("---------------")

    print("Part 1", width * height - len(elves))

    round = 0
    elves = list(parse_input(input_data))
    while True:
        round += 1
        proposed_moves = move_elves(elves)
        num_moves = len([m for m in proposed_moves.values() if m])
        if num_moves == 0:
            print("---------------")
            min_x, max_x = min(e.position.x for e in elves), max(
                e.position.x for e in elves
            )
            min_y, max_y = min(e.position.y for e in elves), max(
                e.position.y for e in elves
            )
            width = max_x - min_x + 1
            height = max_y - min_y + 1
            print_map(
                elves, top_left=Coordinate(min_x, min_y), width=width, height=height
            )
            print("---------------")
            print("No more moves proposed before round ", round)
            break
        else:
            print(f"{num_moves} moves proposed before round {round}")


if __name__ == "__main__":
    day23(["-s"])
