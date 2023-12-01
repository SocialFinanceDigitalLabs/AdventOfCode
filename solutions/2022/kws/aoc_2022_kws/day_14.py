from contextlib import contextmanager
from enum import Enum
from typing import Generator, List, Text

import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config
from rich.live import Live


class CoordinateType(Enum):
    ROCK = "#"
    SAND = "o"
    UNREACHABLE = "-"


class Coordinate:
    def __init__(self, *args, type: CoordinateType):
        if len(args) > 0 and isinstance(args[0], str):
            x, y = args[0].split(",", 1)
            self.x = int(x)
            self.y = int(y)
        else:
            self.x = int(args[0])
            self.y = int(args[1])
        self.type = type

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y}, type={self.type})"


def parse_structures(line) -> List[Coordinate]:
    vertices = line.split(" -> ")
    vertices = [Coordinate(v, type=CoordinateType.ROCK) for v in vertices]

    points = []
    for ix, v in enumerate(vertices[1:]):
        dx = v.x - vertices[ix].x
        dy = v.y - vertices[ix].y
        steps = max(abs(dx), abs(dy))
        dx = dx // steps
        dy = dy // steps
        for step in range(steps + 1):
            points.append(
                Coordinate(
                    vertices[ix].x + dx * step, vertices[ix].y + dy * step, type=v.type
                )
            )

    return points


def animate_sand(
    structures: List[Coordinate], sand, floor=0
) -> Generator[Coordinate, None, None]:
    cave_map = {(s.x, s.y) for s in structures}
    y_max = floor if floor else max([c.y for c in structures])

    if (sand.x, sand.y) in cave_map:
        return

    yield sand

    while sand.y <= y_max:
        possible = [
            (sand.x, sand.y + 1),
            (sand.x - 1, sand.y + 1),
            (sand.x + 1, sand.y + 1),
        ]
        if floor:
            possible = [p for p in possible if p[1] <= floor]
        available = [p for p in possible if p not in cave_map]

        if available:
            c = available[0]
            sand = Coordinate(c[0], c[1], type=CoordinateType.SAND)
            yield sand
        else:
            return None


@contextmanager
def show_map():
    with Live() as live:

        def display(structures: List[Coordinate]):
            x_min = min([c.x for c in structures])
            x_max = max([c.x for c in structures])
            y_min = min([c.y for c in structures])
            y_max = max([c.y for c in structures])

            output_data = ""
            map = {(s.x, s.y): s.type for s in structures}
            for y in range(y_min, y_max + 1):
                for x in range(x_min, x_max + 1):
                    s = map.get((x, y))
                    output_data += s.value if s else "."
                output_data += "\n"
            live.update(Text(output_data))

        yield display


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day14(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day14.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day14.txt").read_text()

    starting_structures = [
        c for struct in input_data.splitlines() for c in parse_structures(struct)
    ]
    structures = list(starting_structures)

    y_max = max([c.y for c in structures])

    start_point = Coordinate(500, 0, type=CoordinateType.SAND)
    path = list(animate_sand(structures, start_point))

    with show_map() as display:
        while path[-1].y <= y_max:
            structures.append(path[-1])
            display(structures)
            path = list(animate_sand(structures, start_point))

    print("PART 1", len([c for c in structures if c.type == CoordinateType.SAND]))

    structures = list(starting_structures)
    y_max += 1
    path = list(
        animate_sand(
            structures, Coordinate(500, 0, type=CoordinateType.SAND), floor=y_max
        )
    )
    while path and path[-1].y <= y_max:
        structures.append(path[-1])
        path = list(animate_sand(structures, start_point, floor=y_max))

    with show_map() as display:
        display(structures)

    print("PART 2", len([c for c in structures if c.type == CoordinateType.SAND]))

    ## I suspect there may be a much quicker way to do this by mapping the areas that can't be filled.
    ## The main shape is basically a triangle, but we remove all solid areas as well as those that are unreachable
    ## A block is unreachable if it has an unreachable block above it from x-1 to x+1

    structures = list(starting_structures)
    y_max = max([c.y for c in structures])

    cave_map = {(s.x, s.y): s for s in structures}
    for y in range(y_max + 2):
        x_min = min([c.x for c in cave_map.values()])
        x_max = max([c.x for c in cave_map.values()])
        for x in range(x_min, x_max + 1):
            blockers = {(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)}
            if blockers & cave_map.keys() == blockers:
                if (x, y) not in cave_map:
                    cave_map[(x, y)] = Coordinate(x, y, type=CoordinateType.UNREACHABLE)

    with show_map() as display:
        display(list(cave_map.values()))

    print(f"There are {len(cave_map)} unreachable blocks")

    h = y_max + 2
    area = h**2
    print(
        f"The whole pyramid is {h} blocks high, so there are {area} blocks in the pyramid"
    )
    print(f"So the fillable area is {area - len(cave_map)}")
