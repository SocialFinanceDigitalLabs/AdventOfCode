import click
import numpy as np
from aoc_2023_kws.cli import main
from aoc_2023_kws.config import config
from aocd import submit


class Digit:
    def __init__(self, schematic, x, y):
        self.schematic = schematic
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.schematic[self.y, self.x]}({self.x}, {self.y}, {self.is_start})"

    @property
    def is_start(self):
        return self.x == 0 or not self.schematic[self.y, self.x - 1].isdigit()

    @property
    def is_end(self):
        return (
            self.x == self.schematic.shape[0] - 1
            or not self.schematic[self.y, self.x + 1].isdigit()
        )

    @property
    def value(self):
        return int(self.schematic[self.y, self.x])

    @property
    def start(self):
        if self.is_start:
            return self
        else:
            return Digit(self.schematic, self.x - 1, self.y).start

    @property
    def end(self):
        if self.is_end:
            return self
        else:
            return Digit(self.schematic, self.x + 1, self.y).end

    @property
    def next(self):
        if self.is_end:
            return None
        else:
            return Digit(self.schematic, self.x + 1, self.y)

    @property
    def all(self):
        d = self.start

        digits = [d]
        while not d.is_end:
            d = d.next
            digits.append(d)

        return tuple(digits)

    @property
    def full(self):
        digits = self.all
        return int("".join([str(d.value) for d in digits]))

    def is_adjacent_to(self, x, y):
        # Check if this digit is adjacent to, including diagonals, the given coordinates
        min_x = max(0, self.x - 1)
        max_x = min(self.schematic.shape[0] - 1, self.x + 1)
        min_y = max(0, self.y - 1)
        max_y = min(self.schematic.shape[1] - 1, self.y + 1)
        return x in range(min_x, max_x + 1) and y in range(min_y, max_y + 1)

    @property
    def adjacent_to_symbol(self):
        # Check if any of the adjacent cells, including diagonals, are symbols
        min_x = max(0, self.x - 1)
        max_x = min(self.schematic.shape[0] - 1, self.x + 1)
        min_y = max(0, self.y - 1)
        max_y = min(self.schematic.shape[1] - 1, self.y + 1)
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                char = self.schematic[y, x]
                if not char.isdigit() and char != ".":
                    return True
        return False

    @property
    def is_part(self):
        digits = self.all
        for d in digits:
            if d.adjacent_to_symbol:
                return True

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, o: object) -> bool:
        return self.x == o.x and self.y == o.y


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day03(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day03.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day03.txt").read_text()

    schematic = np.array([list(l) for l in input_data.splitlines()])

    digits = []
    for y in range(schematic.shape[1]):
        for x in range(schematic.shape[0]):
            if schematic[y, x].isdigit():
                digits.append(Digit(schematic, x, y))

    part_numbers = []
    for d in digits:
        print(d.full, "*" if d.is_part else "")
        if d.is_start and d.is_part:
            part_numbers.append(d.full)

    print(sum(part_numbers))

    ## PART 2

    # find the location of all gears
    gears = []
    for y in range(schematic.shape[1]):
        for x in range(schematic.shape[0]):
            if schematic[y, x] == "*":
                gears.append((x, y))

    proper_gears = []
    for g in gears:
        adjacent_digits = set()
        for d in digits:
            if d.is_adjacent_to(*g):
                adjacent_digits.add(d.start)

        if len(adjacent_digits) > 1:
            proper_gears.append(np.multiply(*[d.full for d in adjacent_digits]))

    print(sum(proper_gears))
