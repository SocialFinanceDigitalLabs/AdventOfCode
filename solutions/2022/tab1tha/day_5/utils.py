from collections import defaultdict


def process_stacks(stacks):
    for line in stacks.split("\n"):
        ind_max = len(line)
        break
    # the elements appear at intervals of 4 across the length
    indices = list(range(1, ind_max, 4))

    stack_dict = defaultdict(list)
    for line in stacks.split("\n"):
        for ind in indices:
            if line[ind] != " ":
                stack_dict[ind].append(line[ind])
    stack_dict = {v.pop(): list(reversed(v)) for k, v in stack_dict.items()}
    return stack_dict


def process_move(move):
    lst = move.split(" ")
    lst.remove("move")
    lst.remove("from")
    lst.remove("to")
    return lst


def get_top(stack_dict):
    result = ""
    stack_keys = list(stack_dict.keys())
    stack_keys.sort()
    for k in stack_keys:
        top = stack_dict[k][-1]
        result += top
    return result
