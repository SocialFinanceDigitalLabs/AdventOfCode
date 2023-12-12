from functools import reduce

import click
from aoc_2023_kws.cli import main
from aoc_2023_kws.config import config
from aocd import submit


def calculate_differences(value_series):
    differences = []
    for i in range(len(value_series) - 1):
        differences.append(value_series[i + 1] - value_series[i])
    return differences


def find_order(value_series):
    all_orders = [value_series]
    while not all([f == 0 for f in value_series]):
        value_series = calculate_differences(value_series)
        all_orders.append(value_series)

    return all_orders


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day09(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day09.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day09.txt").read_text()

    input_data = input_data.splitlines()
    value_series = [[int(value) for value in line.split()] for line in input_data]

    all_predictions = []
    for vs in value_series:
        fit = find_order(vs)
        last_numbers = [f[-1] for f in fit]
        all_predictions.append(sum(last_numbers))
        print(fit, sum(last_numbers))
        print()

    print(f"Part 1: {sum(all_predictions)}")

    all_predictions = []
    for vs in value_series:
        fit = find_order(vs)
        first_numbers = [f[0] for f in fit]
        first_numbers.reverse()
        prediction = reduce(lambda x, y: y - x, first_numbers)
        all_predictions.append(prediction)

        print(fit, prediction)
        print()

    print(f"Part 2: {sum(all_predictions)}")
