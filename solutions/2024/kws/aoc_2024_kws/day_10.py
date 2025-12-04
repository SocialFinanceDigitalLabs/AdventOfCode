import click
from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config
from aocd import submit


class Map:
    def __init__(self, input_data):
        self.map = map = input_data.splitlines()
        self.width = len(map[0])
        self.height = len(map)

        for y in range(self.height):
            self.map[y] = [int(c) for c in self.map[y]]

    def find_points_with_height(self, height):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == height:
                    yield (x, y, height)

    def get_neighbors(self, x, y):
        """Get valid neighboring positions that are one height higher."""
        current_height = self.map[y][x]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (
                0 <= new_x < self.width
                and 0 <= new_y < self.height
                and self.map[new_y][new_x] == current_height + 1
            ):
                yield (new_x, new_y)

    def count_reachable_nines(self, start_x, start_y, visited=None):
        """Count number of unique 9s reachable from the starting position."""
        if visited is None:
            visited = set()

        pos_key = (start_x, start_y)
        if pos_key in visited:
            return set()

        visited.add(pos_key)
        current_height = self.map[start_y][start_x]

        # If we've found a 9, return its position
        if current_height == 9:
            return {pos_key}

        # Collect all reachable 9s from this position
        reachable_nines = set()
        for next_x, next_y in self.get_neighbors(start_x, start_y):
            reachable_nines.update(self.count_reachable_nines(next_x, next_y, visited))

        return reachable_nines

    def count_routes_to_nines(self, start_x, start_y, visited=None):
        """Count number of routes to reach a 9 from the starting position."""
        if visited is None:
            visited = set()

        pos_key = (start_x, start_y)
        if pos_key in visited:
            return 0

        visited.add(pos_key)
        current_height = self.map[start_y][start_x]

        # If we've reached a 9, return 1 route
        if current_height == 9:
            visited.remove(pos_key)  # Allow revisiting this node in different paths
            return 1

        # Collect all routes to reach a 9 from this position
        routes_to_nines = 0
        for next_x, next_y in self.get_neighbors(start_x, start_y):
            routes_to_nines += self.count_routes_to_nines(next_x, next_y, visited)

        visited.remove(pos_key)  # Allow revisiting this node in different paths
        return routes_to_nines

    def mark_all_trails(self):
        """Mark all trails on the map."""
        trail_map = [[" " for _ in range(self.width)] for _ in range(self.height)]

        def dfs(x, y, visited):
            if (x, y) in visited:
                return
            visited.add((x, y))
            trail_map[y][x] = "*"  # Mark the trail with a flag
            for next_x, next_y in self.get_neighbors(x, y):
                dfs(next_x, next_y, visited)

        for x, y, _ in self.find_points_with_height(0):
            visited = set()
            dfs(x, y, visited)

        # Combine the height and trail marker
        combined_map = [
            [f"{self.map[y][x]}{trail_map[y][x]}" for x in range(self.width)]
            for y in range(self.height)
        ]

        return combined_map

    def save_trail_map(self, trail_map, filename):
        """Save the trail map to a file."""
        with open(filename, "w") as f:
            for row in trail_map:
                f.write(" ".join(row) + "\n")


@main.command()
@click.option("--sample", "-s", is_flag=True)
@click.option(
    "--export-trail",
    "-e",
    type=click.Path(file_okay=True, dir_okay=False, writable=True),
    help="Full path to export the map with trails marked.",
)
def day10(sample, export_trail):
    if sample:
        input_data = (config.SAMPLE_DIR / "day10.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day10.txt").read_text()

    map = Map(input_data)

    # For each trail head (height 0), count how many unique 9s it can reach
    trail_head_counts = {}
    for x, y, _ in map.find_points_with_height(0):
        reachable_nines = map.count_reachable_nines(x, y)
        trail_head_counts[(x, y)] = len(reachable_nines)

    max_nines = sum(trail_head_counts.values())
    print("Total unique 9s reachable:", max_nines)

    if not sample:
        submit(max_nines, part="a", day=10, year=2024)

    # For each trail head (height 0), count how many routes can reach a 9
    trail_head_routes = {}
    for x, y, _ in map.find_points_with_height(0):
        routes_to_nines = map.count_routes_to_nines(x, y)
        trail_head_routes[(x, y)] = routes_to_nines

    total_routes = sum(trail_head_routes.values())
    print("Total routes to reach a 9:", total_routes)

    if not sample:
        submit(total_routes, part="b", day=10, year=2024)

    if export_trail:
        trail_map = map.mark_all_trails()
        map.save_trail_map(trail_map, export_trail)
        print(f"Trail map exported to {export_trail}.")
