from collections import defaultdict
import click
from aocd import submit

from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config

import re
import math
ANTENNA_PATTERN = re.compile(r"[a-zA-Z0-9]")
             
                            
@main.command()
@click.option("--sample", "-s", is_flag=True)
def day08(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day08.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day08.txt").read_text()

    input_data = input_data.splitlines()
    map_height = len(input_data)
    map_width = len(input_data[0])


    antenna_positions = []

    for y in range(map_height):
        for x in range(map_width):
            char = input_data[y][x] 
            if ANTENNA_PATTERN.match(char):
                antenna_positions.append((char, x, y))

    by_letter = defaultdict(list)
    for antenna in antenna_positions:
        by_letter[antenna[0]].append(antenna)
    
    antinodes = []
    for letter, positions in by_letter.items():
        if len(positions) > 1:
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    pos1 = positions[i]
                    pos2 = positions[j]
                    x1, y1 = pos1[1], pos1[2]
                    x2, y2 = pos2[1], pos2[2]
                    dx, dy = x2 - x1, y2 - y1
                    antinodes.append((letter, x1 - dx, y1 - dy))
                    antinodes.append((letter, x2 + dx, y2 + dy))

    antinodes = [
        (letter, x, y) for letter, x, y in antinodes 
        if 0 <= x < map_width and 0 <= y < map_height
    ]

    antinode_locations = {(x, y) for _, x, y in antinodes}

    print(len(antinode_locations))
    for x, y in sorted(antinode_locations, key=lambda x: (x[1], x[0])):
        print(f"{x}, {y}")

    if not sample:
        submit(len(antinode_locations), part="a", day=8, year=2024)


    antinode_locations = set()
    for letter, positions in by_letter.items():
        if len(positions) > 1:
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    x1, y1 = positions[i][1], positions[i][2]
                    x2, y2 = positions[j][1], positions[j][2]
                    dx, dy = x2 - x1, y2 - y1
                    if dx == 0:
                        dy = 1
                    elif dy == 0:
                        dx = 1
                    else:
                        gcd = math.gcd(dx, dy)
                        dx //= gcd
                        dy //= gcd
                    
                    line_positions = set()
                    
                    curr_x, curr_y = x1, y1
                    while 0 <= curr_x < map_width and 0 <= curr_y < map_height:
                        line_positions.add((curr_x, curr_y))
                        curr_x += dx
                        curr_y += dy
                    
                    curr_x, curr_y = x1 - dx, y1 - dy
                    while 0 <= curr_x < map_width and 0 <= curr_y < map_height:
                        line_positions.add((curr_x, curr_y))
                        curr_x -= dx
                        curr_y -= dy
                    
                    antinode_locations.update(line_positions)

    if not sample:
        submit(len(antinode_locations), part="b", day=8, year=2024)

    # for y in range(map_height):
    #     for x in range(map_width):
    #         if (x, y) in antinode_locations:
    #             print("#", end="")
    #         else:
    #             print(input_data[y][x], end="")
    #     print()
