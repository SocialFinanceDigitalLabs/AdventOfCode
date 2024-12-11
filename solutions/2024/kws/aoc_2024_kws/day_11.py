import click
from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config
from aocd import submit


class Stone:
    def __init__(self, value):
        self.value = value
        self.next: "Stone" = None
        self.prev: "Stone" = None

    def blink(self):
        if self.value == 0:
            self.value = 1
        elif len(str(self.value)) % 2 == 0:
            val1, val2 = (
                str(self.value)[: len(str(self.value)) // 2],
                str(self.value)[len(str(self.value)) // 2 :],
            )
            self.value = int(val1)
            new_stone = Stone(int(val2))
            if self.next:
                self.next.prev = new_stone
            new_stone.next = self.next
            self.next = new_stone
        else:
            self.value *= 2024

    def __iter__(self):
        current = self
        while current:
            _next = current.next
            yield current
            current = _next


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day11(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day11.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day11.txt").read_text()

    values = [int(line) for line in input_data.split(" ")]
    first_stone = Stone(values.pop(0))
    current_stone = first_stone
    while values:
        new_stone = Stone(values.pop(0))
        current_stone.next = new_stone
        new_stone.prev = current_stone
        current_stone = new_stone

    for _ in range(25):
        for stone in first_stone:
            stone.blink()

    stones = len(list(first_stone))
    print(stones)
    # submit(my_answer, part="a", day=11, year=2024)
