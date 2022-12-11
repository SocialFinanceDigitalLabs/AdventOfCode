EXPECTED_TEST_ANSWER_PART1 = [15]
EXPECTED_TEST_ANSWER_PART2 = [12]

OP_MOVES = ["A", "B", "C"]
YOUR_MOVES = ["X", "Y", "Z"]


def get_shape_score(move):
    """
    Determine the move's score (not if you win or lose)
    """
    if move == "A" or move == "X":
        # Rock
        return 1
    elif move == "B" or move == "Y":
        # Paper
        return 2
    else:
        # Scissors
        return 3


def get_game_score(op_move, your_move):
    """
    Determine the score by the move
    """
    if OP_MOVES.index(op_move) == YOUR_MOVES.index(your_move):
        # A tie
        return 3
    elif (OP_MOVES.index(op_move) + 1) % 3 == YOUR_MOVES.index(your_move):
        # A win
        return 6
    else:
        # A loss
        return 0


def get_shape(op_move, goal):
    """
    Determine which move to use given an expected outcome (goal)
    """
    if goal == "X":
        # Goal is a loss, so look to the entry one before it in the list
        return YOUR_MOVES[(OP_MOVES.index(op_move) - 1) % 3]
    elif goal == "Y":
        # Goal is a tie, so copy the move type
        return YOUR_MOVES[OP_MOVES.index(op_move)]
    else:
        # Goal is a win, so look one entry to the right for the winning move
        return YOUR_MOVES[(OP_MOVES.index(op_move) + 1) % 3]


def run(data):
    score = 0
    for row in data:
        moves = row.split(" ")
        score += get_shape_score(moves[1])
        score += get_game_score(moves[0], moves[1])
    return score


def run_p2(data):
    score = 0
    for row in data:
        moves = row.split(" ")
        # Translate the result into a shape so we can just reuse the part 1 answer code
        shape = get_shape(moves[0], moves[1])

        score += get_shape_score(shape)
        score += get_game_score(moves[0], shape)
    return score
