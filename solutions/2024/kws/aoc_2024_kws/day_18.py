import heapq
from collections import deque

import click
from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config
from aocd import submit
from rich.progress import Progress, track


def print_grid(grid_size, grid):
    for y in range(grid_size[1]):
        for x in range(grid_size[0]):
            if (x, y) in grid:
                print("#", end="")
            else:
                print(".", end="")
        print()


def find_all_paths(grid, grid_size, start, end):
    # Queue to store paths
    queue = deque([[start]])
    # Set to store all squares that are part of any path
    all_path_squares = set()

    while queue:
        path = queue.popleft()
        current_position = path[-1]

        if current_position == end:
            all_path_squares.update(path)
            continue

        x, y = current_position
        # Possible moves: up, down, left, right
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (x + dx, y + dy)
            if 0 <= neighbor[0] < grid_size[0] and 0 <= neighbor[1] < grid_size[1]:
                if grid.get(neighbor) != "#" and neighbor not in path:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)

    return all_path_squares


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day18(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day18.txt").read_text()
        grid_size = (7, 7)
        sample_size = 12
    else:
        input_data = (config.USER_DIR / "day18.txt").read_text()
        grid_size = (71, 71)
        sample_size = 1024

    input_data = input_data.splitlines()
    input_data = [tuple(map(int, line.split(","))) for line in input_data]

    data = input_data[:sample_size]
    print(data)

    grid = {(x, y): "#" for x, y in data}
    shortest_path = dijkstra(
        grid, grid_size, (0, 0), (grid_size[0] - 1, grid_size[1] - 1)
    )
    print(shortest_path)

    print_grid(grid_size, grid)

    if not sample:
        submit(shortest_path, part="a", day=18, year=2024)

    # A better solution to this broute-force approach would be to only check
    # bytes that fall withing the set of possible paths - however, this is quicker to implement...
    # Another alternative would be to 'home' in by bisected sampling.

    with Progress() as progress:
        task = progress.add_task("Processing", total=len(input_data))
        for pos in range(sample_size, len(input_data)):
            grid[input_data[pos]] = "#"
            shortest_path = dijkstra(
                grid, grid_size, (0, 0), (grid_size[0] - 1, grid_size[1] - 1)
            )
            if shortest_path is None:
                print("No path found at ", pos, input_data[pos])
                break
            progress.update(
                task,
                completed=pos,
                description=f"Processing {pos} - shortest path: {shortest_path}",
            )

    blocking_char = input_data[pos]
    print(f"After {pos}: {blocking_char}")

    if not sample:
        submit(f"{blocking_char[0]},{blocking_char[1]}", part="b", day=18, year=2024)

    print_grid(grid_size, grid)


def dijkstra(grid, grid_size, start, end):
    # Priority queue to store (cost, position)
    queue = [(0, start)]
    # Dictionary to store the minimum cost to reach each position
    costs = {start: 0}
    # Set to track visited nodes
    visited = set()

    while queue:
        current_cost, current_position = heapq.heappop(queue)

        if current_position in visited:
            continue

        visited.add(current_position)

        if current_position == end:
            return current_cost

        x, y = current_position
        # Possible moves: up, down, left, right
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (x + dx, y + dy)
            if 0 <= neighbor[0] < grid_size[0] and 0 <= neighbor[1] < grid_size[1]:
                if neighbor not in visited and grid.get(neighbor) != "#":
                    new_cost = current_cost + 1
                    if new_cost < costs.get(neighbor, float("inf")):
                        costs[neighbor] = new_cost
                        heapq.heappush(queue, (new_cost, neighbor))

    return None
