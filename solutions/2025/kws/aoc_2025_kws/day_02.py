
import click

from aoc_2025_kws.cli import main
from aoc_2025_kws.config import config
from tqdm import tqdm
            
def possible_patterns(value):
    max_len = len(value) // 2
    sub_patterns = []
    for i in range(max_len, 0, -1):
        sub_patterns.append(value[:i])
    return sub_patterns

def is_repeating_pattern(value):
    patterns = possible_patterns(value)
    for pattern in patterns:
        if pattern * 2 == value:
            return True
    return False

def is_repeating_pattern_part2(value):
    patterns = possible_patterns(value)
    for pattern in patterns:
        if value.count(pattern) * len(pattern) == len(value):
            return True
    return False


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day02(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day02.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day02.txt").read_text()
        
    ranges = input_data.split(",")

    total = 0
    for r in tqdm(ranges):
        start, end = r.split("-")
        for i in range(int(start), int(end) + 1):
            i = str(i)
            if is_repeating_pattern(i):
                total += int(i)

    print(f"Part 1: {total}")
    print("--------------------------------")


    total = 0
    for r in tqdm(ranges):
        start, end = r.split("-")
        for i in range(int(start), int(end) + 1):
            i = str(i)
            if is_repeating_pattern_part2(i):
                total += int(i)

    print(total)