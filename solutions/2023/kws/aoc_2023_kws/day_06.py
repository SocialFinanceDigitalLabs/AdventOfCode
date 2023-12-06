import math

import click
import numpy as np
from aoc_2023_kws.cli import main
from aoc_2023_kws.config import config
from aocd import submit


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day06(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day06.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day06.txt").read_text()

    input_data = input_data.splitlines()
    time_input = input_data[0][10:]
    distance_input = input_data[1][10:]

    time_input = [int(x) for x in time_input.split(" ") if x.strip()]
    distance_input = [int(x) for x in distance_input.split(" ") if x.strip()]

    print(time_input, distance_input)

    all_charge_times = []
    for t, d in zip(time_input, distance_input):
        charge_times = min_charge_time(t, d)
        print(t, d, charge_times)
        all_charge_times.append(charge_times)

    # Part 1
    print(all_charge_times)
    print(np.prod(all_charge_times))

    # Part 2
    time = int(input_data[0][10:].replace(" ", ""))
    distance = int(input_data[1][10:].replace(" ", ""))
    print(time, distance)

    charge_time = min_charge_time(time, distance)

    print(time, distance, charge_time)


def min_charge_time(t, d):
    a = 1
    b = -t
    c = d

    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return None

    t_charge_1 = (-b + math.sqrt(discriminant)) / (2 * a)
    t_charge_2 = (-b - math.sqrt(discriminant)) / (2 * a)

    t_charge_min = min(t_charge_1, t_charge_2)
    t_charge_max = max(t_charge_1, t_charge_2)

    d_travelled = t_charge_min * (t_charge_min + t) / 2

    t_charge_min = math.ceil(t_charge_min)
    t_charge_max = math.floor(t_charge_max)

    if d == d_travelled:
        t_charge_min += 1
        t_charge_max -= 1

    print(
        f"To reach a distance of {d} in {t} seconds, you need to charge for "
        f"{t_charge_min} seconds and at most {t_charge_max} seconds."
    )

    possible_charge_times = t_charge_max - t_charge_min + 1
    return possible_charge_times
