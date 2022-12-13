import math

import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config
from rich.progress import track


class Monkey:
    def __init__(self, config):
        config = config.splitlines()
        self.name = int(config[0][7:-1])
        self.items = [int(i) for i in config[1].split(":")[1].split(",")]
        self.operation = config[2].split("=", 1)[1]
        self.test = int(config[3].split("by")[1])
        self.true_monkey = int(config[4][-2:])
        self.false_monkey = int(config[5][-2:])
        self.inspection_count = 0

    def has_items(self):
        return len(self.items) > 0

    def throw_item(self, keep_calm=True):
        self.inspection_count += 1
        item = self.items.pop(0)
        locals = dict(old=item)
        worry_level = eval(self.operation, {}, locals)
        if keep_calm:
            worry_level = worry_level // 3
        if worry_level % self.test == 0:
            return worry_level, self.true_monkey
        else:
            return worry_level, self.false_monkey

    def receive_item(self, item):
        self.items.append(item)

    def __repr__(self):
        return f"<Monkey {self.name}: {', '.join([str(i) for i in self.items])}>"


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day11(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day11.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day11.txt").read_text()
    input_data = input_data.split("\n\n")
    monkeys = [Monkey(m) for m in input_data if not m.isspace()]
    monkeys = {m.name: m for m in monkeys}

    for r in range(20):
        print(f"--- Round {r+1} ---")
        for m in monkeys.values():
            while m.has_items():
                item, to_monkey = m.throw_item()
                monkeys[to_monkey].receive_item(item)
                print(f"  * Monkey {m.name} threw {item} to Monkey {to_monkey}")

        print(
            f"At the end of round {r+1}:", ", ".join([str(s) for s in monkeys.values()])
        )

    for m in monkeys.values():
        print(f"Monkey {m.name} inspected {m.inspection_count} items")

    values = [m.inspection_count for m in monkeys.values()]
    values.sort(reverse=True)

    print("Part 1:", math.prod(values[:2]))

    monkeys = [Monkey(m) for m in input_data if not m.isspace()]
    monkeys = {m.name: m for m in monkeys}

    lcm = math.lcm(*[m.test for m in monkeys.values()])
    print("LCM:", lcm)

    for r in track(range(10_000)):
        for m in monkeys.values():
            while m.has_items():
                item, to_monkey = m.throw_item(keep_calm=False)
                item = item % lcm
                monkeys[to_monkey].receive_item(item)

        if r + 1 in (1, 20, 1000, 2000, 5000, 10000):
            print(f"At the end of round {r+1}:")
            for m in monkeys.values():
                print(
                    f"  * Monkey {m.name} has inspected items {m.inspection_count} times"
                )

    values = [m.inspection_count for m in monkeys.values()]
    values.sort(reverse=True)

    print("Part 2:", math.prod(values[:2]))
