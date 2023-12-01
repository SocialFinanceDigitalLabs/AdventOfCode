from faker import Faker
from math import lcm

EXPECTED_TEST_ANSWER_PART1 = [10605]
EXPECTED_TEST_ANSWER_PART2 = [2713310158]

fake = Faker()


class Monkey:
    def __init__(self, name, worry_reduction_factor):
        self.inspection_count = 0
        self.worry_reduction_factor = worry_reduction_factor
        self.name = name
        self.holding_items = []
        self.operation = ""
        self.test = None
        self.true_pass = None
        self.false_pass = None
        self.safe_divisor = None

    def take_turn(self):
        """
        Simple controlling function to group together what needs to be done each turn
        """
        self.inspect()
        self.adjust_worry()

    def inspect(self):
        """
        Performs the operation while a monkey is handling the item
        """
        for idx, item in enumerate(self.holding_items):
            self.inspection_count += 1
            if self.operation["type"] == "+":
                if self.operation["amount"] is None:
                    self.holding_items[idx] += item
                else:
                    self.holding_items[idx] += self.operation["amount"]
            elif self.operation["type"] == "*":
                if self.operation["amount"] is None:
                    self.holding_items[idx] *= item
                else:
                    self.holding_items[idx] *= self.operation["amount"]

    def adjust_worry(self):
        """
        This was the puzzle function. For part 2, the safe_divisor was key
        as LCM means we can divide by that number safely without impacting
        the numbers and preventing the numbers from getting too large
        """
        for idx, item in enumerate(self.holding_items):
            self.holding_items[idx] = (
                item // self.worry_reduction_factor
            ) % self.safe_divisor

    def pass_to_next_monkey(self):
        """
        This sets up the instructions for where each item needs to go next
        """
        pass_instructions = [None for item in self.holding_items]
        for idx, item in enumerate(self.holding_items):
            if item % self.test == 0:
                pass_instructions[idx] = {"item": item, "to_monkey": self.true_pass}
            else:
                pass_instructions[idx] = {"item": item, "to_monkey": self.false_pass}
        self.holding_items = []
        return pass_instructions


def parse_instructions(data, worry_reduction_factor):
    """
    Read in the data from the file
    """
    monkeys = []
    m = None
    for entry in data:
        if entry.startswith("Monkey"):
            m = Monkey(fake.first_name(), worry_reduction_factor)
        elif entry.strip().startswith("Starting items"):
            m.holding_items = [
                int(word) for word in entry.replace(",", " ").split() if word.isdigit()
            ]
        elif entry.strip().startswith("Operation"):
            op = entry.split("=")[-1].strip().split()
            if op[2].isnumeric():
                op[2] = int(op[2])
            else:
                op[2] = None
            m.operation = {"type": op[1], "amount": op[2]}
        elif entry.strip().startswith("Test"):
            m.test = int(entry.split("by")[-1].strip())
        elif entry.strip().startswith("If true"):
            m.true_pass = int(entry.split("monkey")[-1].strip())
        elif entry.strip().startswith("If false"):
            m.false_pass = int(entry.split("monkey")[-1].strip())
        elif entry.strip() == "":
            monkeys.append(m)
            m = None
    monkeys.append(m)
    return monkeys


def get_score(monkeys):
    """
    Calculate the product of the most active 2 monkeys
    """
    inspection_counts = [m.inspection_count for m in monkeys]
    inspection_counts.sort()
    return inspection_counts[-1] * inspection_counts[-2]


def set_safe_divisor(monkeys):
    """
    For part 2 mainly. If we work the least common multiple between
    all the monkey tests, that gives the LCM which we can use to
    safely keep numbers small later on.
    """
    divisor = lcm(*[m.test for m in monkeys])
    for m in monkeys:
        m.safe_divisor = divisor


def show_monkey_handling(passing_round, monkeys):
    """
    Debug function to help show what the status was during the puzzle
    loops to help figure out where problems were when I wasn't getting
    the right answer
    """
    print("-------------------------------")
    print("At the start of passing round {}", passing_round)
    print("-------------------------------")
    for idx, m in enumerate(monkeys):
        print(
            "Monkey #{} (AKA: {}) has {} items, and inspected {} times".format(
                idx, m.name, m.holding_items, m.inspection_count
            )
        )


def run(data):
    monkeys = parse_instructions(data, 3)
    set_safe_divisor(monkeys)
    for passing_round in range(0, 20):
        if passing_round % 2 == 0:
            show_monkey_handling(passing_round, monkeys)
        for m in monkeys:
            m.take_turn()
            where_to_pass = m.pass_to_next_monkey()
            for pass_instruction in where_to_pass:
                monkeys[pass_instruction["to_monkey"]].holding_items.append(
                    pass_instruction["item"]
                )
    return get_score(monkeys)


def run_p2(data):
    monkeys = parse_instructions(data, 1)
    set_safe_divisor(monkeys)
    for passing_round in range(0, 10000):
        if passing_round % 1000 == 0:
            show_monkey_handling(passing_round, monkeys)
        for m in monkeys:
            m.take_turn()
            where_to_pass = m.pass_to_next_monkey()
            for pass_instruction in where_to_pass:
                monkeys[pass_instruction["to_monkey"]].holding_items.append(
                    pass_instruction["item"]
                )

    return get_score(monkeys)
