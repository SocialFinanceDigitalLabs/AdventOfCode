# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 09:58:47 2020

@author: celine.gross
"""

import re

with open('input_day14.txt', 'r') as file:
    puzzle = [line.strip() for line in file]


# Part 1

def parse(mask):
    mask = mask.split(' = ')[1]
    mask = {i:char for i, char in enumerate(mask) if char != 'X'}
    return mask


def extract(memory):
    regex = r"mem\[(\d+)\] = (\d+)"
    index = re.search(regex, memory).group(1)
    number = int(re.search(regex, memory).group(2))
    return index, f'{number:036b}'


def apply_mask(mask, number):
    number = list(number)
    for k,v in mask.items():
        number[k]=v
    return "".join(number)


def update_memory(instructions):
    memory = {}
    for line in instructions:
        if 'mask' in line:
            mask = parse(line)
        else:
            index, number = extract(line)
            masked_number = apply_mask(mask, number)
            memory[index] = int(masked_number, 2)
    return memory


def run(instructions):
    memory = update_memory(instructions)
    return sum([v for k, v in memory.items()])


print(run(puzzle))