from functools import cmp_to_key

from aoc_2023_kws.day_07 import Hand, HandType, joker_comparator


def test_types():
    assert Hand("AAAAA 1").hand_type == HandType.FIVE_OF_A_KIND
    assert Hand("AAAAB 1").hand_type == HandType.FOUR_OF_A_KIND
    assert Hand("AAABB 1").hand_type == HandType.FULL_HOUSE
    assert Hand("AAABC 1").hand_type == HandType.THREE_OF_A_KIND
    assert Hand("AABBC 1").hand_type == HandType.TWO_PAIR
    assert Hand("ABCDA 1").hand_type == HandType.ONE_PAIR
    assert Hand("ABCDE 1").hand_type == HandType.HIGH_CARD


def test_strongest_types():
    assert Hand("T55J5 1").strongest_hand_type == HandType.FOUR_OF_A_KIND
    assert Hand("T55J5 1").hand_type == HandType.THREE_OF_A_KIND

    assert Hand("KTJJT 1").strongest_hand_type == HandType.FOUR_OF_A_KIND
    assert Hand("KTJJT 1").hand_type == HandType.TWO_PAIR


def test_joker_sorting():
    assert joker_comparator(Hand("AAAAA 0"), Hand("AAAAA 0")) == 0
    assert joker_comparator(Hand("T55J5 0"), Hand("QQQJA 0")) == -1
    assert joker_comparator(Hand("QQQQ2 0"), Hand("JKKK2 0")) == 1
    assert joker_comparator(Hand("JKKK2 0"), Hand("QQQQ2 0")) == -1

    hands = [
        Hand("JKKK2 0"),
        Hand("QQQQ2 0"),
    ]

    joker_sorted = sorted(hands, key=cmp_to_key(joker_comparator))
    assert joker_sorted == [
        Hand("JKKK2 0"),
        Hand("QQQQ2 0"),
    ]

    normal_sorted = sorted(hands)
    assert normal_sorted == [
        Hand("JKKK2 0"),
        Hand("QQQQ2 0"),
    ]
