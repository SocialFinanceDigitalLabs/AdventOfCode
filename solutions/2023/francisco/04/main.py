from util import FileParser
import os
from collections import defaultdict
dir_path = os.path.dirname(os.path.realpath(__file__))


class Card:
    id: int
    winners: list[int]
    candidates: list[int]

    def __init__(self, raw: str) -> None:
        card, values = raw.split(":")
        winners, candidates = values.split("|")
        self.id = int(card.replace("Card", "").strip())
        self.winners = [int(nr.strip()) for nr in winners.strip().split(" ") if nr]
        self.candidates = [
            int(nr.strip()) for nr in candidates.strip().split(" ") if nr
        ]

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}{self.id}"
        )
    
    def get_matching_numbers(self):
        return [w for w in self.winners if w in self.candidates]

    def get_result(self):
        winners = self.get_matching_numbers()
        if not winners:
            return 0
        if len(winners) == 1:
            return 1

        result = 1
        for _ in winners[1:]:
            result = result * 2
        return result


def part_1(file: str):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    data = parser.read()
    result = 0
    for raw_card in data:
        card = Card(raw_card)
        result += card.get_result()

    return result


def part_2(file):
    """should return the solution"""
    parser = FileParser(dir_path, file)
    data = parser.read()

    cards: list[Card] = []
    for raw_card in data:
        card = Card(raw_card)
        cards.append(card)
    

    cards_count = {card.id: 1 for card in cards}
    for card in cards:
        matches = card.get_matching_numbers()
        for _ in range(cards_count[card.id]):       
            card_id = card.id
            for _ in matches:
                card_id += 1
                cards_count[card_id] += 1
    return sum(cards_count.values())


