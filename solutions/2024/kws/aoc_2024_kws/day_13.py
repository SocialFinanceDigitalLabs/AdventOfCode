import math
import re
from decimal import Decimal, getcontext

import click
import numpy as np
from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config
from aocd import submit

getcontext().prec = 50

# Match Button A: X+94, Y+34
button_re = re.compile(r"Button (\w): X([+-]\d+), Y([+-]\d+)")

# Match Prize: X=8400, Y=5400
prize_re = re.compile(r"Prize: X=(.\d+), Y=(.\d+)")


def round_int(value: float) -> int | None:
    if math.isclose(value, round(value), abs_tol=1e-5):
        return round(value)
    else:
        return None


def round_int_decimal(value: Decimal) -> int | None:
    if value == value.to_integral_value():
        return value.to_integral_value()
    else:
        return None


def linalg_solve(A, B):
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    if det == 0:
        print("No unique solution exists.")
        return None, None
    else:
        x = (B[0] * A[1][1] - B[1] * A[0][1]) / det
        y = (A[0][0] * B[1] - A[1][0] * B[0]) / det
        return x, y


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day13(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day13.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day13.txt").read_text()

    input_data = input_data.splitlines()
    machines = []
    for ix in range(0, len(input_data), 4):
        button_a = input_data[ix]
        button_b = input_data[ix + 1]
        answer = input_data[ix + 2]

        button_a_match = button_re.match(button_a)
        button_b_match = button_re.match(button_b)
        prize_match = prize_re.match(answer)

        button_a_x = float(button_a_match.group(2))
        button_a_y = float(button_a_match.group(3))
        button_b_x = float(button_b_match.group(2))
        button_b_y = float(button_b_match.group(3))
        prize_x = float(prize_match.group(1))
        prize_y = float(prize_match.group(2))

        machines.append(
            (button_a_x, button_a_y, button_b_x, button_b_y, prize_x, prize_y)
        )

    total_tokens = total_wins = 0

    for machine in machines:
        button_a_x, button_a_y, button_b_x, button_b_y, prize_x, prize_y = machine

        # Represent as matrices
        A = [[button_a_x, button_b_x], [button_a_y, button_b_y]]
        B = [prize_x, prize_y]

        x, y = np.linalg.solve(A, B)
        x, y = round_int(x), round_int(y)

        if x and x < 100 and y and y < 100:
            total_tokens += x * 3 + y
            total_wins += 1
            print(f"x={x}, y={y}, (x*3 + y)={(x*3 + y)}")
        else:
            print(None)

    print(f"\nPart A: tokens={total_tokens}, wins={total_wins}")

    if not sample:
        submit(total_tokens, part="a", day=13, year=2024)

    print("\nPart B\n")

    total_tokens = total_wins = 0
    for machine in machines:
        button_a_x, button_a_y, button_b_x, button_b_y, prize_x, prize_y = machine
        button_a_x = Decimal(button_a_x)
        button_a_y = Decimal(button_a_y)
        button_b_x = Decimal(button_b_x)
        button_b_y = Decimal(button_b_y)
        prize_x = Decimal(prize_x)
        prize_y = Decimal(prize_y)

        # Represent as matrices
        offset = Decimal(10000000000000)
        A = np.array([[button_a_x, button_b_x], [button_a_y, button_b_y]])
        B = np.array([prize_x + offset, prize_y + offset])

        x, y = linalg_solve(A, B)
        x, y = round_int_decimal(x), round_int_decimal(y)

        if x and y:
            total_tokens += x * 3 + y
            total_wins += 1
            print(f"x={x}, y={y}, (x*3 + y)={(x*3 + y)}")
        else:
            print(None)

    print(f"\nPart B: tokens={total_tokens}, wins={total_wins}")

    if not sample:
        submit(total_tokens, part="b", day=13, year=2024)
