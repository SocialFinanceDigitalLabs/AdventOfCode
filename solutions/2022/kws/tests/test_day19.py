from aoc_2022_kws.day_19 import Blueprint, Costs, Resources, Robots, State, find_options


def test_resource_accessor():
    r = Resources(ore=1, clay=2, obsidian=3, geode=4)
    assert r[Robots.ore] == 1
    assert r[Robots.clay] == 2
    assert r[Robots.obsidian] == 3
    assert r[Robots.geode] == 4


def test_resource_increment():
    r = Resources(ore=1, clay=2, obsidian=3, geode=4)
    r2 = Resources(ore=2)

    result = r + r2
    assert result == Resources(ore=3, clay=2, obsidian=3, geode=4)

    result = r + Resources(ore=2, clay=2)
    assert result == Resources(ore=3, clay=4, obsidian=3, geode=4)

    result = r + {Robots.geode: 2}
    assert result == Resources(ore=1, clay=2, obsidian=3, geode=6)

    state = State()
    assert state.resources.ore == 0

    state = state.increment(state.robots)
    assert state.resources.ore == 1

    state = state.increment(clay=1)
    assert state.resources.ore == 1
    assert state.resources.clay == 1


def test_parse_blueprint():
    bp = "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian."
    bp = Blueprint.parse(bp)

    assert bp.id == 1
    assert bp.cost.ore == Resources(ore=4)
    assert bp.cost.clay == Resources(ore=2)
    assert bp.cost.obsidian == Resources(ore=3, clay=14)
    assert bp.cost.geode == Resources(ore=2, obsidian=7)


def test_simple():
    bp = Blueprint.parse(
        "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian."
    )
    result, state_history = find_options(bp, (State(),), 24)
    assert result.geode == 9
