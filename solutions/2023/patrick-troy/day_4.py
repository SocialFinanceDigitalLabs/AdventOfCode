from aocd import get_data
import re

session = "53616c7465645f5f5e959babee3b98732450e5a8dc2320e845ed91c80b7f39fe01f7" \
          "c01baa3710d5d1e1f631fe6c9f768fc1a035e9c3d5cd00e23c7ea0637cae"

data = get_data(day=4, year=2023, session=session).split("\n")


test = [
    "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
]


def solve_1(puzzle_input):
    points = []
    for card in puzzle_input:
        winning_no = re.findall(r"\d+", card.split("|")[0].split(":")[1])
        my_no = re.findall(r"\d+", card.split("|")[1])

        matches = [x for x in my_no if x in winning_no]
        if matches:
            points.append(2**(len(matches)-1))

    print(sum(points))

# solve_1(test)


def solve_2(puzzle_input):
    cards = []
    for i, card in enumerate(puzzle_input):
        winning_no = re.findall(r"\d+", card.split("|")[0].split(":")[1])
        my_no = re.findall(r"\d+", card.split("|")[1])

        matches = [x for x in my_no if x in winning_no]
        cards.append({i+1: len(matches), "copies": 1})

    print(cards)

    for i, value in enumerate(cards):
        for x in range(list(value.values())[0]):
            cards[i+x]["copies"] += 1
            # print(i, x)
            # print(cards)

    print(cards)





solve_2(test)
