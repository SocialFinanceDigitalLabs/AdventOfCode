# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 10:22:31 2020
 
@author: celine.gross
"""
import re

with open("input_day4.txt", "r") as f:
    contents = f.read().strip().split("\n\n")
    puzzle = [re.split('\s|\n', l) for l in contents]
    puzzle = [dict([s.split(':') for s in l]) for l in puzzle]

print(puzzle[:30])


# Part 1 - Count valid passports

fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']

def is_valid(passport, fields, optional=None):
    if optional is not None:
        final_fields = [f for f in fields if f not in optional]
    else:
        final_fields=fields
    return set(final_fields).issubset(passport)

assert is_valid({'cid': '168', 'pid': '#8556c9', 'hcl': '413944', 'eyr': '2036', 'byr': '2013', 'iyr': '2012', 'ecl': '#66dc1c', 'hgt': '59cm'},
                 fields, optional=['pid']) == True
assert is_valid({'cid': '168', 'hcl': '413944', 'eyr': '2036', 'byr': '2013', 'iyr': '2012', 'ecl': '#66dc1c', 'hgt': '59cm'},
                 fields, optional=None) == False

    
count = 0
for passport_info in puzzle:
    count += is_valid(passport_info, fields, optional=['cid'])
print(count)


# Part 2 - Additional passport validation rules

# Define our validation rules for each field
field_validation = {
        'byr': {'number': [1920,2002]},
        'iyr': {'number': [2010,2020]},
        'eyr': {'number': [2020,2030]},
        'hgt': {'height': {'cm':[150, 193], 'in':[59, 76]}},
        'hcl': {'regex': '^#([0-9]|[a-f]){6}$'},
        'ecl': {'regex': '^(amb)|(blu)|(brn)|(gry)|(grn)|(hzl)|(oth)$'},
        'pid': {'regex': '^[0-9]{9}$'}
            }

# Keep two examples to test
valid_passport = {'pid':'087499704', 
                  'hgt':'74in', 
                  'ecl':'grn', 
                  'iyr':'2012', 
                  'eyr':'2030', 
                  'byr':'1980',
                  'hcl':'#623a2f'}

invalid_passport = {'hcl':'dab227', 
                    'iyr':'2012',
                    'ecl':'brn', 
                    'hgt':'182cm', 
                    'pid':'021572410', 
                    'eyr':'2020', 
                    'byr':'1992', 
                    'cid':'277'}

# Functions
def validate_number(field, bounds):
    field = int(field)
    if bounds[0]<=field<=bounds[1]:
        return True
    return False

def validate_regex(field, regex):
    match = re.findall(regex, field)
    if len(match)>0:
        return True
    return False

def validate_height(field, rule):
    system = field[-2:]
    if any(x in system for x in ['cm', 'in']):
        return validate_number(field[:-2], rule[system])
    return False

def assign_function(validation_type, field, rule):
    if validation_type == 'number':
        return validate_number(field, rule)
    elif validation_type == 'regex':
        return validate_regex(field, rule)
    else:
        return validate_height(field, rule)

def validate_all_fields(passport, validation_rules):
    count = 0
    for field in field_validation.keys():
        count += assign_function(list(field_validation[field].keys())[0], passport[field], list(field_validation[field].values())[0])
    if count == len(validation_rules):
        return True
    return False

assert validate_all_fields(valid_passport, field_validation) == True
assert validate_all_fields(invalid_passport, field_validation) == False

# Run
count = 0
for passport_info in puzzle:
    if is_valid(passport_info, fields, optional=['cid']):
        count += validate_all_fields(passport_info, field_validation)
print(count)