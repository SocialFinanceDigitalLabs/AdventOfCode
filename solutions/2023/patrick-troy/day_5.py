from aocd import get_data
import re

session = "53616c7465645f5f5e959babee3b98732450e5a8dc2320e845ed91c80b7f39fe01f7" \
          "c01baa3710d5d1e1f631fe6c9f768fc1a035e9c3d5cd00e23c7ea0637cae"

data = get_data(day=5, year=2023, session=session).split("\n")

test = [
    "seeds: 79 14 55 13",
    "",
    "seed-to-soil map:",
    "50 98 2",
    "52 50 48",
    "",
    "soil-to-fertilizer map:",
    "0 15 37",
    "37 52 2",
    "39 0 15",
    "",
    "fertilizer-to-water map:",
    "49 53 8",
    "0 11 42",
    "42 0 7",
    "57 7 4",
    "",
    "water-to-light map:",
    "88 18 7",
    "18 25 70",
    "",
    "light-to-temperature map:",
    "45 77 23",
    "81 45 19",
    "68 64 13",
    "",
    "temperature-to-humidity map:",
    "0 69 1",
    "1 0 69",
    "",
    "humidity-to-location map:",
    "60 56 37",
    "56 93 4",
]


def solve_1(puzzle_input):
    seeds = {}
    seed_to_soil = {"seed_to_soil": []}
    soil_to_fertilizer = {}
    fertilizer_to_water = {}
    water_to_light = {}
    light_to_temperature = {}
    temperature_to_humidity = {}
    humidity_to_location = {}
    # for row in iter(puzzle_input):
    #     if "seeds" in row:
    #         seeds["seeds"] = re.findall(r"\d+", row)
    #     elif "seed-to-soil" in row:
    #         seed_to_soil["seed_to_soil"].append(re.findall(r"\d+", next(row)))

    row = iter(puzzle_input)
    for r in row:
        if "seeds" in row:
            seeds["seeds"] = re.findall(r"\d+", r)
        elif "seed-to-soil" in row:
            seed_to_soil["seed_to_soil"].append(re.findall(r"\d+", r))


    # print(seed_to_soil)


solve_1(test)
