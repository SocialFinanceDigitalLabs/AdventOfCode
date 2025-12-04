import click
from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config
from aocd import submit


def blink_stone(value):
    value = int(value)
    if value == 0:
        return [1]

    val_str = str(value)
    val_len = len(val_str)
    if val_len % 2 == 0:
        return val_str[: val_len // 2], val_str[val_len // 2 :]

    return [value * 2024]


memo = {}


def blink(stone, generations):
    if generations == 0:
        # print("Final Stone", stone)
        return 1

    if (stone, generations) in memo:
        rv = memo[(stone, generations)]
        return rv

    new_stones = blink_stone(stone)

    final_sum = 0
    for s in new_stones:
        final_sum += blink(s, generations - 1)

    memo[(stone, generations)] = final_sum

    return final_sum


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day11(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day11.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day11.txt").read_text()

    values = [int(x) for x in input_data.split()]

    new_stones = 0
    for stone in values:
        new_stones += blink(stone, 25)
    print(new_stones)
    if not sample:
        submit(new_stones, part="a", day=11, year=2024)

    new_stones = 0
    for stone in values:
        new_stones += blink(stone, 75)
    print(new_stones)

    if not sample:
        submit(new_stones, part="b", day=11, year=2024)
