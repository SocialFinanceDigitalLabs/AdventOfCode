from aocd import get_data
import re
from math import lcm
from copy import deepcopy

session = "53616c7465645f5f932620b9dd9cb53e9facee9282730977ff26a7c28126db6fa8ce7b0" \
          "329cbec99fa54ea4d10b35d0cb2d5b3d17492e51cf4a0282caf0025e1"

monkey_games = get_data(day=11, year=2022, session=session).splitlines()
monkey_games.append("")

test = [line.strip() for line in open(r"C:\Users\Patrick\Downloads\test.txt")]
test.append("")


class Monkey:
    def __init__(self, items=None, operation=None, test=None, if_true=None, if_false=None):
        self.items = items
        self.operation = operation
        self.test = test
        self.if_true = if_true
        self.if_false = if_false
        self.inspections = 0


monkeys = zip(*(iter(monkey_games),) * 7)


def create_monkey_dict(monkey_data):
    monkey_dict = {}
    for monkey in monkey_data:
        monkey_no = monkey[0][:-1]
        monkey_dict[monkey_no] = Monkey()
        monkey_dict[monkey_no].items = re.findall("\\d+", monkey[1])
        monkey_dict[monkey_no].operation = monkey[2].split()[4:]
        monkey_dict[monkey_no].test = monkey[3].split()[-1:]
        monkey_dict[monkey_no].if_true = monkey[4].split()[-1:]
        monkey_dict[monkey_no].if_false = monkey[5].split()[-1:]
    return monkey_dict


def monkey_business(monkey_inspections):
    most_inspections = max(monkey_inspections)
    monkey_inspections.remove(most_inspections)
    second_most_inspections = max(monkey_inspections)
    return most_inspections*second_most_inspections


monkey_dict_part_1 = create_monkey_dict(monkeys)
monkey_dict_part_2 = deepcopy(monkey_dict_part_1)

lowest_common_multiple = lcm(*[int(monkey_dict_part_1[m].test[0]) for m in monkey_dict_part_1])


def calculate_monkey_inspections(rounds, worry_meter, monkey_dict):
    for round in range(rounds):
        for monkey in monkey_dict:
            current_monkey = monkey_dict[monkey]
            for item in current_monkey.items:
                current_monkey.inspections += 1

                if current_monkey.operation[1] == "old":
                    new_worry_level = eval(item + current_monkey.operation[0] + item)
                else:
                    new_worry_level = eval(item + current_monkey.operation[0] + current_monkey.operation[1])
                if worry_meter is False:
                    new_worry_level = str(new_worry_level // 3)
                else:
                    new_worry_level = str(new_worry_level % lowest_common_multiple)

                if eval(new_worry_level + "%" + current_monkey.test[0]) == 0:
                    current_monkey.items = current_monkey.items[1:]
                    monkey_to_throw_to = "Monkey " + current_monkey.if_true[0]
                    monkey_dict[monkey_to_throw_to].items.append(new_worry_level)
                else:
                    current_monkey.items = current_monkey.items[1:]
                    monkey_to_throw_to = "Monkey " + current_monkey.if_false[0]
                    monkey_dict[monkey_to_throw_to].items.append(new_worry_level)

    monkey_inspections = []
    for monkey in monkey_dict:
        monkey_inspections.append(monkey_dict[monkey].inspections)

    return monkey_business(monkey_inspections)


print(calculate_monkey_inspections(20, False, monkey_dict_part_1))
print(calculate_monkey_inspections(10000, True, monkey_dict_part_2))


