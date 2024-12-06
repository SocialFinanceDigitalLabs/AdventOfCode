import random
import time

import click
from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config
from aocd import submit

random.seed(0)


class Grid:
    def __init__(self, input_data: list[str]):
        self.grid = {}
        self.guard = None
        self.width = len(input_data[0])
        self.height = len(input_data)

        for y, line in enumerate(input_data):
            for x, char in enumerate(line):
                if char == "#":
                    self.grid[(x, y)] = Item(x, y)
                elif char == "^":
                    assert not self.guard, "Guard already set"
                    self.guard = Guard(x, y, self)


def setup_grid(input_data: list[str]):
    grid = {}
    guard = None
    return grid, guard, len(input_data[0]), len(input_data)


def print_grid(grid, *, visited: set[tuple[int, int]] = None):
    if visited is None:
        visited = set()
    for y in range(grid.height):
        for x in range(grid.width):
            if grid.guard and grid.guard.position == (x, y):
                print(grid.guard, end="")
            elif (x, y) in grid.grid:
                print(grid.grid[(x, y)], end="")
            elif (x, y) in visited:
                print("X", end="")
            else:
                print(".", end="")
        print()


class Item:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.sprite_id = random.randrange(0, 43)

    @property
    def position(self):
        return (self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "#"


class Guard(Item):
    def __init__(self, x: int, y: int, grid: Grid):
        super().__init__(x, y)
        self.heading = (0, -1)
        self.grid = grid

    @property
    def blocked(self):
        next_pos = self.next_position
        if next_pos in self.grid.grid:
            return True

    @property
    def out_of_bounds(self):
        # Check if next position is out of bounds
        next_pos = self.next_position
        if (
            next_pos[0] < 0
            or next_pos[0] >= self.grid.width
            or next_pos[1] < 0
            or next_pos[1] >= self.grid.height
        ):
            return True

        return False

    def move(self):
        self.x, self.y = self.next_position

    def rotate_90_clockwise(self):
        # Rotate heading 90 degrees clockwise using translation matrix
        # [0 1]  [x]   [-y]
        # [-1 0] [y] = [x]
        x, y = self.heading
        self.heading = (-y, x)

    @property
    def next_position(self):
        return (self.x + self.heading[0], self.y + self.heading[1])

    def __repr__(self):
        if self.heading == (0, -1):
            return "^"
        elif self.heading == (0, 1):
            return "v"
        elif self.heading == (1, 0):
            return ">"
        else:
            return "<"


def run_simulation(grid):
    visited = set()
    visited_heading = set()
    guard = grid.guard
    while True:
        if guard.out_of_bounds:
            visited.add(guard.next_position)
            break
        if guard.blocked:
            guard.rotate_90_clockwise()
        else:
            guard.move()

        pos = guard.position
        pos_heading = (guard.x, guard.y, guard.heading[0], guard.heading[1])
        if pos_heading in visited_heading:
            return visited, visited_heading, True
        visited.add(pos)
        visited_heading.add(pos_heading)

    return visited, visited_heading, False


def animate_simulation(input_data, single):
    grid = Grid(input_data)
    from aoc_2024_kws.extras.day_06 import Animator, GridImage

    animator = Animator(grid)
    guard = grid.guard
    turn = 0
    while True:
        if guard.out_of_bounds:
            break
        if guard.blocked:
            guard.rotate_90_clockwise()
            guard.move()
        else:
            guard.move()

        animator.draw(guard, crop=(200, 200))
        if single:
            animator.images[0].show()
            import sys

            sys.exit(0)
        if len(animator.images) > 400:
            break

        turn += 1
        if turn % 10 == 0:
            print(len(animator.images))

    animator.save_animation("day06.gif")


@main.command()
@click.option("--sample", "-s", is_flag=True)
@click.option("--animate", "-a", is_flag=True)
@click.option("--single", "-S", is_flag=True)
def day06(sample, animate, single):
    if sample:
        input_data = (config.SAMPLE_DIR / "day06.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day06.txt").read_text()

    input_data = input_data.splitlines()

    if animate:
        return animate_simulation(input_data, single)

    grid1 = Grid(input_data)
    visited, _, _ = run_simulation(grid1)

    print(len(visited))

    my_answer = len(visited)
    if not sample:
        submit(my_answer, part="a", day=6, year=2024)

    loops = 0

    # We could optimise this by starting the simulation from the last position of the previous loop,
    # but this is fast enough and I can't be bothered
    for pos in visited:
        grid2 = Grid(input_data)
        grid2.grid[(pos[0], pos[1])] = Item(pos[0], pos[1])
        _, _, loop = run_simulation(grid2)
        if loop:
            loops += 1
            print("Loop", loops)

    print(loops)
    if not sample:
        submit(loops, part="b", day=6, year=2024)
