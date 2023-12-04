import click
from aoc_2023_kws.cli import main
from aoc_2023_kws.config import config
from aocd import submit


class Card:
    def __init__(self, input_string):
        self.card_id, input_string = input_string.split(":")
        winning_numbers, my_numbers = input_string.split(" | ")
        self.winning_numbers = [int(x) for x in winning_numbers.strip().split(" ") if x]
        self.my_numbers = [int(x) for x in my_numbers.strip().split(" ") if x]
        self.count = 1

    @property
    def my_winning_numbers(self):
        return [x for x in self.my_numbers if x in self.winning_numbers]

    @property
    def points(self):
        length = len(self.my_winning_numbers) - 1
        if length == 0:
            return 1
        elif length <= 0:
            return 0
        else:
            return 2**length

    def __repr__(self):
        return f"{self.card_id}{' *' if self.points > 1 else ''}"


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day04(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day04.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day04.txt").read_text()

    lines = input_data.strip().splitlines()

    cards = [Card(line) for line in lines]
    for c in cards:
        print(c.card_id, c.my_winning_numbers, c.points)

    result = sum([c.points for c in cards])
    print(f"The whole pile is worth {result} points")

    # Part 2

    for ix, c in enumerate(cards):
        if c.my_winning_numbers:
            increase = len(c.my_winning_numbers)
            start = ix + 1
            end = ix + increase
            print(
                f"Card {c.card_id} is a winner ({increase}). So {cards[start:end]} increase by {c.count}"
            )
            for c2 in cards[start:end]:
                c2.count += c.count

    result = sum([c.count for c in cards])
    print(f"You now have {result} cards")
