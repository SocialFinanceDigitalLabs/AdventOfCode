from typing import Set

import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config


def section_range(section: str) -> Set[int]:
    start, end = section.split("-")
    return set(range(int(start), int(end) + 1))


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day04(sample):
    data_folder = config.SAMPLE_DIR if sample else config.USER_DIR
    input_data = (data_folder / "day04.txt").read_text()

    sections = input_data.splitlines()
    elf_pairs = [line.split(",", 1) for line in sections]
    elf_pairs = [(section_range(elf1), section_range(elf2)) for elf1, elf2 in elf_pairs]

    contained = 0
    for elf1, elf2 in elf_pairs:
        if elf1.issubset(elf2) or elf2.issubset(elf1):
            print("CONTAINED", elf1, elf2)
            contained += 1

    print("Part 1", contained)

    overlaps = 0
    for elf1, elf2 in elf_pairs:
        if elf1 & elf2:
            print("OVERLAP", elf1, elf2, elf1 & elf2)
            overlaps += 1

    print("Part 2", overlaps)
