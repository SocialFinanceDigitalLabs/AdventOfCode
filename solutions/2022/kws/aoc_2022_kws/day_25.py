import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config
from aocd import submit

snafu_chars = "=-012"


def snafu_val(value: str):
    return snafu_chars.index(value) - 2


def snafu_to_base10(value: str):
    return sum([snafu_val(c) * 5**i for i, c in enumerate(value[::-1])])


rsnafu_chars = "012=-"


def base10_to_snafu(value: int):
    """
    A function from converting base 10 numbers to SNAFU numbers

     0 is 000
     2 is 002
     3 is 01=
     4 is 01-
     5 is 010
     6 is 011
     7 is 012
     8 is 02=
     9 is 02-
    10 is 020
    11 is 021
    12 is 022
    13 is 1==
    14 is 1=-
    15 is 1=0
    20 is 1-0
    21 is 1-1
    22 is 1-2
    23 is 10=
    24 is 10-
    25 is 100
    26 is 101
    27 is 102
    28 is 11=
    29 is 11-
    30 is 110

    First digit is given by:
      x % 5 for sequence 0, 1, 2, =, -"""
    if value + 2 < 5:
        return rsnafu_chars[value]
    return base10_to_snafu((value + 2) // 5) + rsnafu_chars[value % 5]


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day25(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day25.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day25.txt").read_text()

    for line in input_data.splitlines():
        print(line, snafu_to_base10(line))

    answer = sum([snafu_to_base10(line) for line in input_data.splitlines()])
    print(f"Answer: {answer} {base10_to_snafu(answer)}")

    if not sample:
        submit(base10_to_snafu(answer), part="a", day=25, year=2022)
