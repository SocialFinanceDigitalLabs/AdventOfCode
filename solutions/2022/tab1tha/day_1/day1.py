from input_day1 import calories
# calories is a string of containing the input.

def strs_to_ints(lst_strs):
    # convert to list of strings to list of ints
    lst_ints = list(map(int, lst_strs))
    return sum(lst_ints)

inventory_per_elf_lst = [strs_to_ints(cal_lst.split("\n")) for cal_lst in calories.split("\n\n")]

# save the list so that it can be used later
inventory_per_elf = inventory_per_elf_lst.copy()

# elf with the highest number of calories
max_calory_inv = max(inventory_per_elf)
richest_elf = inventory_per_elf.index(max_calory_inv)

# top 3 elves
inventory_per_elf_lst.sort()
top3 = sum(inventory_per_elf_lst[-3:])
