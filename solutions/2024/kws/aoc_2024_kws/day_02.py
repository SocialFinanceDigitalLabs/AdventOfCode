import click
from aocd import submit

from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config
             
def is_sequence_safe(numbers):
    if len(numbers) < 2:
        return False
    
    deltas = [b - a for a, b in zip(numbers, numbers[1:])]

    return (1 <= abs(min(deltas)) <= 3 and 
            1 <= abs(max(deltas)) <= 3 and 
            min(deltas) * max(deltas) > 0)

def can_be_made_safe(sequence):
    for i in range(len(sequence)):
        test_sequence = sequence[:i] + sequence[i+1:]
        if is_sequence_safe(test_sequence):
            return True
    return False


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day02(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day02.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day02.txt").read_text()
        

    input_data = input_data.splitlines()
    input_numbers = [[int(x) for x in row.split()] for row in input_data]
    diffs = [is_sequence_safe(nums) for nums in input_numbers]
    
    safe_count = sum(diffs)

    print(safe_count)

    # submit(safe_count, part="a", day=2, year=2024)

    # part b
    unsafe_numbers = [nums for nums, is_safe in zip(input_numbers, diffs) if not is_safe]
    fixable_count = sum(1 for sequence in unsafe_numbers if can_be_made_safe(sequence))
    
    print(safe_count + fixable_count)
    # submit(safe_count + fixable_count, part="b", day=2, year=2024)
