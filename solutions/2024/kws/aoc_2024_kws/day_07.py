import click
from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config
from aocd import submit


def can_form_target(target, nums, use_concat=False):
    reachable = {nums[0]}
    for i in range(1, len(nums)):
        next_num = nums[i]
        new_reachable = set()
        for val in reachable:
            new_reachable.add(val + next_num)
            new_reachable.add(val * next_num)
            if use_concat:
                new_reachable.add(int(str(val) + str(next_num)))

        reachable = set([x for x in new_reachable if x <= target])
        if not reachable:
            return False

    return target in reachable


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day07(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day07.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day07.txt").read_text()

    input_data = input_data.splitlines()
    data = []
    for line in input_data:
        target, nums = line.split(":")
        target = int(target)
        nums = [int(i) for i in nums.split()]
        data.append((target, nums))

    results = []
    for target, nums in data:
        can_form = can_form_target(target, nums)
        results.append((can_form, target, nums))

    valid = [result for result in results if result[0]]
    answer = sum(int(result[1]) for result in valid)

    print(answer)
    if not sample:
        submit(answer, part="a", day=7, year=2024)

    part2_results = []
    for target, nums in data:
        can_form = can_form_target(target, nums, use_concat=True)
        part2_results.append((can_form, target, nums))

    valid = [result for result in part2_results if result[0]]
    answer = sum(int(result[1]) for result in valid)

    print(answer)
    if not sample:
        submit(answer, part="b", day=7, year=2024)
