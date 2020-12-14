# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 09:58:47 2020

@author: celine.gross
"""

import re

with open('input_day14.txt', 'r') as file:
    puzzle = [line.strip() for line in file]


# Part 1

def parse(mask, exclude):
    mask = mask.split(' = ')[1]
    mask = {i:char for i, char in enumerate(mask) if char != exclude}
    return mask


def extract(memory):
    regex = r"mem\[(\d+)\] = (\d+)"
    index = int(re.search(regex, memory).group(1))
    number = int(re.search(regex, memory).group(2))
    return index, number


def apply_mask(mask, number):
    number = list(f'{number:036b}')
    for k,v in mask.items():
        number[k]=v
    return "".join(number)


def update_memory(instructions):
    memory = {}
    for line in instructions:
        if 'mask' in line:
            mask = parse(line, 'X')
        else:
            index, number = extract(line)
            masked_number = apply_mask(mask, number)
            memory[index] = int(masked_number, 2)
    return memory


def run(instructions):
    memory = update_memory(instructions)
    return sum([v for k, v in memory.items()])


print(run(puzzle))


# Part 2

def apply_mask(mask, index):
    index = list(f'{index:036b}')
    for k,v in mask.items():
        index[k]=v
    return "".join(index)


def generate(index):
    # Base case
    if 'X' not in index:
        return [index]
    # Other cases
    x = index.find('X')
    string1 = index[:x] + '0' + index[x+1:]
    string2 = index[:x] + '1' + index[x+1:]
    branch1 = generate(string1)
    branch2 = generate(string2)
    return branch1 + branch2


def update_memory(instructions):
    memory = {}
    for line in instructions:
        if 'mask' in line:
            mask = parse(line, '0')
        else:
            index, number = extract(line)
            indexes = generate(apply_mask(mask, index))
            for i in indexes:
                memory[int(i, 2)] = number
    return memory

print(run(puzzle))