import math
import re
import sys
from enum import Enum
from typing import Iterable, List, NamedTuple, Set, Tuple

import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config


class Robots(Enum):
    ore = 1
    clay = 2
    obsidian = 3
    geode = 4


class Resources(NamedTuple):
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    @classmethod
    def parse(cls, resources: str) -> "Resources":
        costs = {
            m[1]: int(m[0])
            for m in re.findall(r"(\d+) (ore|clay|obsidian|geode)", resources)
        }
        return cls(**costs)

    def __repr__(self):
        return f"{self.ore}o {self.clay}c {self.obsidian}ob {self.geode}g"

    def __getitem__(self, robot: Robots):
        return getattr(self, robot.name)

    def __add__(self, other):
        if isinstance(other, Resources):
            return Resources(
                ore=self.ore + other.ore,
                clay=self.clay + other.clay,
                obsidian=self.obsidian + other.obsidian,
                geode=self.geode + other.geode,
            )
        else:
            return Resources(
                ore=self.ore + other.get(Robots.ore, 0),
                clay=self.clay + other.get(Robots.clay, 0),
                obsidian=self.obsidian + other.get(Robots.obsidian, 0),
                geode=self.geode + other.get(Robots.geode, 0),
            )

    def __sub__(self, other):
        if isinstance(other, Resources):
            return Resources(
                ore=self.ore - other.ore,
                clay=self.clay - other.clay,
                obsidian=self.obsidian - other.obsidian,
                geode=self.geode - other.geode,
            )
        else:
            return Resources(
                ore=self.ore - other.get(Robots.ore, 0),
                clay=self.clay - other.get(Robots.clay, 0),
                obsidian=self.obsidian - other.get(Robots.obsidian, 0),
                geode=self.geode - other.get(Robots.geode, 0),
            )


class Costs(NamedTuple):
    ore: Resources
    clay: Resources
    obsidian: Resources
    geode: Resources

    def __getitem__(self, robot: Robots):
        return getattr(self, robot.name)


class Blueprint(NamedTuple):
    id: int
    cost: Costs
    targets: Resources = Resources()

    @classmethod
    def parse(cls, blueprint: str) -> "Blueprint":
        match = re.search(r"Blueprint (\d+)", blueprint)
        bp_id = int(match.group(1))
        costs = {
            m[0]: Resources.parse(m[1])
            for m in re.findall(r"Each (\w+) robot costs (.*?)\.", blueprint)
        }
        costs = Costs(**costs)

        # We make some estimates of how many of each resource we need to make
        # These are inspired by optimisations others have done,
        # in particularly https://pastebin.com/KDTmtHCk
        targets = Resources(
            ore=max(costs.clay.ore, costs.obsidian.ore, costs.geode.ore),
            clay=max(costs.obsidian.clay, costs.geode.clay),
            obsidian=costs.geode.obsidian,
            geode=sys.maxsize,
        )

        return Blueprint(id=bp_id, cost=costs, targets=targets)


class State(NamedTuple):
    resources: Resources = Resources()
    robots: Resources = Resources(ore=1)
    ignored: frozenset[str] = frozenset()

    def __gt__(self, other):
        return self.resources.geode > other.resources.geode

    def __repr__(self):
        return f"<State resources={self.resources} robots={self.robots}>"

    def increment(self, *args, **kwargs):
        if args and isinstance(args[0], Resources):
            new_resources = self.resources + args[0]
        else:
            new_resources = self.resources + Resources(**kwargs)
        return State(new_resources, self.robots, self.ignored)

    @property
    def as_dict(self):
        return dict(resources=self.resources, robots=self.robots, ignored=self.ignored)

    def update(self, **kwargs):
        return State(**{**self.as_dict, **kwargs})


def find_options(
    blueprint: Blueprint, prior_states: Tuple[State], timelimit: int
) -> Tuple[Resources, Iterable[State]]:
    time_remaining = timelimit - len(prior_states)
    curr_state = prior_states[-1]
    if time_remaining < 0:
        return curr_state.resources, prior_states

    options: Set[Robots] = set()

    for robot in Robots:
        can_afford = all(
            curr_state.resources[r] >= blueprint.cost[robot][r] for r in Robots
        )

        need = curr_state.robots[robot] < blueprint.targets[robot]

        # We ignore robots we have skipped in an earlier step. We're presumably saving up for something.
        not_ignored = robot not in curr_state.ignored

        if can_afford and need and not_ignored:
            options.add(robot)

    if Robots.geode in options:
        options = {Robots.geode}  # Prioritise above all else
    elif time_remaining < 1:  # Game over
        options.clear()
    else:
        # These are inspired by optimisations others have done,
        # in particularly https://pastebin.com/KDTmtHCk
        if (
            curr_state.robots.clay > 3
            or curr_state.robots.obsidian > 0
            or Robots.obsidian in options
        ):
            options.discard(Robots.ore)

        if (
            curr_state.robots.obsidian > 3
            or curr_state.robots.geode > 0
            or Robots.geode in options
        ):
            options.discard(Robots.clay)

    # We can decide to do nothing and just wait for the next turn
    next_state: State = curr_state.increment(curr_state.robots)

    results = [
        find_options(
            blueprint,
            prior_states + (next_state.update(ignored=curr_state.ignored | options),),
            timelimit,
        )
    ]

    for opt in options:
        option_state = next_state.update(
            robots=curr_state.robots + {opt: 1},
            resources=next_state.resources - blueprint.cost[opt],
            ignored=frozenset(),
        )
        results.append(
            find_options(blueprint, prior_states + (option_state,), timelimit)
        )

    return max(results, key=lambda x: x[0].geode)


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day19(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day19.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day19.txt").read_text()

    blueprints = [Blueprint.parse(line) for line in input_data.splitlines()]

    all_results = []
    for bp in blueprints:
        print("Processing Blueprint", bp.id)
        result, state_history = find_options(bp, (State(),), 24)
        print(f"  Produced {result.geode} geodes")
        all_results.append(result.geode * bp.id)

    print("Part 1", sum(all_results))

    all_results = []
    blueprints = blueprints[0:3]
    for bp in blueprints:
        print("Processing Blueprint", bp.id)
        result, state_history = find_options(bp, (State(),), 32)

        print(f"  Produced {result.geode} geodes")
        all_results.append(result.geode)

    print("Part 2", math.prod(all_results))
