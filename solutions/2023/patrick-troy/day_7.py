from aocd import get_data

session = "53616c7465645f5f5e959babee3b98732450e5a8dc2320e845ed91c80b7f39fe01f7" \
          "c01baa3710d5d1e1f631fe6c9f768fc1a035e9c3d5cd00e23c7ea0637cae"

data = get_data(day=7, year=2023, session=session).split("\n")

test = [
    "32T3K 765",
    "T55J5 684",
    "KK677 28",
    "KTJJT 220",
    "QQQJA 483",
]


def _create_dict(puzzle_input):
    puzzle_list = []
    for row in puzzle_input:
        hand, bid = row.split()[0], row.split()[1]
        hand = hand.translate(str.maketrans("TJQKA", "ABCDE"))
        puzzle_list.append({hand: int(bid)})

    return puzzle_list


def _game_sorter(puzzle_input):
    games_sorted = {
        "five_of_a_kind": [],
        "four_of_a_kind": [],
        "full_house": [],
        "three_of_a_kind": [],
        "two_pair": [],
        "one_pair": [],
        "high_card": [],
    }
    puzzle_list = _create_dict(puzzle_input)
    for game in puzzle_list:
        hand = list(game.keys())[0]
        if any(hand.count(x) == 5 for x in hand):
            games_sorted["five_of_a_kind"].append(hand)
        elif any(hand.count(x) == 4 for x in hand):
            games_sorted["four_of_a_kind"].append(hand)
        elif any(hand.count(x) == 3 for x in hand) and any(hand.count(x) == 2 for x in hand):
            games_sorted["full_house"].append(hand)
        elif any(hand.count(x) == 3 for x in hand):
            games_sorted["three_of_a_kind"].append(hand)
        elif any(hand.count(x) == 2 for x in hand):
            if list(hand.count(x) for x in hand).count(2) == 4:
                games_sorted["two_pair"].append(hand)
            else:
                games_sorted["one_pair"].append(hand)
        else:
            games_sorted["high_card"].append(hand)

    return games_sorted


def _hand_sorter(puzzle_input):
    sorted_hands = []
    game_dict = _game_sorter(puzzle_input)
    for _type, games in game_dict.items():
        sorted_hands.extend(sorted(games, reverse=True))

    return sorted_hands


def _point_giver(puzzle_input):
    puzzle_list = _create_dict(puzzle_input)
    print(puzzle_list)
    sorted_hands = _hand_sorter(puzzle_input)

    for i, hand in enumerate(reversed(sorted_hands), 1):
        print(i, hand)


print(_point_giver(test))
