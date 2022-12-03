from day3_task1 import rucksacks_pack


def test_rucksacks_pack():
    with open("test_input_day3.txt", "r") as f:
        inventory = f.read()
    assert rucksacks_pack(inventory) == 157
