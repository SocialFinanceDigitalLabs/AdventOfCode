from util import FileParser
import os
from collections import defaultdict
from dataclasses import dataclass

dir_path = os.path.dirname(os.path.realpath(__file__))


@dataclass
class Mapper:
    dest: int
    source: int
    length: int

    @property
    def end(self):
        return self.source + self.length


@dataclass
class Seed:
    start: int
    end: int


def build_mapper(mapping: str) -> Mapper:
    dest, source, length = map(int, mapping.split())
    return Mapper(
        dest,
        source,
        length,
    )


def clean_data(data: list[str]) -> tuple[list[int], dict[str, list[Mapper]]]:
    initial_seeds = [int(d) for d in data[0].split(" ") if d.isdigit()]

    maps: dict[str, list] = defaultdict(list)
    start = False
    map_category = None
    for row in data[1:]:
        if row == "":
            start = True
            continue
        if start:
            map_category = row.strip("map:").strip()
            start = False
            continue
        if map_category:
            maps[map_category].append(build_mapper(row))

    return initial_seeds, maps


def get_mapper_value(mappers: list[Mapper], source: int):
    for mapper in mappers:
        if source >= mapper.source and source < mapper.end:
            return mapper.dest + (source - mapper.source)
    return source


def part_1(file: str):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    data = parser.read()

    initial_seeds, maps = clean_data(data)

    locations = []
    for seed in initial_seeds:
        source = seed
        for name, mappers in maps.items():
            dest = get_mapper_value(mappers, source)

            source = dest
        locations.append(source)
    return min(locations)


def part_2(file: str):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    # data: list[str] = parser.file_path
    with open(parser.file_path, "r") as f:
        data = f.read().split("\n\n")
    input = list(map(int, data[0].replace("seeds: ", "").strip().split(" ")))
    seeds: list[Seed] = []
    for i in range(0, len(input) - 1, 2):
        seeds.append(Seed(input[i], input[i] + input[i + 1]))

    for category_block in data[1:]:
        mappers: list[Mapper] = []
        for mapping in category_block.splitlines()[1:]:
            mappers.append(build_mapper(mapping))

        next_seeds = []
        while len(seeds) > 0:
            seed = seeds.pop()
            for mapper in mappers:
                overlap_start = max(seed.start, mapper.source)
                overlap_end = min(seed.end, mapper.source + mapper.length)
                if overlap_start < overlap_end:
                    # there's an overlap range - will be converted to next category_block
                    next_seeds.append(
                        Seed(
                            start=mapper.dest + overlap_start - mapper.source,
                            end=mapper.dest + overlap_end - mapper.source,
                        )
                    )
                    if seed.start < overlap_start:
                        # space in the beggining without overlap - add it as seed for future seed iteration
                        seeds.append(Seed(start=seed.start, end=overlap_start))
                    if overlap_end < seed.end:
                        # space in the end without overlap - add it as seed for future seed iteration
                        seeds.append(Seed(start=overlap_end, end=seed.end))
                    break
            else:
                # if the loop doesn't break, there's no match for this seed - stay the same
                next_seeds.append(Seed(start=seed.start, end=seed.end))

        # the next seeds are now converted values to the destination category, for example:
        # in the first category_block the next_seed will be soil
        # in the second category_block the next_seed will be fertilizer
        seeds = next_seeds
    return min([s.start for s in seeds])
