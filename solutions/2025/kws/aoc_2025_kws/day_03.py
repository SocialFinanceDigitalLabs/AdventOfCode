
import click
from aocd import submit

from aoc_2025_kws.cli import main
from aoc_2025_kws.config import config
             
                            
@main.command()
@click.option("--sample", "-s", is_flag=True)
def day03(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day03.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day03.txt").read_text()

    input_data = input_data.splitlines()

    total = 0
    for line in input_data:
        start_digit = max(line[:-1])
        pos_of_start_digit = line.index(start_digit)
        end_digit = max(line[pos_of_start_digit+1:])
        jolts = int(f"{start_digit}{end_digit}")
        print(line, start_digit, end_digit, jolts)
        total += jolts

    print(total)

    if not sample:
        submit(total, part="a", day=3, year=2025)

    def strip_leftmost_smallest_digit(line):
        for ix, c in enumerate(line):
            if ix < len(line) - 1 and c < line[ix+1]:
                return line[:ix] + line[ix+1:]
        return line[:-1]

    total = 0
    for line in input_data:
        original_line = line
        while len(line) > 12:
            line = strip_leftmost_smallest_digit(line)

        total += int(line)
        print(original_line, line)


    print(total)

    if not sample:
        submit(total, part="b", day=3, year=2025)

