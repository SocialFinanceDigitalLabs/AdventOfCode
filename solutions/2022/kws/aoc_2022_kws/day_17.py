import math
from collections import deque
from typing import Literal

import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config
from aocd import submit
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
    states = {}

    for i in track(range(moves)):
        # cur_state = (chamber.state, tuple(jet), tuple(sprites))
        # if cur_state in states:
        #     print("Cycle detected", i, states[cur_state], i - states[cur_state])
        # else:
        #     states[cur_state] = i
        chamber.simplify()
        max_y = chamber.max_y
        rock = Rock(sprites[0], 2, max_y + 3)
        sprites.rotate(-1)

        # print("Adding rock", rock, max_y)
        while True:
            if not chamber.collides(rock.move(jet[0])):
                rock = rock.move(jet[0])
            jet.rotate(-1)
            if chamber.collides(rock.move("v")):
                break
            rock = rock.move("v")

        chamber.add(rock)


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day17(sample):
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

    # chamber = Chamber()
    # simulate_game(jet, sprites, chamber, 2022)
    # print("PART1", chamber.max_y)

    moves = 1000000000000
    if sample:
        cycle = 35
        cycle_start = 15
    else:
        cycle = 1745
        cycle_start = 72

    chamber = Chamber()
    simulate_game(jet, sprites, chamber, cycle_start + cycle)
    p2_1 = chamber.max_y

    chamber = Chamber()
    simulate_game(jet, sprites, chamber, cycle_start + cycle * 2)
    p2_2 = chamber.max_y

    remainder = (moves % cycle) - 1

    chamber = Chamber()
    simulate_game(jet, sprites, chamber, cycle_start + cycle + remainder)
    p2_3 = chamber.max_y

    increments_per_cycle = p2_2 - p2_1

    print("Cycle loops =", cycle)
    print("Cycles height =", p2_1, p2_2, p2_3)
    print("Increment per cycle height =", increments_per_cycle)
    print("Remainder loops =", remainder)
    print("Increment for remainder height =", p2_3 - p2_1)

    answer = increments_per_cycle * (moves // cycle) + p2_3 - p2_1
    print("PART2", answer, answer - 1569054441249)  # Too high
