import re

import click
from aoc_2023_kws.cli import main
from aoc_2023_kws.config import config
from aocd import submit

PTN_MATCHER = re.compile(r"(\w+)-to-(\w+) map:")


class Mapper:
    def __init__(self, mapper_id, input_data):
        matches = PTN_MATCHER.match(mapper_id)
        self.from_id = matches.group(1)
        self.to_id = matches.group(2)
        self._ranges = []
        while input_data and input_data[0].strip():
            current_line = input_data.pop(0).strip()
            (
                destination_range_start,
                source_range_start,
                range_length,
            ) = current_line.split(" ", 3)
            destination_range_start = int(destination_range_start)
            source_range_start = int(source_range_start)
            range_length = int(range_length)
            self._ranges.append(
                (destination_range_start, source_range_start, range_length)
            )

    def get(self, value):
        for destination_range_start, source_range_start, range_length in self._ranges:
            if source_range_start <= value < source_range_start + range_length:
                return destination_range_start + value - source_range_start
        return value

    @property
    def reverse(self):
        reverse_mapper = Mapper(f"{self.to_id}-to-{self.from_id} map:", [])
        reverse_mapper._ranges = [(x[1], x[0], x[2]) for x in self._ranges]
        return reverse_mapper

    @property
    def min_mapped(self):
        return min([x[1] for x in self._ranges])

    @property
    def max_mapped(self):
        return max([x[1] for x in self._ranges])

    @property
    def min_target(self):
        return min([x[0] for x in self._ranges])

    @property
    def max_target(self):
        return max([x[0] for x in self._ranges])

    def __repr__(self):
        return f"<Mapper {self.from_id} to {self.to_id}>"


class UberMapper:
    def __init__(self, mappers):
        self.mappers = {m.from_id: m for m in mappers}

    def get(self, from_id, to_id, value):
        mappings = [(from_id, value)]
        while True:
            next_mapper = self.mappers[from_id]
            from_id = next_mapper.to_id
            value = next_mapper.get(value)
            mappings.append((from_id, value))
            if next_mapper.to_id == to_id:
                return mappings[-1][1], mappings

    @property
    def reverse(self):
        return UberMapper([m.reverse for m in self.mappers.values()])

    def __getitem__(self, key):
        return self.mappers[key]


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day05(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day05.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day05.txt").read_text()

    parse_input(input_data)


def parse_input(input_data):
    input_data = input_data.strip().splitlines()

    seeds = input_data.pop(0)[6:].strip().split(" ")
    seeds = [int(x) for x in seeds if x]

    all_mappers = []

    while input_data:
        current_line = input_data.pop(0).strip()
        if not current_line:
            continue

        if ":" in current_line:
            mapper = Mapper(current_line, input_data)
            all_mappers.append(mapper)

    uber_mapper = UberMapper(all_mappers)

    print(seeds, all_mappers)

    # Part 1
    all_locations = []
    for seed in seeds:
        soil_id, mappers = uber_mapper.get("seed", "location", seed)
        print(f"Seed {seed} needs location {soil_id}")
        all_locations.append((soil_id, mappers))

    all_locations.sort(key=lambda x: x[0])

    print(f"Part 1: {all_locations[0]}")

    # Part 2
    seed_ranges = []
    for seed_ix in range(0, len(seeds), 2):
        seed_ranges.append((seeds[seed_ix], seeds[seed_ix] + seeds[seed_ix + 1]))
    print(seed_ranges)

    def in_range(value):
        for seed_range in seed_ranges:
            if seed_range[0] <= value <= seed_range[1]:
                return True
        return False

    for loc in range(0, 100_000_000):
        if loc % 25_000 == 0:
            print(f"Checking location {loc}")
        seed_id, mappers = uber_mapper.reverse.get("location", "seed", loc)
        if in_range(seed_id):
            print(f"Location {loc} can be reached by seed {seed_id}")
            break
