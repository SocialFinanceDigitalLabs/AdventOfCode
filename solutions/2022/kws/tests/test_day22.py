import pytest
from aoc_2022_kws.config import config
from aoc_2022_kws.day_22 import (
    BoardMap,
    Coordinate,
    CubeMap,
    Direction,
    Facing,
    MovementInstructions,
)


@pytest.fixture
def sample_map():
    input_data = (config.SAMPLE_DIR / "day22.txt").read_text()
    input_map, input_directions = input_data.split("\n\n")
    return BoardMap(input_map)


@pytest.fixture
def sample_cube():
    input_data = (config.SAMPLE_DIR / "day22.txt").read_text()
    input_map, input_directions = input_data.split("\n\n")
    return CubeMap(input_map, 4)


def test_start_pos(sample_map):
    assert sample_map.start_pos == Coordinate(8, 0)


def test_map_wrap(sample_map):
    start = sample_map.min_x(3)  # Minimum x value for y=3
    assert start == Coordinate(8, 3)
    assert sample_map.move(start, Facing.RIGHT, 1)[0] == Coordinate(start.x + 1, 3)
    assert sample_map.move(start, Facing.RIGHT, 3)[0] == Coordinate(start.x + 3, 3)
    assert sample_map.move(start, Facing.RIGHT, 4)[0] == start
    assert sample_map.move(start, Facing.RIGHT, 5)[0] == Coordinate(start.x + 1, 3)

    start = sample_map.max_x(3)  # Maximum x value for y=3
    assert start == Coordinate(11, 3)
    assert sample_map.move(start, Facing.LEFT, 1)[0] == Coordinate(start.x - 1, 3)
    assert sample_map.move(start, Facing.LEFT, 3)[0] == Coordinate(start.x - 3, 3)
    assert sample_map.move(start, Facing.LEFT, 4)[0] == start
    assert sample_map.move(start, Facing.LEFT, 5)[0] == Coordinate(start.x - 1, 3)

    start = sample_map.min_y(0)
    assert start == Coordinate(0, 4)
    assert sample_map.move(start, Facing.DOWN, 1)[0] == Coordinate(0, start.y + 1)
    assert sample_map.move(start, Facing.DOWN, 3)[0] == Coordinate(0, start.y + 3)
    assert sample_map.move(start, Facing.DOWN, 4)[0] == start
    assert sample_map.move(start, Facing.DOWN, 5)[0] == Coordinate(0, start.y + 1)

    start = sample_map.max_y(0)
    assert start == Coordinate(0, 7)
    assert sample_map.move(start, Facing.UP, 1)[0] == Coordinate(0, start.y - 1)
    assert sample_map.move(start, Facing.UP, 3)[0] == Coordinate(0, start.y - 3)
    assert sample_map.move(start, Facing.UP, 4)[0] == start
    assert sample_map.move(start, Facing.UP, 5)[0] == Coordinate(0, start.y - 1)


def test_blocked(sample_map):
    start = sample_map.min_x(0)
    assert start == Coordinate(8, 0)
    assert sample_map.move(start, Facing.RIGHT, 1)[0] == Coordinate(start.x + 1, 0)
    assert sample_map.move(start, Facing.RIGHT, 2)[0] == Coordinate(start.x + 2, 0)
    assert sample_map.move(start, Facing.RIGHT, 3)[0] == Coordinate(start.x + 2, 0)
    assert sample_map.move(start, Facing.RIGHT, 10)[0] == Coordinate(start.x + 2, 0)


def test_wrap_blocked(sample_map):
    start = sample_map.min_x(0)
    assert start == Coordinate(8, 0)
    assert sample_map.move(start, Facing.LEFT, 1)[0] == start

    start = Coordinate(3, 2)
    assert sample_map.move(start, Facing.RIGHT, 1)[0] == start

    start = Coordinate(3, 7)
    assert sample_map.move(start, Facing.DOWN, 1)[0] == start

    start = Coordinate(14, 8)
    assert sample_map.move(start, Facing.UP, 1)[0] == start


def test_move(sample_map):
    start = Coordinate(x=10, y=0)
    assert sample_map.move(start, Facing.DOWN, 5)[0] == Coordinate(x=10, y=5)


def test_heading_scores():
    assert Facing.RIGHT.score == 0
    assert Facing.DOWN.score == 1
    assert Facing.LEFT.score == 2
    assert Facing.UP.score == 3


def test_parse_directions():
    assert MovementInstructions.parse_directions("2R") == [
        MovementInstructions(Direction.RIGHT, 2)
    ]
    assert MovementInstructions.parse_directions("10L") == [
        MovementInstructions(Direction.LEFT, 10)
    ]

    assert MovementInstructions.parse_directions("2R10L15") == [
        MovementInstructions(Direction.RIGHT, 2),
        MovementInstructions(Direction.LEFT, 10),
        MovementInstructions(Direction.NONE, 15),
    ]


def test_cube_map_faces(sample_cube):
    assert sample_cube.face(Coordinate(8, 0)) == 1
    assert sample_cube.face(Coordinate(11, 3)) == 1

    assert sample_cube.face(Coordinate(0, 4)) == 2
    assert sample_cube.face(Coordinate(3, 7)) == 2

    assert sample_cube.face(Coordinate(4, 4)) == 3
    assert sample_cube.face(Coordinate(7, 7)) == 3

    assert sample_cube.face(Coordinate(8, 4)) == 4
    assert sample_cube.face(Coordinate(11, 7)) == 4

    assert sample_cube.face(Coordinate(8, 8)) == 5
    assert sample_cube.face(Coordinate(11, 11)) == 5

    assert sample_cube.face(Coordinate(12, 8)) == 6
    assert sample_cube.face(Coordinate(15, 11)) == 6


def assert_move(map, x, y, dir, expected_x, expected_y, expected_dir):
    start_pos = Coordinate(x, y)
    expected_pos = Coordinate(expected_x, expected_y)
    pos, facing = map.move(start_pos, dir, 1)
    if not (expected_pos == pos and expected_dir == facing):
        print()
        print(
            map.draw(
                {
                    start_pos: dir.symbol,
                    expected_pos: "E",
                    pos: facing.symbol,
                }
            )
        )
        return False
    return True


def test_cube_warp(sample_cube):
    sample_map = sample_cube

    assert assert_move(sample_map, 8, 0, Facing.UP, 8, 11, Facing.UP)
    assert assert_move(sample_map, 11, 0, Facing.UP, 11, 11, Facing.UP)

    assert assert_move(sample_map, 11, 0, Facing.RIGHT, 15, 11, Facing.LEFT)
    assert assert_move(sample_map, 11, 3, Facing.RIGHT, 15, 8, Facing.LEFT)
