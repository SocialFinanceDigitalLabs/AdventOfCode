import pandas as pd
import string

from utils import string_in_two, common_element, priorities_map

with open("input_day3.txt", "r") as f:
    inventory = f.read()


def rucksacks_pack(inventory):
    compartments = [string_in_two(strng) for strng in inventory.split()]
    compartments = pd.DataFrame(compartments, columns=["first_part", "second_part"])

    compartments["commoner"] = compartments.apply(
        lambda x: common_element(x["first_part"], x["second_part"]), axis=1
    )
    compartments["priority"] = compartments["commoner"].map(priorities_map)

    return compartments["priority"].sum()


result = rucksacks_pack(inventory)
print(result)
