import pandas as pd

from utils import priorities_map


def elf_group(inventory):
    compartments = inventory.split()
    # use zip_longest from itertools if the index doesn't perfectly divide by 3.
    elf_groups = list(zip(*(iter(compartments),) * 3))

    def _find_commoner(tup):
        uniques = [set(strng) for strng in tup]
        commoner, *_ = set.intersection(*uniques)
        return commoner

    commoners = [_find_commoner(tup) for tup in elf_groups]
    commoners = pd.DataFrame(commoners, columns=["group_badge"])

    commoners["priority"] = commoners["group_badge"].map(priorities_map)

    return commoners["priority"].sum()


with open("input_day3.txt", "r") as f:
    inventory = f.read()

result = elf_group(inventory)
print(result)
