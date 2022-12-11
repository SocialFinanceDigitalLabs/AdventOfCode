from collections import namedtuple

import click
from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config

File = namedtuple("File", "name, size")


class Folder:
    def __init__(self, name, parent):
        self.__name = name
        self.__parent = parent
        self.__children = {}

    @property
    def name(self):
        return self.__name

    @property
    def parent(self):
        return self.__parent

    @property
    def children(self):
        return self.__children.values()

    @property
    def all(self):
        for c in self.children:
            yield c
            if isinstance(c, Folder):
                yield from c.all

    def __getitem__(self, item):
        return self.__children[item]

    @property
    def size(self):
        return sum([c.size for c in self.__children.values()])

    def add(self, line):
        part, name = line.split(" ", 1)
        if part == "dir":
            self.__children[name] = Folder(name, self)
        else:
            self.__children[name] = File(name, int(part))


@main.command()
@click.option("--sample", "-s", is_flag=True)
@click.option("--input", "-i", "input_file", type=click.File("rt"))
def day07(sample, input_file):
    assert not (sample and input_file), "Only one of sample or input_file can be set"
    if input_file:
        input_data = input_file.read()
    elif sample:
        input_data = (config.SAMPLE_DIR / "day07.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day07.txt").read_text()
    root = parse_files(input_data)

    all_small_folders = [
        f for f in root.all if isinstance(f, Folder) and f.size <= 100_000
    ]

    print("Part 1", sum([f.size for f in all_small_folders]))

    total_size = 70_000_000
    target_size = 30_000_000
    current_size = root.size

    to_clean = target_size - (total_size - current_size)

    possible_folders = [
        f for f in root.all if isinstance(f, Folder) and f.size >= to_clean
    ]
    possible_folders.sort(key=lambda f: f.size)

    print("Part 2", possible_folders[0].name, possible_folders[0].size)


def parse_files(input_data):
    current_dir = root = Folder("", parent=None)
    for line in input_data.splitlines():
        if line.startswith("$ cd "):
            folder = line[5:]
            if folder == "/":
                current_dir = root
            elif folder == "..":
                current_dir = current_dir.parent
            else:
                current_dir = current_dir[folder]
        elif line.startswith("$"):
            pass
        else:
            current_dir.add(line)

    return root
