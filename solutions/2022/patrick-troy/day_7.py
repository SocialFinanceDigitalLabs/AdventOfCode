from aocd import get_data
import re

session = "53616c7465645f5f932620b9dd9cb53e9facee9282730977ff26a7c28126db6fa8ce7b0" \
          "329cbec99fa54ea4d10b35d0cb2d5b3d17492e51cf4a0282caf0025e1"

directory_browsing = get_data(day=7, year=2022, session=session).split("\n")


class Tree:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.size = 0
        self.nodes = []

    def add_node(self, name=None, parent=None):
        node = Tree(name, parent)
        self.nodes.append(node)

    def add_data(self, name, parent, size):
        data = Data(name, parent, size)
        self.nodes.append(data)

    def get_dir(self, name):
        for node in self.nodes:
            if node.name == name:
                return node

    def update_size(self, size):
        self.size += size
        if self.parent:
            self.parent.update_size(size)


class Data:
    def __init__(self, name, parent, size):
        self.name = name
        self.parent = parent
        self.size = size
        parent.update_size(self.size)


def change_directory(directory_command, tree, parent=None):
    directory = directory_command.split()[2]
    match directory:
        case "..":
            new_directory = parent.parent
        case "/":
            new_directory = tree
        case _:
            new_directory = parent.get_dir(directory)
    return new_directory


def size_from_file(file_name):
    size = re.match(r"^\d*", file_name.split()[0]).group(0)
    return int(size) if size else None


def commands_to_directories(commands):
    tree = Tree("/")
    parent = None
    for command in commands:
        if "$ cd" in command:
            parent = change_directory(command, tree, parent)
        if "$ ls" in command:
            continue
        if command.split()[0] == "dir":
            parent.add_node(name=command.split()[1], parent=parent)
        if size_from_file(command) is not None:
            parent.add_data(name=command, parent=parent, size=size_from_file(command))
    return tree


def find_directory_size(directory, limit, greater_than, result):
    if greater_than and directory.size >= limit or not greater_than and directory.size <= limit:
        result.append(directory)
    for node in directory.nodes:
        if isinstance(node, Tree):
            result = find_directory_size(node, limit, greater_than, result)
    return result


complete_tree = commands_to_directories(directory_browsing)

total = 0
for node in find_directory_size(complete_tree, 100000, False, []):
    total += node.size

print(total)


total_space = 70000000
space_required = 30000000
total_size = complete_tree.size
free_space = total_space - total_size
min_file_to_delete = space_required - free_space

directory_size = 0
for node in find_directory_size(complete_tree, min_file_to_delete, True, []):
    if node.size <= directory_size or directory_size == 0:
        directory_size = node.size

print(directory_size)
