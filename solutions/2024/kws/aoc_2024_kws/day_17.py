import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import StringIO

import click
from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config
from aocd import submit
from rich.progress import Progress, track

opcode_registry = {}


def opcode(opcode):
    def wrapper(func):
        def executor(*args, **kwargs):
            return func(*args, **kwargs)

        executor.OPCODE = opcode
        opcode_registry[opcode] = executor
        return executor

    return wrapper


class Halt(Exception):
    pass


class D17Computer:
    def __init__(
        self, reg_a: int, reg_b: int, reg_c: int, program: list[int], out=sys.stdout
    ):
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_c = reg_c
        self.program = program
        self.ip = 0
        self.out = out
        self.values_written = 0

    @property
    def current(self):
        if self.ip >= len(self.program):
            raise Halt()
        return self.program[self.ip]

    def execute(self):
        opcode = opcode_registry[self.current]
        self.ip += 1
        self.ip = opcode(self)

    def run(self):
        while True:
            try:
                self.execute()
            except Halt:
                break

    @property
    def combo(self):
        value = self.current
        if value < 4:
            return value
        elif value == 4:
            return self.reg_a
        elif value == 5:
            return self.reg_b
        elif value == 6:
            return self.reg_c
        else:
            raise ValueError(f"Invalid value: {value}")


@opcode(0)
def adv(computer: D17Computer) -> int:
    numerator = computer.reg_a
    denominator = 2**computer.combo
    computer.reg_a = numerator // denominator
    return computer.ip + 1


@opcode(1)
def bxl(computer: D17Computer) -> int:
    literal_operand = computer.current
    computer.reg_b ^= literal_operand
    return computer.ip + 1


@opcode(2)
def bst(computer: D17Computer) -> int:
    value = computer.combo % 8
    computer.reg_b = value
    return computer.ip + 1


@opcode(3)
def jnz(computer: D17Computer) -> int:
    if computer.reg_a == 0:
        return computer.ip + 1
    else:
        return computer.current


@opcode(4)
def bxc(computer: D17Computer) -> int:
    computer.reg_b ^= computer.reg_c
    return computer.ip + 1


@opcode(5)
def out(computer: D17Computer) -> int:
    value = computer.combo % 8
    if computer.values_written > 0:
        computer.out.write(",")
    computer.out.write(f"{value}")
    computer.values_written += 1
    return computer.ip + 1


@opcode(6)
def bdv(computer: D17Computer) -> int:
    numerator = computer.reg_a
    denominator = 2**computer.combo
    computer.reg_b = numerator // denominator
    return computer.ip + 1


@opcode(7)
def cdv(computer: D17Computer) -> int:
    numerator = computer.reg_a
    denominator = 2**computer.combo
    computer.reg_c = numerator // denominator
    return computer.ip + 1


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day17(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day17.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day17.txt").read_text()

    input_data = input_data.splitlines()
    reg_a = int(input_data[0].split(":")[1].strip())
    reg_b = int(input_data[1].split(":")[1].strip())
    reg_c = int(input_data[2].split(":")[1].strip())
    program = [int(x) for x in input_data[4].split(":")[1].strip().split(",")]

    print(reg_a, reg_b, reg_c, program)

    out = StringIO()
    computer = D17Computer(reg_a, reg_b, reg_c, program, out=out)
    computer.run()

    answer = out.getvalue()
    print(answer)

    if not sample:
        submit(answer, part="a", day=17, year=2024)

    if sample:
        reg_b = 0
        reg_c = 0
        program = [0, 3, 5, 4, 3, 0]

    output_length = len(program)

    def compute_result(reg_a):
        out = StringIO()
        computer = D17Computer(reg_a, 0, 0, program, out=out)
        computer.run()
        output_value = [int(x) for x in out.getvalue().split(",")]
        return output_value

    def find_target(digit, start_value):
        periodicity = 8 ** (digit)
        end_value = start_value + (periodicity * 8)

        target_value = program[digit]
        print(
            f"Periodicity: {periodicity} for digit {digit}. Start {start_value} End {end_value}. Looking for {target_value}"
        )

        for reg_a in range(start_value, end_value, periodicity):
            result = compute_result(reg_a)
            print("P", digit, reg_a, program, len(program), target_value)
            print("R", digit, reg_a, result, len(result), result[digit])
            print()
            if result[digit] == target_value:
                print(f"Found at {reg_a}")
                return reg_a

        raise ValueError(f"No match found for {digit}")

    # for reg_a in range(0, 120_000):
    #     result = compute_result(reg_a)
    #     print(reg_a, "".join(str(x) for x in result))

    print(f"My output length is {output_length}: {program}")
    start_digit = output_length - 1
    start_value = (2**start_digit) ** 3
    for digit in range(start_digit, 0, -1):
        start_value = find_target(digit, start_value)

    for reg_a in range(start_value, start_value * 2):
        result = compute_result(reg_a)
        if result == program:
            print(reg_a, result)
            break

    if not sample:
        submit(reg_a, part="b", day=17, year=2024)


if __name__ == "__main__":
    day17()

    # submit(my_answer, part="a", day=17, year=2024)
