from collections import deque
from typing import NamedTuple

import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config
from aocd import submit
from rich.progress import track


class Entry(NamedTuple):
    value: int
    orig_index: int

    def __str__(self):
        return str(self.value)


def input_to_list(input):
    return [Entry(int(v), ix) for ix, v in enumerate(input.splitlines())]


def from_extended_index(container, value) -> Entry:
    container_length = len(container)
    return container[value % container_length]


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day20(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day20.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day20.txt").read_text()

    input_data = input_to_list(input_data)
    original_order = tuple(input_data)

    for v in track(original_order):
        current_index = input_data.index(v)
        input_data.remove(v)
        new_index = (current_index + v.value) % len(input_data)
        if new_index == 0:
            input_data.append(v)
        else:
            input_data.insert(new_index, v)
        # print(", ".join(str(s) for s in input_data))

    just_digits = [e.value for e in input_data]
    index_of_zero = just_digits.index(0)

    part_1 = [
        from_extended_index(input_data, index_of_zero + x).value
        for x in (1000, 2000, 3000)
    ]
    print("Part 1", part_1, sum(part_1))

    decryption_key = 811589153

    original_order = tuple(
        Entry(v.value * decryption_key, ix) for ix, v in enumerate(original_order)
    )
    input_data = list(original_order)

    for i in range(10):
        for v in track(original_order):
            current_index = input_data.index(v)
            input_data.remove(v)
            new_index = (current_index + v.value) % len(input_data)
            if new_index == 0:
                input_data.append(v)
            else:
                input_data.insert(new_index, v)

    just_digits = [e.value for e in input_data]
    index_of_zero = just_digits.index(0)

    part_2 = [
        from_extended_index(input_data, index_of_zero + x).value
        for x in (1000, 2000, 3000)
    ]
    print("Part 2", part_2, sum(part_2))
