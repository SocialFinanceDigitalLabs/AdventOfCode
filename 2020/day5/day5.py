# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 10:15:03 2020

@author: celine.gross
"""

with open('input_day5.txt', 'r') as file:
    puzzle = file.read().strip().split('\n')
    

def return_lower(input_list):
    return input_list[:len(input_list)//2]

assert return_lower([1,2,3,4]) == [1,2]


def return_upper(input_list):
    return input_list[len(input_list)//2:]

assert return_upper([1,2,3,4,5,6]) == [4,5,6]
   

def determine_row(boardingpass, totalrows = 128):
    eligible_rows = [i for i in range(totalrows)]
    for letter in boardingpass[:8]:
        if letter == 'F':
            eligible_rows = return_lower(eligible_rows)
        elif letter == 'B':
            eligible_rows = return_upper(eligible_rows)
    return eligible_rows[0]

assert determine_row('FBFBBFFRLR') == 44
assert determine_row('BFFFBBFRRR') == 70


def determine_col(boardingpass, totalcols = 8):
    eligible_cols = [i for i in range(totalcols)]
    for letter in boardingpass[-3:]:
        if letter == 'L':
            eligible_cols = return_lower(eligible_cols)
        elif letter == 'R':
            eligible_cols = return_upper(eligible_cols)
    return eligible_cols[0]

assert determine_col('FBFBBFFRLR') == 5
assert determine_col('BFFFBBFRRR') == 7


def create(boardingpass):
    boarding_info = {}
    boarding_info['row'] = determine_row(boardingpass)
    boarding_info['col'] = determine_col(boardingpass)
    boarding_info['id'] = boarding_info['row']*8 + boarding_info['col']
    return boarding_info

assert create('BFFFBBFRRR') == {'row':70, 'col':7, 'id':567}
assert create('FFFBBBFRRR') == {'row':14, 'col':7, 'id':119}


def run(data):
    all_ids = []
    for boardingpass in data:
        all_ids.append(create(boardingpass)['id'])
    return max(all_ids)


# Respond to part 1
    
print(run(puzzle))


# Respond to part 2

def missing_ids(data):
    all_ids = []
    missing_ids = []
    for boardingpass in data:
        all_ids.append(create(boardingpass)['id'])
    min_id, max_id = min(all_ids), max(all_ids)
    for id_number in range(min_id, max_id +1):
        if id_number not in all_ids:
            missing_ids.append(id_number)
    return missing_ids

print(missing_ids(puzzle))
    
    