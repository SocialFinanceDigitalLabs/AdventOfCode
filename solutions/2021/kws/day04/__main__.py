from common import standard_setup
import day04


def main(*argv):
    lines = standard_setup(*argv)

    numbers, boards = day04.parse_input(lines)
    board_dimension = boards[0].rows.shape[0]
    print(f"Read {len(numbers)} numbers and {len(boards)} boards. The boards are {board_dimension}x{board_dimension}.")

    for ix in range(board_dimension, len(numbers)+1):
        drawn = numbers[:ix]
        for b in boards:
            winning = b.bingo(drawn)
            if winning is not None:
                break
        if winning is not None:
            break

    winning_sum = b.sum_unmarked(drawn)
    print(f"Drew {drawn[-1]} and got a winning row {winning} with {winning_sum}: {winning_sum * drawn[-1]}")

    for ix in range(board_dimension, len(numbers)+1):
        drawn = numbers[:ix]
        for b in boards:
            winning = b.bingo(drawn)
            if winning is not None:
                boards.remove(b)
                print(f"Win after {len(drawn)}. {len(boards)} boards left.")
                winning_board = b
                winning_drawn = drawn

    print(f"Last win was after {len(winning_drawn)} numbers.")
    winning_sum = winning_board.sum_unmarked(winning_drawn)
    print(f"Drew {winning_drawn[-1]} and matched with {winning_sum}: {winning_sum * winning_drawn[-1]}")


if __name__ == "__main__":
    main()
