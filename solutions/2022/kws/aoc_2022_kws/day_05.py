import re
from collections import defaultdict

import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config

move_pattern = re.compile(r"move (\d+) from (\d) to (\d)")


def process_stacks(stack_data):
    stack_data = stack_data.splitlines()[::-1][1:]
    stacks = defaultdict(list)
    for line in stack_data:
        for s in range(9):
            pos = 4 * s + 1
            if pos < len(line) and line[pos].strip():
                stacks[s + 1].append(line[pos])

    return stacks


def process_moves(move_directions):
    for line in move_directions.splitlines():
        groups = move_pattern.match(line)
        for _ in range(int(groups[1])):
            yield int(groups[2]), int(groups[3])


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day05(sample):
    data_folder = config.SAMPLE_DIR if sample else config.USER_DIR
    input_data = (data_folder / "day05.txt").read_text()

    stack_data, move_directions = input_data.split("\n\n", 1)
    stacks = process_stacks(stack_data)

    moves = list(process_moves(move_directions))

    for move in moves:
        container = stacks[move[0]].pop()
        stacks[move[1]].append(container)

    top_crates = "".join([stack[-1] for stack in stacks.values()])
    print("Part 1:", top_crates)

    stacks = process_stacks(stack_data)
    for move in move_directions.splitlines():
        groups = move_pattern.match(move)
        from_stack = stacks[int(groups[2])]
        to_stack = stacks[int(groups[3])]
        num_to_move = int(groups[1])

        moved_crates = from_stack[-num_to_move:]
        del from_stack[-num_to_move:]
        to_stack.extend(moved_crates)

    top_crates = "".join([stack[-1] for stack in stacks.values()])
    print("Part 2:", top_crates)
