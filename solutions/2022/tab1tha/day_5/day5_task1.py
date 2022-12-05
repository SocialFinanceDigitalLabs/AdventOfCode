from utils import process_stacks, process_move, get_top


def mover(moves, stack_dict):
    for move in moves:
        num, start, end = move
        for i in range(int(num)):
            element = stack_dict[start].pop()
            stack_dict[end].append(element)
    return stack_dict


def restacker(plan):
    stacks, moves = plan.split("\n\n")
    # get stacks into lists
    stack_dict = process_stacks(stacks)
    # get moves into a df
    moves = [process_move(move) for move in moves.split("\n")]
    stack_dict = mover(moves, stack_dict)
    result = get_top(stack_dict)
    return result


with open("input_day5.txt", "r") as f:
    plan = f.read()

result = restacker(plan)
print(result)
