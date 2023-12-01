import click
from aoc_2023_kws.cli import main
from aoc_2023_kws.config import config
from aocd import submit

NUMBERS = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def get_number(word):
    word = [x for x in word if x.isdigit()]
    if len(word) == 1:
        line = int(f"{word[0]}{word[0]}")
    else:
        line = int(f"{word[0]}{word[-1]}")
    return line


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day01(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day01-1.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day01.txt").read_text()

    input_data = input_data.splitlines()

    numbers = []
    for line in input_data:
        numbers.append(get_number(line))

    print(sum(numbers))

    # submit(sum(numbers), part="a", day=1, year=2023)

    if sample:
        input_data = (config.SAMPLE_DIR / "day01-2.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day01.txt").read_text()

    input_data = input_data.splitlines()

    numbers = []
    for line in input_data:
        line = line.lower().strip()
        current_line = ""
        for pos, char in enumerate(line):
            if char.isdigit():
                current_line += char
            else:
                for n, num in enumerate(NUMBERS):
                    if line[pos:].startswith(num):
                        current_line += str(n)
        numbers.append(get_number(current_line))

    print(sum(numbers))

    submit(sum(numbers), part="b", day=1, year=2023)
