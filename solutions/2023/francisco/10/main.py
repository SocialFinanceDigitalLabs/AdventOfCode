from dataclasses import dataclass
from enum import Enum
from collections import deque
from util import FileParser
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


@dataclass(frozen=True)
class Coordinates:
    y: int
    x: int


def part_1(file):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    data = parser.read()
    s = None
    for row_i, row in enumerate(data):
        for col_i, col in enumerate(row):
            if col == "S":
                s = Coordinates(y=row_i, x=col_i)
                break
        else:
            continue
        break

    queue = deque([s])
    seen = {s}

    while queue:
        c = queue.popleft()
        print(c)

        tile = data[c.y][c.x]

        # tile north
        north = Coordinates(y=c.y - 1, x=c.x)
        south = Coordinates(y=c.y + 1, x=c.x)
        west = Coordinates(y=c.y, x=c.x - 1)
        east = Coordinates(y=c.y, x=c.x + 1)

        if (
            c.y > 0
            and tile in "S|LJ"
            and data[north.y][north.x] in "|7F"
            and north not in seen
        ):
            seen.add(north)
            queue.append(north)

        # tile south
        if (
            c.y < len(data)
            and tile in "S|7F"
            and data[south.y][south.x] in "|LJ"
            and south not in seen
        ):
            seen.add(south)
            queue.append(south)

        # tile west
        if (
            c.x > 0
            and tile in "S-J7"
            and data[west.y][west.x] in "-FL"
            and west not in seen
        ):
            seen.add(west)
            queue.append(west)

        # tile east
        if (
            c.x < len(data[0])
            and tile in "S-LF"
            and data[east.y][east.x] in "-J7"
            and east not in seen
        ):
            seen.add(east)
            queue.append(east)

    return len(seen) // 2


def part_2(file):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    data = parser.read()
    print(data)
