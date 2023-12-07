from collections import Counter
from enum import Enum
from functools import cmp_to_key

import click
from aoc_2023_kws.cli import main
from aoc_2023_kws.config import config
from aocd import submit

CARD_RANK = "23456789TJQKA"
JOKER_RANK = "J23456789TQKA"


class HandType(Enum):
    HIGH_CARD = 10
    ONE_PAIR = 20
    TWO_PAIR = 30
    THREE_OF_A_KIND = 40
    FULL_HOUSE = 50
    FOUR_OF_A_KIND = 60
    FIVE_OF_A_KIND = 70


class Hand:
    def __init__(self, input_string):
        cards, bid = input_string.split(" ")
        self.cards = list(cards.strip())
        self.bid = int(bid.strip())

    @property
    def hand_type(self):
        counts = Counter(self.cards)
        if len(counts) == 5:
            return HandType.HIGH_CARD
        elif len(counts) == 4:
            return HandType.ONE_PAIR
        elif len(counts) == 3:
            if 3 in counts.values():
                return HandType.THREE_OF_A_KIND
            else:
                return HandType.TWO_PAIR
        elif len(counts) == 2:
            if 2 in counts.values():
                return HandType.FULL_HOUSE
            else:
                return HandType.FOUR_OF_A_KIND
        elif len(counts) == 1:
            return HandType.FIVE_OF_A_KIND
        else:
            raise ValueError("Invalid hand")

    @property
    def strongest_hand_type(self):
        all_hands = []
        for sub in "23456789TQKA":
            cards = "".join(self.cards).replace("J", sub)
            hand = Hand(cards + " 1")
            all_hands.append(hand)

        all_hands.sort()

        return all_hands[-1].hand_type

    @property
    def card_rank(self):
        return [CARD_RANK.index(c) for c in self.cards]

    def __lt__(self, other):
        if self.hand_type.value == other.hand_type.value:
            return self.card_rank < other.card_rank
        return self.hand_type.value < other.hand_type.value

    def __eq__(self, other: object) -> bool:
        return self.cards == other.cards

    def __repr__(self):
        return f"{''.join(self.cards)} {self.bid} {self.hand_type}"


def joker_comparator(a, b):
    if a.strongest_hand_type.value == b.strongest_hand_type.value:
        a_rank = [JOKER_RANK.index(c) for c in a.cards]
        b_rank = [JOKER_RANK.index(c) for c in b.cards]
        return 1 if a_rank > b_rank else -1 if a_rank < b_rank else 0
    return (
        1
        if a.strongest_hand_type.value > b.strongest_hand_type.value
        else -1
        if a.strongest_hand_type.value < b.strongest_hand_type.value
        else 0
    )


@main.command()
@click.option("--sample", "-s", is_flag=True)
def day07(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day07.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day07.txt").read_text()

    all_hands = [Hand(line) for line in input_data.splitlines()]
    all_hands.sort()

    # Part 1
    score = 0
    for ix, h in enumerate(all_hands):
        print(ix + 1, h)
        score += (ix + 1) * h.bid

    print("Part 1:", score)

    # Part 2
    score = 0

    joker_hands = sorted(all_hands, key=cmp_to_key(joker_comparator))

    for ix, h in enumerate(joker_hands):
        print(ix + 1, h, h.strongest_hand_type)
        score += (ix + 1) * h.bid

    print("Part 2:", score)
