from enum import Enum

EXPECTED_TEST_ANSWER_PART1 = [6440, 7227, 7653, 105907]
EXPECTED_TEST_ANSWER_PART2 = [5905, 8388, 8680, 105124]

CARD_ORDER = "23456789TJQKA"
CARD_ORDER_PART2 = "J23456789TQKA"


class PossibleHands(Enum):
    """
    Had to use this to keep track. Kept making mistakes on the values.
    """

    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIRS = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


def get_rank(cards):
    """
    This determines the type of hand a person has mainly by
    the difference between the set (unique characters) and the actual cards
    and their count
    """
    card_set = set(cards)
    unique_counts = {cards.count(char) for char in card_set}

    if len(card_set) == 1:
        return PossibleHands.FIVE_OF_A_KIND
    elif len(card_set) == 5:
        return PossibleHands.HIGH_CARD
    elif len(card_set) == 2 and 3 in unique_counts:
        return PossibleHands.FULL_HOUSE
    elif len(card_set) == 2:
        return PossibleHands.FOUR_OF_A_KIND
    elif len(card_set) == 3 and 3 in unique_counts:
        return PossibleHands.THREE_OF_A_KIND
    elif len(card_set) == 3:
        return PossibleHands.TWO_PAIRS
    else:
        return PossibleHands.ONE_PAIR


def get_rank_p2(cards):
    unique_cards = set(cards)
    unique_cards_length = len(unique_cards)
    joker_count = cards.count("J")

    if unique_cards_length == 1:
        return PossibleHands.FIVE_OF_A_KIND
    elif unique_cards_length == 5:
        return PossibleHands.HIGH_CARD if joker_count == 0 else PossibleHands.ONE_PAIR
    elif unique_cards_length == 2:
        if joker_count == 0:
            return (
                PossibleHands.FOUR_OF_A_KIND
                if any(cards.count(char) == 4 for char in unique_cards)
                else PossibleHands.FULL_HOUSE
            )
        else:
            return PossibleHands.FIVE_OF_A_KIND
    elif unique_cards_length == 3:
        if joker_count == 0:
            return (
                PossibleHands.THREE_OF_A_KIND
                if any(cards.count(char) == 3 for char in unique_cards)
                else PossibleHands.TWO_PAIRS
            )
        elif joker_count == 1:
            return (
                PossibleHands.FOUR_OF_A_KIND
                if any(cards.count(char) == 3 for char in unique_cards)
                else PossibleHands.FULL_HOUSE
            )
        elif joker_count in {2, 3}:
            return PossibleHands.FOUR_OF_A_KIND
    else:
        return (
            PossibleHands.THREE_OF_A_KIND if joker_count > 0 else PossibleHands.ONE_PAIR
        )


def individual_card_rank(card, ordering_list):
    '''
    Turns the card into its score equivalents
    So in part 1 AKQJJ would become (12, 10, 11, 9, 9)
    This allows for faster sorting
    '''
    return tuple(ordering_list.index(char) for char in card)


def parse_cards(data):
    '''
    Parse input data and structures the result in
    a way that will be easy to visualise and sort through
    '''
    ranks = {}
    for line in data:
        cards = line.strip().split(" ")[0].strip()
        bids = line.strip().split(" ")[1].strip()
        result = get_rank(cards)
        if result not in ranks.keys():
            ranks[result] = [{"cards": cards, "bid": int(bids)}]
        else:
            try:
                ranks[result].append({"cards": cards, "bid": int(bids)})
            except KeyError as err:
                print(ranks)
    return ranks


def parse_cards_p2(data):
    '''
    Parse input data and structures the result in
    a way that will be easy to visualise and sort through
    A slight change for part 2. I could simplify to avoid
    duplication with part 1, but why?
    '''
    ranks = {}
    for line in data:
        cards = line.strip().split(" ")[0].strip()
        bids = line.strip().split(" ")[1].strip()
        result = get_rank_p2(cards)
        if result not in ranks.keys():
            ranks[result] = [{"cards": cards, "bid": int(bids)}]
        else:
            try:
                ranks[result].append({"cards": cards, "bid": int(bids)})
            except KeyError as err:
                print(ranks)
    return ranks


def get_score(ranks, card_count):
    '''
    Cycles through the cards and their resulting
    ranks and generates an overall score for
    input into AoC
    '''
    total = 0
    for rank in sorted(ranks.keys(), key=lambda x: x.value, reverse=True):
        for item in ranks[rank]:
            total += card_count * item["bid"]
            card_count -= 1
    return total


def run(data):
    card_count = len(data)
    ranks = parse_cards(data)

    # Sorting the cards
    for rank in sorted(ranks.keys(), key=lambda x: x.value, reverse=True):
        ranks[rank] = sorted(
            ranks[rank],
            key=lambda x: individual_card_rank(x["cards"], CARD_ORDER),
            reverse=True,
        )

    # Totalling up the score
    total = get_score(ranks, card_count)

    return total


def run_p2(data):
    card_count = len(data)
    ranks = parse_cards_p2(data)

    # Sorting the cards
    for rank in sorted(ranks.keys(), key=lambda x: x.value, reverse=True):
        ranks[rank] = sorted(
            ranks[rank],
            key=lambda x: individual_card_rank(x["cards"], CARD_ORDER_PART2),
            reverse=True,
        )

    # Totalling up the score
    total = get_score(ranks, card_count)
    return total
