from aocd import get_data
import re
from copy import deepcopy

session = "53616c7465645f5f932620b9dd9cb53e9facee9282730977ff26a7c28126db6fa8ce7b0" \
          "329cbec99fa54ea4d10b35d0cb2d5b3d17492e51cf4a0282caf0025e1"

crate_data = get_data(day=5, year=2022, session=session).split("\n")


# PART 1
crate_layout = crate_data[0:9]
crane_instructions = crate_data[10:]

crate_columns = []
[crate_columns.append([i]) for i in range(1, 10)]

row_values_dict = {1: 1, 2: 5, 3: 9, 4: 13, 5: 17, 6: 21, 7: 25, 8: 29, 9: 33}
for i in range(len(crate_layout)-1):
    for value in row_values_dict:
        crate_letter = crate_layout[i][row_values_dict[value]]
        if crate_letter != " ":
            crate_columns[value-1].append(crate_letter)

for column in crate_columns:
    column_value = column[0]-1
    crate_columns[column_value] = column[1:][::-1]

crate_columns_2 = deepcopy(crate_columns)


def _find_instruction_values(instructions):
    values = re.search("move (\\d*) from (\\d*) to (\\d*)", instructions).groups()
    amount, from_column, to_column = int(values[0]), int(values[1]), int(values[2])
    return amount, from_column, to_column


def move_crate_9000(instructions, crate_layout):
    instruction_values = _find_instruction_values(instructions)
    amount = instruction_values[0]
    from_column = instruction_values[1]
    to_column = instruction_values[2]
    for i in range(amount):
        crate = crate_layout[from_column-1][::-1][0]
        del(crate_layout[from_column-1][-1])
        crate_layout[to_column-1].append(crate)
    return crate_layout


for instruction in crane_instructions:
    crate_columns = move_crate_9000(instruction, crate_columns)

end_crates = ""
for column in crate_columns:
    end_crates += column[-1:][0]

print(end_crates)

# PART 2
def move_crate_9001(instructions, crate_layout):
    instruction_values = _find_instruction_values(instructions)
    amount = instruction_values[0]
    from_column = instruction_values[1]
    to_column = instruction_values[2]
    crates = crate_layout[from_column-1][-amount:]
    del(crate_layout[from_column-1][-amount:])
    crate_layout[to_column-1] += crates
    return crate_layout


for instruction in crane_instructions:
    crate_columns_2 = move_crate_9001(instruction, crate_columns_2)

end_crates = ""
for column in crate_columns_2:
    end_crates += column[-1:][0]

print(end_crates)
