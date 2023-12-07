from util import FileParser
import os
from dataclasses import dataclass
from typing import Callable

from enum import Enum
from functools import cached_property, cmp_to_key
from collections import Counter

dir_path = os.path.dirname(os.path.realpath(__file__))


class HandTypes(Enum):
    ALL_EQUAL = 6
    POKER = 5
    FULL_HOUSE = 4
    TRIPLE = 3
    TWO_PAIRS = 2
    PAIR = 1
    HIGH_CARD = 0


cards = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
cards_p2 = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]


@dataclass
class Hand:
    cards: str
    bid: int

    @cached_property
    def type(self):
        counter = Counter(self.cards)
        unique_cards_count = len(counter.keys())
        if unique_cards_count == 1:
            return HandTypes.ALL_EQUAL
        if unique_cards_count == 2:
            if any(c == 4 for c in counter.values()):
                return HandTypes.POKER
            if any(c == 3 for c in counter.values()):
                return HandTypes.FULL_HOUSE
        if any(c == 3 for c in counter.values()):
            return HandTypes.TRIPLE
        if sum(c == 2 for c in counter.values()) == 2:
            return HandTypes.TWO_PAIRS
        if any(c == 2 for c in counter.values()):
            return HandTypes.PAIR
        return HandTypes.HIGH_CARD

    @cached_property
    def typep2(self):
        counter = Counter(self.cards)
        j_count = counter.pop("J", 0)
        unique_cards_count = len(counter.keys())

        if unique_cards_count == 1:
            return HandTypes.ALL_EQUAL

        if any(c == 4 for c in counter.values()):
            if j_count == 1:
                return HandTypes.ALL_EQUAL
            return HandTypes.POKER

        if any(c == 3 for c in counter.values()):
            if j_count == 2:
                return HandTypes.ALL_EQUAL
            if j_count == 1:
                return HandTypes.POKER
            if unique_cards_count == 2:
                return HandTypes.FULL_HOUSE
            return HandTypes.TRIPLE

        if sum(c == 2 for c in counter.values()) == 2:
            if j_count == 1:
                return HandTypes.FULL_HOUSE
            return HandTypes.TWO_PAIRS

        if any(c == 2 for c in counter.values()):
            if j_count == 3:
                return HandTypes.ALL_EQUAL
            if j_count == 2:
                return HandTypes.POKER
            if j_count == 1:
                return HandTypes.TRIPLE
            return HandTypes.PAIR

        if j_count == 5 or j_count == 4:
            return HandTypes.ALL_EQUAL
        if j_count == 3:
            return HandTypes.POKER
        if j_count == 2:
            return HandTypes.TRIPLE
        if j_count == 1:
            return HandTypes.PAIR
        return HandTypes.HIGH_CARD

    def __repr__(self) -> str:
        return f"Hand(cards={self.cards}, bid={self.bid}, type={self.type})"


def comparep1(hand1: Hand, hand2: Hand):
    if hand1.type.value > hand2.type.value:
        return 1
    if hand1.type.value < hand2.type.value:
        return -1
    if hand1.type.value == hand2.type.value:
        for i in range(len(hand1.cards)):
            c1 = hand1.cards[i]
            c2 = hand2.cards[i]
            if c1 == c2:
                continue
            if cards.index(c1) > cards.index(c2):
                return 1
            if cards.index(c1) < cards.index(c2):
                return -1
        raise (ValueError("this shouldn't happen"))


def comparep2(hand1: Hand, hand2: Hand):
    if hand1.typep2.value > hand2.typep2.value:
        return 1
    if hand1.typep2.value < hand2.typep2.value:
        return -1
    if hand1.typep2.value == hand2.typep2.value:
        for i in range(len(hand1.cards)):
            c1 = hand1.cards[i]
            c2 = hand2.cards[i]
            if c1 == c2:
                continue
            if cards_p2.index(c1) > cards_p2.index(c2):
                return 1
            if cards_p2.index(c1) < cards_p2.index(c2):
                return -1
        raise (ValueError("this shouldn't happen"))


def clean_data(data: list[str]) -> list[Hand]:
    hands = []
    for d in data:
        cards, bid = d.split(" ")
        hand = Hand(cards, int(bid))
        hands.append(hand)
    return hands


def solve(file: str, compare_method: Callable):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    data = parser.read()
    hands = clean_data(data)
    sorted_hands: list[Hand] = sorted(hands, key=cmp_to_key(compare_method))
    total = 0
    for i, hand in enumerate(sorted_hands):
        print(i + 1, hand.bid)
        total += (i + 1) * hand.bid
    return total


def part_1(file: str):
    solve(file, comparep1)


def part_2(file: str):
    solve(file, comparep2)
