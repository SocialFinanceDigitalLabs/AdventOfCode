
import click
from aocd import submit as aocd_submit

from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config

from rich import print
from rich.console import Console
from rich.text import Text

def print_grid_with_matches(grid, matches):
    console = Console()
    
    matched_positions = set()
    for match in matches:
        matched_positions.add(match['center'])
        matched_positions.update(match['positions'].values())

    for y in range(len(grid)):
        line = Text()
        for x in range(len(grid[0])):
            char = grid[y][x]
            if (x, y) in matched_positions:
                line.append(char, style="bold red1")
            else:
                line.append(char, style="green3")
        console.print(line)

             
                            
@main.command()
@click.option("--sample", "-s", is_flag=True)
@click.option("--submit", "-S", is_flag=True)
def day04(sample, submit):
    assert not(sample and submit), "You cannot submit the sample"
    if sample:
        input_data = (config.SAMPLE_DIR / "day04.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day04.txt").read_text()
        
    grid = input_data.splitlines()
    word = "XMAS"
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    directions = [
        (-1, -1),  # Northwest
        (-1, 0),   # West
        (-1, 1),   # Southwest
        (0, -1),   # North
        (0, 1),    # South
        (1, -1),   # Northeast
        (1, 0),    # East
        (1, 1)     # Southeast
    ]

    matches = []

    for y in range(height):
        for x in range(width):
            for dx, dy in directions:
                found = True
                for i in range(len(word)):
                    nx = x + dx * i
                    ny = y + dy * i
                    if nx < 0 or nx >= width or ny < 0 or ny >= height:
                        found = False
                        break
                    if grid[ny][nx] != word[i]:
                        found = False
                        break
                if found:
                    matches.append({
                        'start': (x, y),
                        'direction': (dx, dy)
                    })

    print(f"Total occurrences of '{word}': {len(matches)}")
    if submit:
        aocd_submit(len(matches), part="a", day=4, year=2024)
        
    directions = [
        (-1, -1),  # Northwest
        # (-1, 0),   # West
        (-1, 1),   # Southwest
        # (0, -1),   # North
        # (0, 1),    # South
        (1, -1),   # Northeast
        # (1, 0),    # East
        (1, 1)     # Southeast
    ]

    matches = []

    for y in range(height):
        for x in range(width):
            if grid[y][x] == 'A':
                for i in range(len(directions)):
                    dx1, dy1 = directions[i]
                    for j in range(i + 1, len(directions)):
                        dx2, dy2 = directions[j]

                        if dx1 == -dx2 and dy1 == -dy2:
                            continue

                        x_m1, y_m1 = x - dx1, y - dy1  # 'M'
                        x_s1, y_s1 = x + dx1, y + dy1  # 'S'

                        x_m2, y_m2 = x - dx2, y - dy2  # 'M'
                        x_s2, y_s2 = x + dx2, y + dy2  # 'S'

                        positions = [
                            (x_m1, y_m1), (x_s1, y_s1),
                            (x_m2, y_m2), (x_s2, y_s2)
                        ]
                        if any(px < 0 or px >= width or py < 0 or py >= height for px, py in positions):
                            continue

                        if (grid[y_m1][x_m1] == 'M' and grid[y_s1][x_s1] == 'S' and
                            grid[y_m2][x_m2] == 'M' and grid[y_s2][x_s2] == 'S'):
                            matches.append({
                                'center': (x, y),
                                'directions': [(dx1, dy1), (dx2, dy2)],
                                'positions': {
                                    'M1': (x_m1, y_m1),
                                    'S1': (x_s1, y_s1),
                                    'M2': (x_m2, y_m2),
                                    'S2': (x_s2, y_s2)
                                }
                            })

    print(f"Total occurrences of 'MAS in X': {len(matches)}")
    if submit:
        aocd_submit(len(matches), part="b", day=4, year=2024)

    print_grid_with_matches(grid, matches)

