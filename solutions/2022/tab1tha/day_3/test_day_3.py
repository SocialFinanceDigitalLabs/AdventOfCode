from day3_task1 import rucksacks_pack
from day3_task2 import elf_group

with open("test_input_day3.txt", "r") as f:
    inventory = f.read()


def test_rucksacks_pack():
    assert rucksacks_pack(inventory) == 157


def test_elf_group():
    assert elf_group(inventory) == 70
