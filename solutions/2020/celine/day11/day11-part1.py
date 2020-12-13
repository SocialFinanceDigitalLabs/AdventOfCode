# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 17:04:59 2020

@author: celine.gross
"""

import numpy as np

with open('input_day11.txt', 'r') as file:
    puzzle = [[x for x in line.strip()] for line in file]
    puzzle = np.array(puzzle)
    
with open('example.txt', 'r') as file:
    example = [[x.strip() for x in line] for line in file]
    example = np.array(example)
    
with open('no_movement.txt', 'r') as file:
    no_movement = [[x.strip() for x in line] for line in file]
    no_movement = np.array(no_movement)
    
print(puzzle[:100])

def count_seats_taken(data):
    count = 0
    for row in data:
        for seat in row:
            if seat == '#':
                count+=1
    return count

assert count_seats_taken(example) == 23
assert count_seats_taken(puzzle) == 0


def seat_to_free(x, y, data):
    if data[x][y] != '#':
        return False
    else:
        count = 0
        for row in data[max(0, x-1): min(x+1, len(data)-1)+1]:
            for seat in row[max(0, y-1): min(y+1, len(data[0])-1)+1]:
                if seat == '#':
                    count += 1
        if count>4:
            return True
    return False

assert seat_to_free(3, 1, example) == True
assert seat_to_free(5, 6, example) == False


def seat_to_take(x, y, data):
    if data[x][y] != 'L':
        return False
    else:
        for i in range(max(0, x-1), min(x+1, len(data)-1)+1):
            for j in range(max(0, y-1), min(y+1, len(data[0])-1)+1):
                if data[i][j] == '#':
                    return False
    return True

assert seat_to_take(2, 7, example) == True
assert seat_to_take(3, 3, example) == False


def get_seat_coordinates(data):
    to_free = set()
    to_take = set()
    for i, row in enumerate(data):
        for j, col in enumerate(row):
            if seat_to_free(i, j, data):
                to_free.add((i,j))
            elif seat_to_take(i, j, data):
                to_take.add((i,j))         
    return to_free, to_take


def update_seats(data, to_free, to_take):
    for x,y in to_free:
        data[x][y] = 'L'
    for x,y in to_take:
        data[x][y] = '#'
    return data


def run(data):
    changes = True
    while changes:
        to_free, to_take = get_seat_coordinates(data)
        data = update_seats(data, to_free, to_take)
        if (len(to_free) == 0 and len(to_take) == 0):
            changes = False        
    return count_seats_taken(data)


print(run(puzzle))
    
        
    