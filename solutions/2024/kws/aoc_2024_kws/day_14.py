import math
import os
from collections import Counter
from itertools import combinations

import click
import matplotlib.pyplot as plt
import numpy as np
from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config
from aocd import submit
from rich.progress import track


class Config:
    def __init__(self, grid_size):
        self.grid_size = grid_size[0], grid_size[1]
        self.middle = self.grid_size[0] // 2, self.grid_size[1] // 2
        print(f"Grid size: {self.grid_size}, mid: {self.middle}")


class Robot:
    def __init__(self, config, position, velocity):
        self.config = config
        self.position = position
        self.velocity = velocity

    def move(self, steps):
        self.position = (
            self.position[0] + self.velocity[0] * steps,
            self.position[1] + self.velocity[1] * steps,
        )
        self.position = (
            self.position[0] % self.config.grid_size[0],
            self.position[1] % self.config.grid_size[1],
        )

    def position_after(self, steps):
        position = (
            self.position[0] + self.velocity[0] * steps,
            self.position[1] + self.velocity[1] * steps,
        )
        position = (
            position[0] % self.config.grid_size[0],
            position[1] % self.config.grid_size[1],
        )
        return position

    @property
    def quadrant(self):
        x, y = self.position
        mid_x, mid_y = self.config.middle
        if x == mid_x or y == mid_y:
            return None
        elif x < mid_x and y < mid_y:
            return 1
        elif x > mid_x and y < mid_y:
            return 2
        elif x < mid_x and y > mid_y:
            return 3
        elif x > mid_x and y > mid_y:
            return 4


def load_robots(cfg, input_data):
    robots = []
    for line in input_data.splitlines():
        pos, vel = line.split(" ")
        pos = tuple(map(int, pos[2:].split(",")))
        vel = tuple(map(int, vel[2:].split(",")))
        robots.append(Robot(cfg, pos, vel))
    return robots


def create_image(cfg, robots, seconds):
    grid = np.zeros(cfg.grid_size)
    for robot in robots:
        grid[robot] = 1
    plt.imsave(f"day14/{seconds:08d}.png", grid, cmap="gray")
    return grid


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day14(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day14.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day14.txt").read_text()

    grid_size = (11, 7) if sample else (101, 103)
    cfg = Config(grid_size=grid_size)

    robots = load_robots(cfg, input_data)

    for robot in robots:
        robot.move(100)

    counter = Counter()
    for robot in sorted(robots, key=lambda x: (x.position[1], x.position[0])):
        print(robot.position, robot.quadrant)
        if robot.quadrant is not None:
            counter[robot.quadrant] += 1

    print(counter)
    safety_factor = math.prod(counter.values())

    print(safety_factor)

    if not sample:
        submit(safety_factor, part="a", day=14, year=2024)

    if sample:
        print("No part b")
        return

    def get_pairwise_distances(robots):
        positions = set([r.position for r in robots])
        distances = [
            np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            for (x1, y1), (x2, y2) in combinations(positions, 2)
        ]
        return np.mean(distances)

    robots = load_robots(cfg, input_data)

    os.makedirs("day14", exist_ok=True)
    # min_distance = get_pairwise_distances(robots)
    # for seconds in track(range(10_000)):
    #     for robot in robots:
    #         robot.move(1)

    #     create_image(cfg, robots, seconds)

    # From visually observing the above images, we find that there is a clear
    # concentration of robots in the following sequence of seconds:
    # 46, 104, 147, 207, 248, 310, 349, 413, 450

    # Based on this it appears an 'odd' and 'even' pattern emerges:

    def T(n):
        if n % 2 == 1:  # odd index
            return 46 + 101 * ((n - 1) // 2)
        else:  # even index
            return 103 * (n // 2) + 1

    for n in track(range(1, 10_000)):
        seconds = T(n)
        positions = set([r.position_after(seconds) for r in robots])
        create_image(cfg, positions, seconds)

    # Again, visually inspecting the images, I find a xmas tree at 7520 seconds.
