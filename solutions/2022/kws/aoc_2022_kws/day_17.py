from collections import deque
from queue import Queue
from typing import Literal

import click
import numpy as np
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config
from rich.progress import track

SPRITES = """
####

 #
###
 #

  #
  #
###

#
#
#
#

##
##
""".split(
    "\n\n"
)


class Sprite:
    def __init__(self, shape):
        coords = []
        shape = [l for l in shape.splitlines() if l.strip() != ""]

        for y, line in enumerate(shape):
            for x, char in enumerate(line):
                if char == "#":
                    coords.append((x, y))

        self.w = max(x for x, y in coords) + 1
        self.h = max(y for x, y in coords) + 1

        self.coords = tuple((x, self.h - y) for x, y in coords)

    @property
    def shape_gen(self):
        for y in range(self.h):
            for x in range(self.w):
                if (x, y) in self.coords:
                    yield "#"
                else:
                    yield "."
            yield "\n"

    @property
    def shape(self):
        return "".join(self.shape_gen)

    def __repr__(self):
        return f"Sprite(w={self.w}, h={self.h}: {self.coords})"


class Rock:
    def __init__(self, sprite: Sprite, x: int, y: int):
        self.sprite = sprite
        self.x = x
        self.y = y

    @property
    def min_x(self):
        return min(x + self.x for x, y in self.sprite.coords)

    @property
    def max_x(self):
        return max(x + self.x for x, y in self.sprite.coords)

    @property
    def translated_coords(self):
        return tuple((x + self.x, y + self.y) for x, y in self.sprite.coords)

    def move(self, direction: Literal["<", ">", "v", "^"]) -> "Rock":
        if direction == "v":
            return Rock(self.sprite, self.x, self.y - 1)

        if direction == "^":
            return Rock(self.sprite, self.x, self.y + 1)

        if self.min_x <= 0 and direction == "<":
            return self

        if self.max_x >= 6 and direction == ">":
            return self

        dx = 1 if direction == ">" else -1
        return Rock(self.sprite, self.x + dx, self.y)

    def __repr__(self):
        return f"Rock({self.sprite} at x={self.x}, y={self.y})"


class Chamber:
    def __init__(self):
        self.coordinates = [(x, 0) for x in range(0, 7)]

    @property
    def max_y(self):
        return max(y for x, y in self.coordinates)

    @property
    def min_y(self):
        return min(y for x, y in self.coordinates)

    def add(self, rock: Rock):
        self.coordinates.extend(rock.translated_coords)

    def collides(self, rock: Rock):
        rock_coordinates = set(rock.translated_coords)
        return set(self.coordinates).intersection(rock_coordinates)

    def simplify(self):
        if self.max_y - self.min_y >= 200:
            self.coordinates = [
                (x, y) for x, y in self.coordinates if y >= self.max_y - 100
            ]

    def state(self):
        state = set(
            (x, y - self.max_y) for x, y in self.coordinates if y >= self.max_y - 10
        )
        return tuple(sorted(state))

    def draw(self, *other_objects):
        coords = set(self.coordinates)
        for obj in other_objects:
            coords.update(obj.translated_coords)

        max_y = max(y for x, y in coords)

        for y in range(max_y, -1, -1):
            print("|", end="")
            for x in range(7):
                if (x, y) in coords:
                    print("#", end="")
                else:
                    print(".", end="")
            print("|")
        print("+-------+")
        print()


def simulate_game(jet, sprites, chamber, moves):
    jet = deque(jet)
    sprites = deque(sprites)

    for i in track(range(moves)):
        yield i, chamber.max_y, chamber.state, tuple(jet), tuple(sprites)
        chamber.simplify()
        max_y = chamber.max_y
        rock = Rock(sprites[0], 2, max_y + 3)
        sprites.rotate(-1)

        while True:
            if not chamber.collides(rock.move(jet[0])):
                rock = rock.move(jet[0])
            jet.rotate(-1)
            if chamber.collides(rock.move("v")):
                break
            rock = rock.move("v")

        chamber.add(rock)


def part2_cycle(jet, sprites):
    moves = 1000000000000

    states = {}
    heights = []

    chamber = Chamber()
    queue = deque(maxlen=6)
    cycle = False
    for i, max_y, *state in simulate_game(jet, sprites, chamber, moves):
        heights.append(max_y)
        state = tuple(state)
        last_state = states.get(state)
        if last_state is None:
            states[state] = i
        else:
            queue.append(last_state)
            if len(queue) == queue.maxlen:
                xdiff = np.diff(queue)
                if xdiff[0] == xdiff[1] == xdiff[3] == xdiff[4] == 1 and xdiff[2] != 1:
                    cycle = True
                    break

    if cycle:
        cycle_start = min(queue)
        cycle_length = max(queue) - min(queue) + 1

        print("Cycle detected")
        print("Cycle start =", cycle_start)
        print("Cycle length =", cycle_length)

        start_height = heights[cycle_start]
        cycle_height = heights[max(queue) + 1] - heights[cycle_start]

        print("Height at cycle start =", start_height)
        print("Height per cycle =", cycle_height)

        cycle_count = (moves - cycle_start) // cycle_length
        extra_cycles = (moves - cycle_start) % cycle_length

        print("Cycle count =", cycle_count)
        print("Extra cycles =", extra_cycles)

        answer = (
            start_height
            + cycle_height * cycle_count
            + heights[cycle_start + extra_cycles]
            - heights[cycle_start]
        )
        print("PART2", answer)
    else:
        print("PART2", chamber.max_y)


@main.command()
@click.option("--sample", "-s", is_flag=True)
@click.option("--part-1", "-1", "part_1", is_flag=True)
@click.option("--part-2", "-2", "part_2", is_flag=True)
def day17(sample, part_1, part_2):
    if sample:
        input_data = (config.SAMPLE_DIR / "day17.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day17.txt").read_text()

    jet = tuple(x for x in input_data if x in "<>")
    sprites = tuple(Sprite(s) for s in SPRITES)

    for s in sprites:
        print(s)
        print(s.shape)
        print()

    if part_1:
        chamber = Chamber()
        for move in simulate_game(jet, sprites, chamber, 2022):
            pass
        print("PART1", chamber.max_y)

    if part_2:
        part2_cycle(jet, sprites)
