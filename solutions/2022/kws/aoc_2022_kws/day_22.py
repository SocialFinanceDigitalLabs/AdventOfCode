import re
from collections import deque
from enum import Enum
from typing import Iterator, List, Mapping, NamedTuple, Tuple

import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config
from aocd import submit
from attr import dataclass


class Tile(Enum):
    OPEN_SPACE = "."
    WALL = "#"


class Direction(Enum):
    LEFT = "L"
    RIGHT = "R"
    NONE = ""


class Facing(Enum):
    RIGHT = ">", (1, 0)
    DOWN = "v", (0, 1)
    LEFT = "<", (-1, 0)
    UP = "^", (0, -1)

    def __init__(self, symbol: str, delta: Tuple[int, int]):
        self.symbol = symbol
        self.delta = delta

    def __str__(self):
        return self.symbol

    @property
    def score(self):
        options = list(type(self))
        return options.index(self)

    def turn(self, direction: Direction) -> "Facing":
        options = deque(type(self))
        current_ix = options.index(self)
        if direction == Direction.LEFT:
            options.rotate(1)
        elif direction == Direction.RIGHT:
            options.rotate(-1)
        return options[current_ix]


class MovementInstructions(NamedTuple):
    direction: Direction
    length: int

    def __str__(self):
        return f"Move {self.length} and rotate {self.direction.name.lower()}"

    @staticmethod
    def parse_directions(data) -> List["MovementInstructions"]:
        def yield_groups(data):
            while m := re.search(r"(\d+)([LR])?", data):
                length, direction = m.groups()
                length = int(length)
                direction = Direction(direction) if direction else Direction.NONE
                yield MovementInstructions(direction, length)
                data = data[m.end() :]

        return list(yield_groups(data))


class Coordinate(NamedTuple):
    x: int
    y: int

    def move(self, direction: Facing):
        return Coordinate(self.x + direction.delta[0], self.y + direction.delta[1])


class BoardMap(Mapping[Coordinate, Tile]):
    def __init__(self, data):
        def readlines():
            for y, line in enumerate(data.splitlines()):
                for x, c in enumerate(line):
                    if c != " ":
                        yield x, y, c

        self.__map = {Coordinate(x, y): Tile(c) for x, y, c in readlines()}

    def min_x(self, y: int) -> Coordinate:
        return Coordinate(min(x for x, _y in self if _y == y), y)

    def max_x(self, y: int) -> Coordinate:
        return Coordinate(max(x for x, _y in self if _y == y), y)

    def max_y(self, x: int) -> Coordinate:
        return Coordinate(x, max(y for _x, y in self if _x == x))

    def min_y(self, x: int) -> Coordinate:
        return Coordinate(x, min(y for _x, y in self if _x == x))

    @property
    def start_pos(self) -> Coordinate:
        return self.min_x(0)

    def __getitem__(self, pos: Coordinate) -> Tile:
        return self.__map[pos]

    def __len__(self) -> int:
        return len(self.__map)

    def __iter__(self) -> Iterator[Coordinate]:
        return iter(self.__map)

    def move(
        self, pos: Coordinate, heading: Facing, length: int
    ) -> Tuple[Coordinate, Facing]:
        if length <= 0:
            return pos, heading
        new_pos, new_heading = pos.move(heading), heading
        if new_pos in self and self[new_pos] == Tile.OPEN_SPACE:
            return self.move(new_pos, new_heading, length - 1)
        elif new_pos in self and self[new_pos] == Tile.WALL:
            return pos, heading
        else:
            new_heading, new_pos = self.wrap(new_pos, heading)
            if new_pos in self and self[new_pos] == Tile.WALL:
                return pos, heading

            return self.move(new_pos, new_heading, length - 1)

    def wrap(self, pos: Coordinate, heading: Facing) -> Tuple[Facing, Coordinate]:
        if heading == Facing.UP:
            new_pos = self.max_y(pos.x)
        elif heading == Facing.DOWN:
            new_pos = self.min_y(pos.x)
        elif heading == Facing.LEFT:
            new_pos = self.max_x(pos.y)
        elif heading == Facing.RIGHT:
            new_pos = self.min_x(pos.y)
        else:
            raise ValueError(f"Invalid move from {pos}")
        return heading, new_pos

    def expand_moves(self, moves):
        for start, heading, end in moves:
            yield start, heading.symbol
            while start != end:
                start = self.move(start, heading, 1)
                if self.get(start) != Tile.OPEN_SPACE:
                    raise ValueError(
                        "Invalid move - Tried to make an illegal move to ", self[start]
                    )
                yield start, heading.symbol

    def draw(self, extra_symbols=None):
        map = {p: v.value for p, v in self.items()}
        if extra_symbols:
            map.update(extra_symbols)

        max_x = max(x for x, _ in map)
        max_y = max(y for _, y in map)
        map_output = ""
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                map_output += map.get(Coordinate(x, y), " ")
            map_output += "\n"

        return map_output


class CubeMap(BoardMap):
    def __init__(self, data, dimensions: int):
        super().__init__(data)
        self.__dimensions = dimensions

    def face(self, pos: Coordinate):
        if pos.y < self.__dimensions:
            return 1
        elif self.__dimensions <= pos.y < self.__dimensions * 2:
            return 2 + pos.x // self.__dimensions
        else:
            return 5 + ((pos.x - (2 * self.__dimensions)) // self.__dimensions)

    def wrap(self, pos: Coordinate, heading: Facing) -> Tuple[Facing, Coordinate]:
        face = self.face(pos)
        if face == 1:
            if heading == Facing.UP:
                pos = self.max_y(pos.x)
            elif heading == Facing.RIGHT:
                pos = Coordinate(
                    self.__dimensions * 4 - 1, self.__dimensions * 3 - pos.y - 1
                )
                heading = Facing.LEFT
            elif heading == Facing.LEFT:
                pos = Coordinate(self.__dimensions + pos.y, self.__dimensions)
                heading = Facing.DOWN
        elif face == 2:
            if heading == Facing.UP:
                pos = Coordinate(self.__dimensions - pos.x, 0)
                heading = Facing.DOWN
            elif heading == Facing.DOWN:
                pos = Coordinate(self.__dimensions - pos.x, self.__dimensions * 3 - 1)
                heading = Facing.UP
            elif heading == Facing.LEFT:
                pos = Coordinate(
                    self.__dimensions * 3 - pos.y, self.__dimensions * 3 - 1
                )
                heading = Facing.UP

        return heading, pos


@dataclass(frozen=True)
class Player:
    position: Coordinate
    heading: Facing

    def move(self, instructions: MovementInstructions, map: BoardMap) -> "Player":
        pos, heading = map.move(self.position, self.heading, instructions.length)
        return Player(pos, heading.turn(instructions.direction))


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day22(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day22.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day22.txt").read_text()

    input_coordinates, input_directions = input_data.split("\n\n")
    input_map = BoardMap(input_coordinates)
    input_directions = MovementInstructions.parse_directions(input_directions)

    print("Start pos:", input_map.start_pos)

    moves = []

    player = Player(input_map.start_pos, Facing.RIGHT)
    for d in input_directions:
        move = [player.position, player.heading]
        player = player.move(d, input_map)
        moves.append(tuple(move + [player.position]))

    print("Final pos:", player.position, player.heading)

    my_answer = (
        1000 * (player.position.y + 1)
        + 4 * (player.position.x + 1)
        + player.heading.score
    )

    print("Answer:", my_answer)
    # submit(my_answer, part="a", day=22, year=2022)

    cube = CubeMap(input_coordinates, 4 if sample else 50)

    # moves.append(tuple([player.position, player.heading, player.position]))
    # print(input_map.draw({p: v for p, v in self.expand_moves(moves)}))
