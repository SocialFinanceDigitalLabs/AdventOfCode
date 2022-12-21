from typing import Dict, Iterator, Mapping, Union

import click
import sympy
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config
from aocd import submit
from sympy import parse_expr

TARGET_VARIABLE = "x"


class MonkeyMagic(Mapping[str, int]):
    def __init__(self, monkeys: Dict[str, str]):
        self.__monkeys = monkeys

    def __getattr__(self, item):
        if item in self.__monkeys:
            return self[item]
        raise AttributeError(item)

    def __getitem__(self, item: str) -> int:
        return int(eval(self.__monkeys[item], {}, self))

    def __len__(self) -> int:
        return len(self.__monkeys)

    def __iter__(self) -> Iterator[str]:
        return iter(self.__monkeys)


class MonkeyInsanity(Mapping[str, int]):
    def __init__(self, monkeys: Dict[str, str]):
        self.__monkeys = monkeys

    def __getattr__(self, item):
        if item in self.__monkeys:
            return self[item]
        raise AttributeError(item)

    def __getitem__(self, item: str) -> Union[str, int]:
        value = self.__monkeys[item]

        if value == TARGET_VARIABLE:
            return TARGET_VARIABLE
        elif value.isnumeric():
            return int(value)

        left, op, right = value.split()
        left = self[left]
        right = self[right]

        return f"({left} {op} {right})"

    def __len__(self) -> int:
        return len(self.__monkeys)

    def __iter__(self) -> Iterator[str]:
        return iter(self.__monkeys)


def solve(value, attribute, monkeys: MonkeyMagic):
    value = monkeys[value]
    print("Attribute:", attribute)


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day21(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day21.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day21.txt").read_text()

    input_data = input_data.splitlines()
    input_data = {m.strip(): v.strip() for l in input_data for m, v in [l.split(":")]}
    monkeys = MonkeyMagic(input_data)
    print("Part 1", monkeys.root)

    # Part 2
    part2_data = input_data.copy()
    part2_data["humn"] = TARGET_VARIABLE
    monkeys = MonkeyInsanity(part2_data)

    left_side, right_side = input_data["root"].split(" + ", 1)
    left_side = monkeys[left_side]
    right_side = monkeys[right_side]

    if TARGET_VARIABLE in right_side:
        left_side, right_side = right_side, left_side

    right_side = eval(right_side)
    equation = f"({left_side}) - ({int(right_side)})"

    from sympy.abc import x

    expr = parse_expr(equation, evaluate=False)

    print("Expr is", expr)
    x = sympy.solve(expr, x)

    print("Part 2", int(x[0]))


if __name__ == "__main__":
    day21(["-s"])
