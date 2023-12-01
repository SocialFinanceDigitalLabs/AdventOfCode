import functools
import json
from typing import List, Union

import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config
from aocd import submit

Value = Union[int, str, List["Value"]]


def test_lists(left: List[Value], right: List[Value]):
    for l, r in zip(left, right):
        comp = test_order(l, r)
        if comp != 0:
            return comp

    if len(left) < len(right):
        return -1
    elif len(left) == len(right):
        return 0
    else:
        return 1


def test_ints(left: int, right: int):
    if left < right:
        return -1
    elif left == right:
        return 0
    else:
        return 1


def test_order(left: Value, right: Value):
    left = json.loads(left) if isinstance(left, str) else left
    right = json.loads(right) if isinstance(right, str) else right
    if isinstance(left, int) and isinstance(right, int):
        return test_ints(left, right)
    elif isinstance(left, list) and isinstance(right, list):
        return test_lists(left, right)
    else:
        left = [left] if not isinstance(left, list) else left
        right = [right] if not isinstance(right, list) else right
        return test_lists(left, right)


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day13(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day13.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day13.txt").read_text()

    packet_pairs = input_data.split("\n\n")

    pair_order_check = [test_order(*p.splitlines()) for p in packet_pairs]

    print(pair_order_check)
    print("PART 1", sum([ix + 1 for ix, v in enumerate(pair_order_check) if v < 0]))

    all_packets = [p for p in input_data.splitlines() if p] + ["[[2]]", "[[6]]"]
    all_packets.sort(key=functools.cmp_to_key(test_order))
    print("\n".join(all_packets))

    ix_2 = all_packets.index("[[2]]") + 1
    ix_6 = all_packets.index("[[6]]") + 1

    print("Part 2: ", ix_2, ix_6, ix_2 * ix_6)
