from aocd import get_data

session = "53616c7465645f5f932620b9dd9cb53e9facee9282730977ff26a7c28126db6fa8ce7b0" \
          "329cbec99fa54ea4d10b35d0cb2d5b3d17492e51cf4a0282caf0025e1"

signal_cycle = get_data(day=10, year=2022, session=session).splitlines()

X = 1
cycle = 0
signal_strength = 0


def calculate_signal_strength(cycle):
    for i in range(6):
        if cycle == 20 + 40 * i:
            global signal_strength
            signal_strength += X * cycle


for instruction in signal_cycle:
    elem = instruction.split()

    if elem[0] == "noop":
        cycle += 1
        calculate_signal_strength(cycle)

    if elem[0] == "addx":
        second_elem = int(elem[1])
        for value in range(2):
            cycle += 1
            calculate_signal_strength(cycle)
        X += second_elem

print(signal_strength)

X = 1
cycle = 0
crt = list("." * 40 * 6)


def update_crt(X, cycle, crt):
    pos = (cycle - 1) % 40
    if pos in {X - 1, X, X + 1}:
        crt[cycle - 1] = "#"


for instruction in signal_cycle:
    elem = instruction.split()

    if elem[0] == "noop":
        cycle += 1
        update_crt(X, cycle, crt)

    elif elem[0] == "addx":
        second_elem = int(elem[1])
        cycle += 1
        update_crt(X, cycle, crt)

        cycle += 1
        update_crt(X, cycle, crt)
        X += second_elem

for i in range(0, 201, 40):
    print("".join(crt[i: i + 40]))
