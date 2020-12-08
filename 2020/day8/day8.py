# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 13:44:47 2020

@author: celine.gross
"""

with open('input_day8.txt', 'r') as file:
    puzzle = file.read().strip().split('\n')


# Part 1

def to_next(data, i=0, accumulator=0):
    '''
    Returns the next line index to look at (i) and the updated accumulator value
    '''
    action, increment = data[i].split(' ')
    if action == 'nop':
        i += 1
    elif action == 'acc':
        i += 1
        if increment[0] == '+':
            accumulator += int(increment[1:])
        else:
            accumulator -= int(increment[1:])
    else:
        if increment[0] == '+':
            i += int(increment[1:])
        else:
            i -= int(increment[1:])
    return i, accumulator

assert to_next(puzzle, i=0, accumulator=0) == (232, 0)
assert to_next(puzzle, i=10, accumulator=0) == (11, 47)


def run(data):
    '''
    Returns accumulator value as soon as one instruction is repeated
    '''
    tracker = {}
    i, accumulator = 0, 0
    while to_next(data, i, accumulator)[0] not in tracker:
        i, accumulator = to_next(data, i, accumulator)
        tracker[i] = accumulator
    return accumulator

print(run(puzzle))


# Part 2

def replace(instruction, changes={'nop':'jmp', 'jmp':'nop', 'acc':'acc'}):
    '''
    Returns the new instruction with changes made
    '''
    for k in changes.keys():
        if k in instruction:
            return instruction.replace(k, changes[k])

assert replace('jmp +232') == 'nop +232'
assert replace('nop +55') == 'jmp +55'
assert replace('acc -33') == 'acc -33'


def terminates(data):
    '''
    Returns True and the accumulator value if the programme terminates
    Returns False and the accumulator value when first repeat
    '''
    tracker = {}
    i, accumulator = 0, 0
    while i < len(data):
        if to_next(data, i, accumulator)[0] in tracker:
            return False, accumulator
        else:
            i, accumulator = to_next(data, i, accumulator)
            tracker[i] = accumulator
    return True, accumulator


def run(data):
    '''
    Returns the accumulator value for the instruction set that successfully terminated
    '''
    for i, line in enumerate(data):
        copy = list(data)
        copy[i] = replace(copy[i])
        if terminates(copy)[0]:
            return terminates(copy)[1]


print(run(puzzle))
