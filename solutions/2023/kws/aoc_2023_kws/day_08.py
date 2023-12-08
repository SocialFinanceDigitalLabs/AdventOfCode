import click
from aoc_2023_kws.cli import main
from aoc_2023_kws.config import config
from aocd import submit


class Instructions:
    def __init__(self, input_data) -> None:
        self._input_data = input_data
        self._pos = 0

    @property
    def current(self):
        return self._input_data[self._pos]

    @property
    def next(self):
        self._pos += 1
        self._pos %= len(self._input_data)
        return self.current


class Node:
    def __init__(self, value) -> None:
        self.node_id = value[0:3]
        self.left_node = value[7:10]
        self.right_node = value[12:15]

        assert len(self.node_id) == 3, f"Incorrect node id: {self.node_id}"

    @property
    def dead_end(self):
        return self.left_node == self.right_node == self.node_id

    def __repr__(self) -> str:
        return f"{self.node_id} -> L->{self.left_node} R->{self.right_node}"


class Grid:
    def __init__(self, input_data) -> None:
        nodes = [Node(line) for line in input_data if line]
        self.nodes = {node.node_id: node for node in nodes}
        self.current_node = nodes[0]

    @property
    def current(self):
        return self.current_node

    def goto(self, node_id):
        self.current_node = self.nodes[node_id]

    def go_left(self):
        self.current_node = self.nodes[self.current_node.left_node]

    def go_right(self):
        self.current_node = self.nodes[self.current_node.right_node]


class Ghost:
    def __init__(self, name, grid, start_node) -> None:
        self.name = name
        self.grid = grid
        self.grid.goto(start_node)
        self.step = 0
        self._last_z = -1
        self._intervals = []

    def go_left(self):
        self.grid.go_left()
        self.go()

    def go_right(self):
        self.grid.go_right()
        self.go()

    @property
    def at_end(self):
        return self.grid.current.node_id[2] == "Z"

    def go(self):
        self.step += 1
        if not self.at_end:
            return

        if self._last_z == -1:
            self._last_z = self.step
            return

        interval = self.step - self._last_z
        self._last_z = self.step
        self._intervals.append(interval)

    @property
    def looping(self):
        return len(self._intervals) > 2 and len(set(self._intervals)) == 1


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day08(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day08-1.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day08.txt").read_text()

    input_data = input_data.splitlines()

    instructions = Instructions(input_data[0])
    grid = Grid(input_data[1:])

    target = "ZZZ"
    step = 0
    grid.goto("AAA")
    while grid.current.node_id != target:
        step += 1
        if instructions.current == "L":
            grid.go_left()
        else:
            grid.go_right()
        instructions.next

    print(f"Found {target} in {step} steps")

    # Part 2
    if sample:
        input_data = (config.SAMPLE_DIR / "day08-2.txt").read_text().splitlines()
        instructions = Instructions(input_data[0])
        grid = Grid(input_data[1:])

    start_nodes = [id for id in grid.nodes.keys() if id[2] == "A"]
    ghosts = [
        Ghost(f"Ghost {ix+1}", Grid(input_data[1:]), node)
        for ix, node in enumerate(start_nodes)
    ]

    step = 0

    while not all([ghost.at_end for ghost in ghosts]):
        step += 1
        if step % 1_000_000 == 0:
            print(f"{step}: {[ghost.grid.current.node_id for ghost in ghosts]}")

        for ghost in ghosts:
            if instructions.current == "L":
                ghost.go_left()
            else:
                ghost.go_right()
        instructions.next

        if any([ghost.grid.current.dead_end for ghost in ghosts]):
            print("Dead end")
            break

        if all([ghost.looping for ghost in ghosts]):
            print("Looping")
            break

    for g in ghosts:
        print(g.name, g._intervals)

    import math

    periods = [g._intervals[-1] for g in ghosts]
    lcm = math.lcm(*periods)
    print(f"Found {lcm} steps")
