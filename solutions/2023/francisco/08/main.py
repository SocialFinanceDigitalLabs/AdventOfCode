from util import FileParser
import os
from dataclasses import dataclass
import time
from tqdm import tqdm
import re
import math


dir_path = os.path.dirname(os.path.realpath(__file__))


def part_1(file: str):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    data = parser.read()
    directions = data[0]
    nodes = {
        v: (l, r) for v, l, r in (re.findall("[A-Z]{3}", line) for line in data[2:])
    }

    value = "AAA"
    i = 0
    while True:
        if value == "ZZZ":
            break
        d = directions[i % (len(directions))]
        value = nodes[value]["LR".index(d)]
        i += 1

    return i


def part_2(file):
    parser = FileParser(dir_path, file)
    data = parser.read()
    directions = data[0]
    nodes = {
        v: (l, r) for v, l, r in (re.findall("[A-Z]{3}", line) for line in data[2:])
    }

    values = [n for n in nodes.keys() if n[-1] == "A"]
    def count_steps(value):
        step = 0
        while True:
            if value[-1] == "Z":
                break
            d = directions[step % (len(directions))]
            value = nodes[value]["LR".index(d)]
            step += 1
        return step

    all_steps = [count_steps(value) for value in values]
    return math.lcm(*all_steps)
