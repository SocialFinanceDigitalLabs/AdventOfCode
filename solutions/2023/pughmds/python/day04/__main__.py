import math

EXPECTED_TEST_ANSWER_PART1 = [13]
EXPECTED_TEST_ANSWER_PART2 = [30]

def parseCard(card):
    # Find the position of the colon in "Card 1:"
    colon_index = card.index(':')

    # Extract the card number
    card_number = int(card[5:colon_index])

    # Split the string based on the pipe (|) character
    left_part, right_part = card[colon_index + 1:].split('|')

    # Convert the substrings to lists of integers
    winning_numbers = [int(num) for num in left_part.split() if num.isdigit()]
    numbers = [int(num) for num in right_part.split() if num.isdigit()]

    return card_number, winning_numbers, numbers


def run(data):
    """
    Determines if the numbers on the right appear in the winning number list on the left
    Scores based on a power of two depending on how many matches there are.
    """
    total = 0
    for card in data:
        card_number, winning_numbers, numbers = parseCard(card)

        winning_set = set(winning_numbers)
        numbers_set = set(numbers)

        # Find common elements
        common_elements = winning_set.intersection(numbers_set)
        if len(common_elements) > 0:
            total += (2**(len(common_elements)-1))

    return total


def run_p2(data):
    """
    Same as above, but crazy rules involving...more scratch cards?
    """

    total = 0
    cards = []
    for card in data:
        # This time, we need to parse each card separately
        card_number, winning_numbers, numbers = parseCard(card)
        cards.append({"win": set(winning_numbers), "numbers": set(numbers), "copies": 1})

    # Next, we need to create duplicates based on wins
    for index, card in enumerate(cards):
        # Get the winning numbers in the card
        common_elements = card["win"].intersection(card["numbers"])
        # Count how many and add to the "copies" of the next n cards.
        for n in range(index+1, len(common_elements)+index+1):
            print(n)
            try:
                # We win the number of cards again
                cards[n]["copies"] += cards[index]["copies"]
            except IndexError as err:
                # In case we go over the size of the list, just ignore the problem
                continue

    # Add up the number of cards we have
    for card in cards:
        total += card["copies"]

    return total
