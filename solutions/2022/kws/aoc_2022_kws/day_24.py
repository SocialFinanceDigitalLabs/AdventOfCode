import random
from collections import defaultdict, deque
from dataclasses import asdict, dataclass, field
from enum import Enum
from functools import cached_property
from queue import PriorityQueue
from typing import Mapping, NamedTuple, Set

import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config
from aocd import submit
from frozendict import frozendict
from rich.live import Live
from rich.text import Text


def parse_map(input_data):
    for y, line in enumerate(input_data.splitlines()):
        for x, c in enumerate(line):
            yield x, y, c


class Coordinate(NamedTuple):
    x: int
    y: int

    def move(self, x=0, y=0):
        return Coordinate(self.x + x, self.y + y)

    def move_to(self, x=None, y=None):
        x = self.x if x is None else x
        y = self.y if y is None else y
        return Coordinate(x, y)

    def move_direction(self, direction: "Direction", boundaries: "Boundaries"):
        x, y = self.x + direction.coordinate.x, self.y + direction.coordinate.y
        if x >= boundaries.max_x:
            x = boundaries.min_x + 1
        elif x <= boundaries.min_x:
            x = boundaries.max_x - 1
        elif y >= boundaries.max_y:
            y = boundaries.min_y + 1
        elif y <= boundaries.min_y:
            y = boundaries.max_y - 1
        return Coordinate(x, y)

    def __add__(self, other):
        if isinstance(other, Direction):
            other = other.coordinate
        return Coordinate(self.x + other.x, self.y + other.y)


class Boundaries(NamedTuple):
    min_x: int
    max_x: int
    min_y: int
    max_y: int


class Direction(Enum):
    UP = "^", Coordinate(0, -1)
    DOWN = "v", Coordinate(0, 1)
    LEFT = "<", Coordinate(-1, 0)
    RIGHT = ">", Coordinate(1, 0)

    def __init__(self, label, coordinate):
        self.label = label
        self.coordinate = coordinate

    @classmethod
    def for_label(cls, label):
        for direction in cls:
            if direction.label == label:
                return direction
        raise ValueError(f"Unknown label: {label}")


@dataclass(frozen=True)
class Tornado:
    pos: Coordinate
    direction: Direction

    def move(self, boundaries: Boundaries):
        return Tornado(
            pos=self.pos.move_direction(self.direction, boundaries),
            direction=self.direction,
        )

    @classmethod
    def from_input(cls, c, x, y):
        return cls(
            pos=Coordinate(x, y),
            direction=Direction.for_label(c),
        )


@dataclass(frozen=True)
class ValleyMap:
    moves: int
    walls: tuple[Coordinate]
    boundaries: Boundaries
    tornadoes: tuple[Tornado]
    start_pos: Coordinate
    end_pos: Coordinate
    wall_index: Mapping[Coordinate, list[str]]

    __cache = dict()

    @classmethod
    def from_input_data(cls, input_data):
        walls = tuple([Coordinate(x, y) for x, y, c in input_data if c == "#"])

        boundaries = Boundaries(
            min(x for x, y in walls),
            max(x for x, y in walls),
            min(y for x, y in walls),
            max(y for x, y in walls),
        )

        tornadoes = tuple(
            [Tornado.from_input(c, x, y) for x, y, c in input_data if c in "<>^v"]
        )

        start_x = (
            set(range(boundaries.min_x, boundaries.max_x + 1))
            - set(x for x, y in walls if y == boundaries.min_y)
        ).pop()
        end_x = (
            set(range(boundaries.min_x, boundaries.max_x + 1))
            - set(x for x, y in walls if y == boundaries.max_y)
        ).pop()

        start_pos = Coordinate(start_x, boundaries.min_y)
        end_pos = Coordinate(end_x, boundaries.max_y)

        wall_index = frozendict({Coordinate(wall[0], wall[1]): ["#"] for wall in walls})

        return cls(
            moves=0,
            walls=walls,
            boundaries=boundaries,
            tornadoes=tornadoes,
            start_pos=start_pos,
            end_pos=end_pos,
            wall_index=wall_index,
        )

    def clone(self, **kwargs):
        return self.__class__(**{**asdict(self), **kwargs})

    @cached_property
    def next(self) -> "ValleyMap":
        valley_map = ValleyMap.__cache.get(self.tornadoes)
        if valley_map is None:
            valley_map = ValleyMap(
                moves=self.moves + 1,
                walls=self.walls,
                boundaries=self.boundaries,
                tornadoes=tuple(
                    tornado.move(self.boundaries) for tornado in self.tornadoes
                ),
                start_pos=self.start_pos,
                end_pos=self.end_pos,
                wall_index=self.wall_index,
            )
            ValleyMap.__cache[self.tornadoes] = valley_map
        return valley_map

    @cached_property
    def index(self):
        ix = defaultdict(list)
        ix.update(self.wall_index)
        for tornado in self.tornadoes:
            ix[tornado.pos].append(tornado.direction.label)
        return frozendict(ix)

    def to_map(self, expedition: Set[Coordinate] = None):
        value = ""
        for y in range(self.boundaries.min_y, self.boundaries.max_y + 1):
            for x in range(self.boundaries.min_x, self.boundaries.max_x + 1):
                objects_here = self.index.get(Coordinate(x, y), [])
                if expedition and Coordinate(x, y) in expedition:
                    value += "E"
                elif len(objects_here) == 0:
                    value += "."
                elif len(objects_here) == 1:
                    value += objects_here[0]
                else:
                    value += str(len(objects_here))[0]
            value += "\n"
        return value

    def __str__(self):
        return self.to_map()


def three_dijsktra(map_dict, visited, start_pos, end_pos):
    # We start with the last map in the chain
    time_passed = max(map_dict.keys())
    valley_map = map_dict[time_passed]
    b = valley_map.boundaries

    with Live() as live:
        while True:
            last_turn = visited[time_passed]
            time_passed += 1
            valley_map = valley_map.next
            map_dict[time_passed] = valley_map
            visited[time_passed] = current_layer = set()
            live.update(
                Text.assemble(("Round", "bold"), (f" {time_passed}", "bold red"))
            )
            for pos in last_turn:
                for new_pos in [pos] + [
                    pos + direction.coordinate for direction in Direction
                ]:
                    if (
                        new_pos not in valley_map.index
                        and b.min_x <= new_pos.x <= b.max_x
                        and b.min_y <= new_pos.y <= b.max_y
                    ):
                        current_layer.add(new_pos)
                        if new_pos == end_pos:
                            print("Previous position", pos)
                            return map_dict, visited


@main.command()
@click.option("--sample", "-s", is_flag=True)
@click.option("--simple-sample", "-ss", is_flag=True)
def day24(sample, simple_sample):
    if simple_sample:
        input_data = (config.SAMPLE_DIR / "day24-simple.txt").read_text()
    elif sample:
        input_data = (config.SAMPLE_DIR / "day24.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day24.txt").read_text()

    input_data = tuple(parse_map(input_data))
    valley_map = ValleyMap.from_input_data(input_data)

    end_pos, start_pos = valley_map.end_pos, valley_map.start_pos
    print("Journey:", start_pos, end_pos)

    visited = {0: {start_pos}}
    map_dict = {0: valley_map}

    map_dict, visited = three_dijsktra(map_dict, visited, start_pos, end_pos)

    time_passed = max(map_dict.keys())
    print(f"Found in {time_passed} steps")

    print("Returning....")
    visited = {time_passed: {end_pos}}
    map_dict, visited = three_dijsktra(map_dict, visited, end_pos, start_pos)

    time_passed = max(map_dict.keys())
    print(f"Back to start in {time_passed} steps")

    print("And back....")
    visited = {time_passed: {start_pos}}
    map_dict, visited = three_dijsktra(map_dict, visited, start_pos, end_pos)

    time_passed = max(map_dict.keys())
    print(f"And finally at end {time_passed} steps")
