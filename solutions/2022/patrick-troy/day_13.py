from aocd import get_data

session = "53616c7465645f5f932620b9dd9cb53e9facee9282730977ff26a7c28126db6fa8ce7b0" \
          "329cbec99fa54ea4d10b35d0cb2d5b3d17492e51cf4a0282caf0025e1"

packet_pairs = get_data(day=13, year=2022, session=session).split()

test = open(r"C:\Users\Patrick\Downloads\test.txt").read().split()


def group_list(data, group_size):
    grouped_pairs = [data[i:i+group_size] for i in range(0, len(data), group_size)]
    return grouped_pairs


grouped_pairs = group_list(test, 2)


def check_bigger_int(left: int, right: int):
    if left == right:
        return "equal"
    elif left < right:
        return "right order"
    elif left > right:
        return "wrong order"


def check_both_different(left, right):
    if isinstance(left, list) and isinstance(right, int):
        right = [right]
        compare(left, right)
    if isinstance(left, int) and isinstance(right, list):
        left = [left]
        compare(left, right)


def compare(left, right):
    order = None
    if isinstance(left, list) and isinstance(right, list):
        max_len = max(len(left), len(right))
        for value in range(max_len):
            try:
                compare(left[value], right[value])
            except IndexError:
                if len(left) < len(right):
                    order = "len, right order"
                else:
                    order = "len, wrong order"
        return order
    if isinstance(left, int) and isinstance(right, int):
        if check_bigger_int(left, right) == "right order":
            order = "right order"
        if check_bigger_int(left, right) == "wrong order":
            order = "wrong order"
        else:
            pass
        return order
    else:
        return check_both_different(left, right)


pair_dict = {}
index = 1
for group in grouped_pairs:
    print(group)
    left, right = eval(group[0]), eval(group[1])
    pair_dict[index] = compare(left, right)
    print(compare(left, right))
    index += 1


print(pair_dict)