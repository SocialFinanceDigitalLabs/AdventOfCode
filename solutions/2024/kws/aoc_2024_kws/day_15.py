import sys
import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterator, List, TextIO, Type, TypeVar

import click
from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config
from aocd import submit

T = TypeVar("T", bound="Item")


class Direction(Enum):
    UP = ("^", (0, -1))
    DOWN = ("v", (0, 1))
    LEFT = ("<", (-1, 0))
    RIGHT = (">", (1, 0))

    def __init__(self, symbol, delta):
        self.symbol = symbol
        self.delta = delta

    @classmethod
    def from_symbol(cls, symbol):
        for direction in cls:
            if direction.symbol == symbol:
                return direction
        raise ValueError(f"Invalid direction symbol: {symbol}")


class Grid:
    def __init__(self, map: List[str]):
        self.width = len(map[0])
        self.height = len(map)
        self.items = []
        self.robot = None
        for y, row in enumerate(map):
            for x, cell in enumerate(row):
                if cell == "#":
                    self.items.append(Wall(self, x, y))
                elif cell == "O":
                    self.items.append(Box(self, x, y))
                elif cell == "[":
                    self.items.append(LeftBox(self, x, y))
                elif cell == "]":
                    self.items.append(RightBox(self, x, y))
                elif cell == "@":
                    self.robot = Robot(self, x, y)
                    self.items.append(self.robot)
                elif cell == ".":
                    pass
                else:
                    raise ValueError(f"Unknown character: {cell}")

    def objects_of_type(self, item_type: Type[T]) -> Iterator[T]:
        for item in self.items:
            if isinstance(item, item_type):
                yield item

    def get_object(self, x: int, y: int) -> "Item":
        for item in self.items:
            if item.x == x and item.y == y:
                return item
        return None

    def print(self, output: TextIO):
        for y in range(self.height):
            for x in range(self.width):
                for item in self.items:
                    if item.x == x and item.y == y:
                        output.write(item.SYMBOL)
                        break
                else:
                    output.write(".")
            output.write("\n")


class Item(ABC):
    def __init__(self, grid: Grid, x: int, y: int):
        self.grid = grid
        self.x = x
        self.y = y

    @property
    def gps_position(self) -> int:
        return self.y * 100 + self.x

    @abstractmethod
    def can_move(self, direction: Direction) -> bool:
        ...

    @abstractmethod
    def move(self, direction: Direction) -> bool:
        ...

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y})"


class MoveableItem(Item, ABC):
    def can_move(self, direction: Direction) -> bool:
        """
        Checks if this item can move, but doesn't actually move it.

        Does not check if the linked item can move.
        """
        target = self.grid.get_object(
            self.x + direction.delta[0], self.y + direction.delta[1]
        )
        if target is None:
            return True
        return target.can_move(direction)

    def move(self, direction: Direction) -> bool:
        target = self.grid.get_object(
            self.x + direction.delta[0], self.y + direction.delta[1]
        )
        if target is None:
            self.x += direction.delta[0]
            self.y += direction.delta[1]
            return True

        moved = target.move(direction)
        if moved:
            self.x += direction.delta[0]
            self.y += direction.delta[1]
        return moved


class Robot(MoveableItem):
    SYMBOL = "@"


class Box(MoveableItem):
    SYMBOL = "O"


class LeftBox(Item):
    SYMBOL = "["

    @property
    def linked_item(self) -> "RightBox":
        return self._linked_item

    def can_move(self, direction: Direction) -> bool:
        return self.linked_item.can_move(direction)

    def move(self, direction: Direction) -> bool:
        return self.linked_item.move(direction)


class RightBox(Item):
    SYMBOL = "]"

    def __init__(self, grid: Grid, x: int, y: int):
        super().__init__(grid, x, y)
        self._linked_item = self.grid.get_object(self.x - 1, self.y)
        assert isinstance(self._linked_item, LeftBox)
        self._linked_item._linked_item = self

    @property
    def linked_item(self) -> "LeftBox":
        return self._linked_item

    def move_targets(self, direction: Direction):
        if direction in (Direction.UP, Direction.DOWN):
            left_target = self.grid.get_object(self.x - 1, self.y + direction.delta[1])
            right_target = self.grid.get_object(self.x, self.y + direction.delta[1])
            if left_target is not None:
                yield left_target
            if right_target is not None:
                if (
                    hasattr(right_target, "linked_item")
                    and right_target.linked_item is not left_target
                ):
                    yield right_target
        elif direction == Direction.LEFT:
            target = self.grid.get_object(self.x - 2, self.y)
            if target is not None:
                yield target
        elif direction == Direction.RIGHT:
            target = self.grid.get_object(self.x + 1, self.y)
            if target is not None:
                yield target

    def can_move(self, direction: Direction) -> bool:
        move_targets = list(self.move_targets(direction))
        if len(move_targets) == 0:
            return True
        return all(target.can_move(direction) for target in move_targets)

    def move(self, direction: Direction) -> bool:
        targets = list(self.move_targets(direction))
        for t in targets:
            if not t.can_move(direction):
                return False
        for t in targets:
            t.move(direction)

        linked_item = self.linked_item

        if self.can_move(direction) and linked_item.can_move(direction):
            self.x += direction.delta[0]
            self.y += direction.delta[1]
            linked_item.x = self.x - 1
            linked_item.y = self.y

            return True
        return False


class Wall(Item):
    SYMBOL = "#"

    def can_move(self, direction: Direction) -> bool:
        return False

    def move(self, direction: Direction) -> bool:
        return False


def test_run():
    map = """
##############
##......##..##
##...@......##
##..........##
##...[].....##
##..........##
##..[]......##
##..........##
##...[].....##
##..........##
##..........##
##############
""".strip()

    instructions = "vvvvvvv"

    grid = Grid(map.splitlines())
    grid.print(sys.stdout)
    for i in instructions:
        direction = Direction.from_symbol(i)
        grid.robot.move(direction)
        print(f"After moving {direction}:")
        grid.print(sys.stdout)


@main.command()
@click.option("--sample", "-s", is_flag=True)
@click.option("--test", "-t", is_flag=True)
def day15(sample, test):
    if test:
        return test_run()
    if sample:
        input_data = (config.SAMPLE_DIR / "day15.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day15.txt").read_text()

    map, instructions = input_data.split("\n\n")
    map = map.splitlines()
    instructions = instructions.strip().replace("\n", "")

    grid = Grid(map)

    for i in instructions:
        direction = Direction.from_symbol(i)
        grid.robot.move(direction)

    grid.print(sys.stdout)

    total_score = 0
    for item in grid.objects_of_type(Box):
        total_score += item.gps_position

    print()
    print(total_score)

    if not sample:
        submit(total_score, part="a", day=15, year=2024)

    part2_map = []
    for y in map:
        new_row = []
        for x in y:
            # new_row.append(x)
            if x == "@":
                new_row.append("@.")
            elif x == "#":
                new_row.append("##")
            elif x == "O":
                new_row.append("[]")
            elif x == ".":
                new_row.append("..")
            else:
                raise ValueError(f"Unknown character: {x}")
        part2_map.append("".join(new_row))

    grid = Grid(part2_map)
    grid.print(sys.stdout)

    left_boxes = list(grid.objects_of_type(LeftBox))
    right_boxes = list(grid.objects_of_type(RightBox))
    walls = list(grid.objects_of_type(Wall))

    for i in instructions:
        direction = Direction.from_symbol(i)
        can_move = grid.robot.move(direction)
        # if can_move:
        #     print(f"After moving {direction} {i}:")
        #     grid.print(sys.stdout)
        # else:
        #     print(f"BLOOCKED from moving {direction} {i}")
        #     grid.print(sys.stdout)
        # time.sleep(1)

    grid.print(sys.stdout)

    total_score = 0
    for item in grid.objects_of_type(LeftBox):
        total_score += item.gps_position

    print()
    print(total_score)

    new_left_boxes = list(grid.objects_of_type(LeftBox))
    new_right_boxes = list(grid.objects_of_type(RightBox))
    new_walls = list(grid.objects_of_type(Wall))

    assert len(new_left_boxes) == len(left_boxes)
    assert len(new_right_boxes) == len(right_boxes)
    assert len(new_walls) == len(walls)

    assert len(new_left_boxes) == len(new_right_boxes)

    if not sample:
        submit(total_score, part="b", day=15, year=2024)
