import pytest
from aoc_2022_kws.config import config
from aoc_2022_kws.day_22 import (
    BoardMap,
    Coordinate,
    CubeFace,
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
    return CubeMap(input_map)


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
    assert sample_cube.face(Coordinate(8, 0)).id == 1
    assert sample_cube.face(Coordinate(11, 3)).id == 1

    assert sample_cube.face(Coordinate(0, 4)).id == 2
    assert sample_cube.face(Coordinate(3, 7)).id == 2

    assert sample_cube.face(Coordinate(4, 4)).id == 3
    assert sample_cube.face(Coordinate(7, 7)).id == 3

    assert sample_cube.face(Coordinate(8, 4)).id == 4
    assert sample_cube.face(Coordinate(11, 7)).id == 4

    assert sample_cube.face(Coordinate(8, 8)).id == 5
    assert sample_cube.face(Coordinate(11, 11)).id == 5

    assert sample_cube.face(Coordinate(12, 8)).id == 6
    assert sample_cube.face(Coordinate(15, 11)).id == 6


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
        print(expected_pos, pos)
        print(expected_dir, facing)
        return False
    return True


def test_cube_warp(sample_cube):
    sample_map = sample_cube

    assert assert_move(sample_map, 8, 0, Facing.UP, 8, 0, Facing.UP)  # Blocked
    assert assert_move(sample_map, 11, 0, Facing.UP, 0, 4, Facing.DOWN)

    assert assert_move(sample_map, 11, 0, Facing.RIGHT, 15, 11, Facing.LEFT)
    assert assert_move(sample_map, 11, 3, Facing.RIGHT, 15, 8, Facing.LEFT)

    assert assert_move(sample_map, 11, 3, Facing.DOWN, 11, 3, Facing.DOWN)  # Blocked
    assert assert_move(sample_map, 8, 3, Facing.DOWN, 8, 4, Facing.DOWN)

    assert assert_move(sample_map, 8, 3, Facing.LEFT, 7, 4, Facing.DOWN)
    assert assert_move(sample_map, 8, 0, Facing.LEFT, 4, 4, Facing.DOWN)


def test_dimensions(sample_cube):
    assert sample_cube.max_x == 15
    assert sample_cube.dimensions == 4

    assert sample_cube.faces[1].min_x == 8
    assert sample_cube.faces[1].max_x == 11
    assert sample_cube.faces[1].min_y == 0
    assert sample_cube.faces[1].max_y == 3

    assert Coordinate(8, 0) in sample_cube.faces[1]

    assert sample_cube.faces[2].min_x == 0
    assert sample_cube.faces[2].max_x == 3
    assert sample_cube.faces[2].min_y == 4
    assert sample_cube.faces[2].max_y == 7
    assert Coordinate(1, 5) in sample_cube.faces[2]

    input_data = (config.USER_DIR / "day22.txt").read_text()
    input_map, input_directions = input_data.split("\n\n")
    cube = CubeMap(input_map)

    assert cube.max_x == 149
    assert cube.dimensions == 50
    assert cube.faces[1].min_x == 50
    assert cube.faces[1].max_x == 99

    assert cube.min_x(0) == Coordinate(50, 0)

    assert cube.start_pos == Coordinate(50, 0)


def test_connections(sample_cube):
    for face_id in range(1, 7):
        face = sample_cube.faces[face_id]
        assert face.id == face_id
        for heading in Facing:
            other_face = face.connection(heading)
            assert other_face is not None
            assert other_face.heading(face) is not None


def test_diagonal():
    faces = [CubeFace(i, 0, 0, 0) for i in range(1, 7)]
    faces = {f.id: f for f in faces}

    faces[1].add_connection(Facing.DOWN, faces[4], Facing.UP)
    faces[4].add_connection(Facing.LEFT, faces[3], Facing.RIGHT)

    other, facing = faces[1].diagonal(Facing.LEFT, Direction.RIGHT)
    assert other is None

    other, facing = faces[1].diagonal(Facing.LEFT, Direction.LEFT)
    assert other.id == 3
    assert facing == Facing.UP

    faces[4].add_connection(Facing.RIGHT, faces[6], Facing.UP)

    other, facing = faces[1].diagonal(Facing.RIGHT, Direction.RIGHT)
    assert other.id == 6
    assert facing == Facing.RIGHT

    other, facing = faces[4].diagonal(Facing.UP, Direction.RIGHT)
    assert other is None

    faces[6].add_connection(Facing.RIGHT, faces[1], Facing.RIGHT)

    other, facing = faces[4].diagonal(Facing.UP, Direction.RIGHT)
    assert other.id is 1
    assert facing == Facing.DOWN
