import pandas as pd
import string

from utils import string_in_two, common_element


def rucksacks_pack(inventory):
    compartments = [string_in_two(strng) for strng in inventory.split()]
    compartments = pd.DataFrame(compartments, columns=["first_part", "second_part"])

    compartments["commoner"] = compartments.apply(
        lambda x: common_element(x["first_part"], x["second_part"]), axis=1
    )

    lowercase = list(string.ascii_lowercase)
    small_weights = list(range(1, 27))
    small_priorities = dict(zip(lowercase, small_weights))

    uppercase = list(string.ascii_uppercase)
    upper_weights = list(range(27, 53))
    upper_priorities = dict(zip(uppercase, upper_weights))

    priorities_map = small_priorities | upper_priorities

    compartments["priority"] = compartments["commoner"].map(priorities_map)

    return compartments["priority"].sum()


with open("input_day3.txt", "r") as f:
    inventory = f.read()

result = rucksacks_pack(inventory)
print(result)
