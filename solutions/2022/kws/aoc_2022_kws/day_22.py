import re
from collections import deque
from enum import Enum
from functools import cached_property, lru_cache
from typing import Dict, Iterator, List, Mapping, NamedTuple, Tuple

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
    RIGHT = ">", (1, 0), "LEFT"
    DOWN = "v", (0, 1), "UP"
    LEFT = "<", (-1, 0), "RIGHT"
    UP = "^", (0, -1), "DOWN"

    def __init__(self, symbol: str, delta: Tuple[int, int], opposite: str):
        self.symbol = symbol
        self.delta = delta
        self.__opposite = opposite

    @property
    def opposite(self) -> "Facing":
        return type(self)[self.__opposite]

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return f"<{type(self).__name__}.{self.name}>"

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
        elif direction == Direction.NONE:
            pass
        else:
            raise ValueError(f"Invalid direction: {direction}")
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
            new_heading, new_pos = self.wrap(pos, heading)
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


class CubeFace:
    def __init__(self, id, x, y, dimensions):
        self.id = id
        self.x = x
        self.y = y
        self.dimensions = dimensions
        self.__connections: Dict[Facing, CubeFace] = {}
        self.__headings: Dict[CubeFace, Facing] = {}

    def __repr__(self):
        return f"CubeFace({self.id}, {self.x}, {self.y})"

    def connections(self) -> Mapping[Facing, "CubeFace"]:
        return self.__connections

    def connection(self, facing: Facing) -> "CubeFace":
        return self.__connections.get(facing)

    def heading(self, face):
        return self.__headings.get(face)

    def add_connection(
        self, facing: Facing, other_face: "CubeFace", other_facing: Facing
    ):
        if other_face not in self.__headings:
            self.__connections[facing] = other_face
            self.__headings[other_face] = facing
        elif self.__headings[other_face] != facing:
            raise ValueError(
                f"Face {self.id} can't have two different headings to the same face: "
                f"{facing} and {self.__headings[other_face]} for Face {other_face.id}"
            )
        if not other_face.connection(other_facing):
            other_face.add_connection(other_facing, self, facing)

    @cached_property
    def min_x(self):
        return self.x * self.dimensions

    @cached_property
    def max_x(self):
        return (self.x + 1) * self.dimensions - 1

    @cached_property
    def min_y(self):
        return self.y * self.dimensions

    @cached_property
    def max_y(self):
        return (self.y + 1) * self.dimensions - 1

    def __contains__(self, item):
        return self.min_x <= item.x <= self.max_x and self.min_y <= item.y <= self.max_y

    def diagonal(
        self, facing: Facing, direction: Direction
    ) -> Tuple["CubeFace", "Facing"]:
        connecting_heading: Facing = facing.turn(direction)
        connecting_face = self.connection(connecting_heading)
        if not connecting_face:
            return None, None

        target_heading = connecting_face.heading(self).turn(direction)

        diagonal = connecting_face.connection(target_heading)
        if not diagonal:
            return None, None

        connecting_heading = diagonal.heading(connecting_face)

        return diagonal, connecting_heading.turn(direction)


class CubeMap(BoardMap):
    def __init__(self, data):
        super().__init__(data)
        self.max_x = max(x for x, _ in self)
        self.max_y = max(y for _, y in self)
        self.dimensions = (max(self.max_x, self.max_y) + 1) // 4
        faces = []
        for y in range(0, self.max_y + 1, self.dimensions):
            for x in range(0, self.max_x + 1, self.dimensions):
                if Coordinate(x, y) in self:
                    faces.append(
                        CubeFace(
                            len(faces) + 1,
                            x // self.dimensions,
                            y // self.dimensions,
                            self.dimensions,
                        )
                    )
        self.faces = {f.id: f for f in faces}

        def get_face(pos):
            for face in self.faces.values():
                if face.x == pos.x and face.y == pos.y:
                    return face

        # Connect directly connected faces
        for face in faces:
            for facing in Facing:
                if not face.connection(facing):
                    other_face = get_face(Coordinate(face.x, face.y).move(facing))
                    if other_face:
                        face.add_connection(facing, other_face, facing.opposite)

        while any(len(f.connections()) < 4 for f in faces):
            for face in faces:
                for facing in Facing:
                    if not face.connection(facing):
                        for dir in [Direction.LEFT, Direction.RIGHT]:
                            other_face, other_facing = face.diagonal(facing, dir)
                            if other_face:
                                face.add_connection(facing, other_face, other_facing)

    def face(self, pos: Coordinate) -> CubeFace:
        for face in self.faces.values():
            if pos in face:
                return face
        raise ValueError(f"Invalid position {pos}")

    def wrap(self, pos: Coordinate, heading: Facing) -> Tuple[Facing, Coordinate]:
        face = self.face(pos)
        nf_face = face.connection(heading)
        nf_heading = nf_face.heading(face)
        if heading == Facing.UP:
            departing_coordinate = pos.x - face.min_x
        elif heading == Facing.RIGHT:
            departing_coordinate = pos.y - face.min_y
        elif heading == Facing.DOWN:
            departing_coordinate = face.max_x - pos.x
        elif heading == Facing.LEFT:
            departing_coordinate = face.max_y - pos.y
        else:
            raise ValueError(f"Invalid move from {pos}")

        if nf_heading == Facing.UP:
            new_pos = Coordinate(nf_face.max_x - departing_coordinate, nf_face.min_y)
            new_heading = Facing.DOWN
        elif nf_heading == Facing.RIGHT:
            new_pos = Coordinate(nf_face.max_x, nf_face.max_y - departing_coordinate)
            new_heading = Facing.LEFT
        elif nf_heading == Facing.DOWN:
            new_pos = Coordinate(nf_face.min_x + departing_coordinate, nf_face.max_y)
            new_heading = Facing.UP
        elif nf_heading == Facing.LEFT:
            new_pos = Coordinate(nf_face.min_x, nf_face.min_y + departing_coordinate)
            new_heading = Facing.RIGHT
        else:
            raise ValueError(f"Invalid move to {nf_heading}")

        return new_heading, new_pos


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

    cube = CubeMap(input_coordinates)

    player = Player(cube.start_pos, Facing.RIGHT)
    for d in input_directions:
        move = [player.position, player.heading]
        player = player.move(d, cube)
        moves.append(tuple(move + [player.position]))

    # moves.append(tuple([player.position, player.heading, player.position]))
    # print(input_map.draw({p: v for p, v in self.expand_moves(moves)}))
    print("Final pos:", player.position, player.heading)

    my_answer = (
        1000 * (player.position.y + 1)
        + 4 * (player.position.x + 1)
        + player.heading.score
    )
    print("Answer:", my_answer)
