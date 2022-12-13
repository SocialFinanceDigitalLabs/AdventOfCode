from aocd import get_data

session = "53616c7465645f5f932620b9dd9cb53e9facee9282730977ff26a7c28126db6fa8ce7b0" \
          "329cbec99fa54ea4d10b35d0cb2d5b3d17492e51cf4a0282caf0025e1"

packet_pairs = get_data(day=13, year=2022, session=session).split()

test = open(r"C:\Users\patrick.troy\Downloads\test.txt").read().split()


def group_list(data, group_size):
    grouped_pairs = [data[i:i+group_size] for i in range(0, len(data), group_size)]
    return grouped_pairs


grouped_pairs = group_list(test, 2)


for group in grouped_pairs:
    left, right = eval(group[0]), eval(group[1])
    print(left, right)




L = "[[], [1], [[[1, 3], 2, 1, 3]]]"
R = "[[[], 6, [3, 8]], []]"

