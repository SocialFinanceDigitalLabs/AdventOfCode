from collections import Counter
from typing import Generator, Iterable, Literal, Set

import click
import trimesh.creation
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config
from trimesh import transformations


class Facet:
    def __init__(
        self, axis: Literal["x", "y", "z"], x: int, y: int, z: int, vector: int
    ):
        self.axis = axis
        self.x = x
        self.y = y
        self.z = z
        self.vector = vector

    def __repr__(self):
        return f"Facet({self.axis}, {self.x}, {self.y}, {self.z} [{self.vector}])"

    def __eq__(self, other):
        return (
            self.axis == other.axis
            and self.x == other.x
            and self.y == other.y
            and self.z == other.z
        )

    def __hash__(self):
        return hash((self.axis, self.x, self.y, self.z))


class Cube:
    def __init__(self, *args):
        if len(args) == 1:
            self.x, self.y, self.z = [int(i) for i in args[0].split(",")]
        else:
            self.x, self.y, self.z = args

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    @property
    def faces(self) -> Generator[Facet, None, None]:
        yield Facet("x", self.x, self.y, self.z, -1)
        yield Facet("x", self.x + 1, self.y, self.z, 1)
        yield Facet("y", self.x, self.y, self.z, -1)
        yield Facet("y", self.x, self.y + 1, self.z, 1)
        yield Facet("z", self.x, self.y, self.z, -1)
        yield Facet("z", self.x, self.y, self.z + 1, 1)

    @property
    def mesh(self):
        move = transformations.translation_matrix(
            (self.x + 0.5, self.y + 0.5, self.z + 0.5)
        )
        return trimesh.creation.box(extents=(1, 1, 1), transform=move)

    def exterior(self, cubes: Set["Cube"]):
        if set(self.neighbours) - set(cubes):
            return True

    def neighbour(self, x=0, y=0, z=0):
        return Cube(self.x + x, self.y + y, self.z + z)

    @property
    def neighbours(self):
        return [
            self.neighbour(x=-1),
            self.neighbour(x=1),
            self.neighbour(y=-1),
            self.neighbour(y=1),
            self.neighbour(z=-1),
            self.neighbour(z=1),
        ]


def calculate_bounding_box(cubes: Iterable[Cube]):
    x_min = y_min = z_min = 0
    x_max = y_max = z_max = 0

    for cube in cubes:
        x_min = min(x_min, cube.x)
        y_min = min(y_min, cube.y)
        z_min = min(z_min, cube.z)
        x_max = max(x_max, cube.x)
        y_max = max(y_max, cube.y)
        z_max = max(z_max, cube.z)

    return x_min, y_min, z_min, x_max, y_max, z_max


@main.command()
@click.option("--sample", "-s", is_flag=True)
@click.option("--save", type=click.Path(dir_okay=False), default=None)
@click.option("--view", is_flag=True)
def day18(sample, save, view):
    if sample:
        input_data = (config.SAMPLE_DIR / "day18.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day18.txt").read_text()

    cubes = [Cube(line) for line in input_data.splitlines()]

    if save:
        combined = trimesh.util.concatenate([c.mesh for c in cubes])
        combined.export(save)

    if view:
        combined = trimesh.util.concatenate([c.mesh for c in cubes])
        combined.show()

    if view or save:
        return

    # Part 1
    all_faces = []
    for c in cubes:
        all_faces.extend(c.faces)

    face_counts = Counter(all_faces)
    covered_faces = set([f for f, c in face_counts.items() if c > 1])
    surface_faces = set(all_faces) - covered_faces

    print("Part 1", len(surface_faces))

    #######################################
    # Part 2                              #
    #######################################

    x_min, y_min, z_min, x_max, y_max, z_max = calculate_bounding_box(cubes)
    print("Bounding box", x_min, y_min, z_min, x_max, y_max, z_max)

    void_cubes = set()
    for x in range(x_min - 1, x_max + 2):
        for y in range(y_min - 1, y_max + 2):
            for z in range(z_min - 1, z_max + 2):
                my_cube = Cube(x, y, z)
                if not my_cube in cubes:
                    void_cubes.add(my_cube)

    print("Void cubes", len(void_cubes))

    whole_area = set(cubes) | set(void_cubes)
    print("Before", len(whole_area))

    to_remove: Set | None = None
    while to_remove is None or len(to_remove) > 0:
        if to_remove:
            whole_area -= to_remove
        to_remove = set()
        for my_cube in whole_area & void_cubes:
            if my_cube in void_cubes and my_cube.exterior(whole_area):
                to_remove.add(my_cube)

    internal_void_cubes = set([c for c in whole_area if c in void_cubes])
    print("After", len(internal_void_cubes))

    internal_faces = set(f for c in internal_void_cubes for f in c.faces)

    external_faces = surface_faces - internal_faces

    print("Part 2", len(external_faces))
