import os
from pprint import pprint
from typing import Optional

from util import FileParser

dir_path = os.path.dirname(os.path.realpath(__file__))

from dataclasses import dataclass
from enum import Enum

TOTAL_SPACE = 70000000
SPACE_NEEDED = 30000000
DIR_SIZE_LIMIT = 100000


class NodeType(Enum):
    DIR = "dir"
    FILE = "file"


@dataclass
class Node:
    node_type: NodeType
    name: str
    parent: Optional[int]
    size: int = 0


class FileSystem:
    def __init__(self, commands: list[str]) -> None:
        self.commands = commands
        self.nodes: dict[int, Node] = {
            0: Node(node_type=NodeType.DIR, name="/", parent=None)
        }
        self.current_pos = 0

    def is_command(self, command: str):
        return command.startswith("$")

    def add_parents_size(self, node: Node, size: int):
        parent = self.nodes.get(node.parent)
        if parent:
            parent.size += size
            self.add_parents_size(parent, size)

    def create_node(self, name: str, node_type: NodeType, size: int = 0) -> int:
        id = len(self.nodes)
        node = Node(node_type=node_type, name=name, parent=self.current_pos, size=size)
        self.nodes[id] = node
        if node_type == NodeType.FILE:
            self.add_parents_size(node, size)
        return id

    def update_nodes(self, entry: str):
        size_or_type, name = entry.split(" ")
        for node in self.nodes.values():
            if node.name == name and node.parent == self.current_pos:
                return

        if size_or_type == "dir":
            self.create_node(name, node_type=NodeType.DIR)
        else:
            self.create_node(name=name, node_type=NodeType.FILE, size=int(size_or_type))

    def apply_command(self, command: str):
        _command = command.split("$")[-1].strip()
        try:
            cmd, dest = _command.split(" ")
        except ValueError:
            # in case it's ls, we dont do nothing
            return
        # move up
        if dest == "..":
            self.current_pos = self.nodes[self.current_pos].parent
            return

        # move to next dir if exists
        for id, node in self.nodes.items():
            if node.name == dest and node.parent == self.current_pos:
                self.current_pos = id
                return

        # move to new next dir if it doesn't exist
        id = self.create_node(dest, node_type=NodeType.DIR)
        self.current_pos = id

    def fill_nodes(self):
        for entry in self.commands:
            if self.is_command(entry):
                self.apply_command(entry)
            else:
                self.update_nodes(entry)
        pprint(self.nodes)

    def calculate_dirs_size(self) -> int:
        dir_sizes = [
            node.size
            for node in self.nodes.values()
            if node.node_type == NodeType.DIR and node.size <= DIR_SIZE_LIMIT
        ]
        return sum(dir_sizes)

    def find_smallest_dir_to_delete(self) -> int:
        space_to_delete = SPACE_NEEDED - (TOTAL_SPACE - self.nodes[0].size)
        dir_sizes = [
            node.size for node in self.nodes.values() if node.node_type == NodeType.DIR
        ]
        dir_sizes.sort()
        for dir_size in dir_sizes:
            if dir_size >= space_to_delete:
                return dir_size


def part_1(file: str):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    commands = parser.read()
    file_system = FileSystem(commands)
    file_system.fill_nodes()
    return file_system.calculate_dirs_size()


def part_2(file: str):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    commands = parser.read()
    file_system = FileSystem(commands)
    file_system.fill_nodes()
    return file_system.find_smallest_dir_to_delete()
