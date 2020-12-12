# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 15:26:31 2020

@author: celine.gross
"""

with open('input_day12.txt', 'r') as file:
    puzzle = [line.strip() for line in file]
    puzzle = [(line[0], int(line[1:])) for line in puzzle]


# Part 1

def implement_instruction(instruction, position=None):
   
    if position is None:
        position={'E':0, 'W':0,'N':0, 'S':0, 'facing':'E'}
   
    if instruction[0] in ['E', 'W', 'N', 'S']:
        position[instruction[0]] += instruction[1]
    
    elif instruction[0] == 'F':
        position[position['facing']] += instruction[1]
    
    elif instruction[0] == 'R':
        position['facing'] = 'NESW'[('NESW'.index(position['facing']) + instruction[1]//90) % 4]
        
    elif instruction[0] == 'L':
        position['facing'] = 'NESW'[('NESW'.index(position['facing']) - instruction[1]//90) % 4]
   
    return position

assert implement_instruction(('F', 100)) == {'E':100, 'W':0, 'N':0, 'S':0, 'facing':'E'}
assert implement_instruction(('R', 90)) == {'E':0, 'W':0, 'N':0, 'S':0, 'facing':'S'}


def run(instructions):
    # Run first instruction
    position = implement_instruction(instructions[0])
    # Run following instructions
    for line in instructions[1:]:
        position = implement_instruction(line, position)
    return abs(position['E']-position['W']) + abs(position['N']-position['S'])

print(run(puzzle))