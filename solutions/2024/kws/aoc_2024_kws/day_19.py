import heapq
from collections import deque
from functools import lru_cache

import click
from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config
from aocd import submit
from rich.progress import Progress

CACHE_LOOKAHEAD = 8


@lru_cache(maxsize=None)
def test_pattern(sub_pattern, patterns):
    matches = []
    for pattern in patterns:
        if sub_pattern.startswith(pattern):
            matches.append(pattern)
            matches += test_pattern(sub_pattern[len(pattern) :], patterns)

    return tuple(matches)


def find_patterns(design, patterns):
    candidates = [(len(design), [], design)]

    my_patterns = tuple([p for p in patterns if p in design])

    with Progress() as progress:
        task = progress.add_task("Testing patterns", total=len(patterns))
        while candidates:
            _, path, remainder = heapq.heappop(candidates)
            for matched_pattern in test_pattern(
                remainder[:CACHE_LOOKAHEAD], my_patterns
            ):
                new_path = path + [matched_pattern]
                new_match = "".join(new_path)
                new_design = design[len(new_match) :]
                if len(new_design) == 0:
                    yield new_path
                else:
                    heapq.heappush(candidates, (len(new_design), new_path, new_design))
                progress.update(
                    task,
                    description=f"Testing patterns {len(candidates)} - remaining {len(new_design)}",
                )


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day19(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day19.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day19.txt").read_text()

    lines = input_data.splitlines()
    patterns = tuple(lines[0].split(", "))
    designs = lines[2:]

    print("Patterns:", patterns)

    possible = 0
    for design in designs:
        matches = next(find_patterns(design, patterns), None)
        if matches:
            possible += 1
        print(design, matches)

    print("Possible:", possible)

    if not sample:
        submit(possible, part="a", day=19, year=2024)
