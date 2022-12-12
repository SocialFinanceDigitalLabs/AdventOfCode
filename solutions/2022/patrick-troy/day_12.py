from aocd import get_data

session = "53616c7465645f5f932620b9dd9cb53e9facee9282730977ff26a7c28126db6fa8ce7b0" \
          "329cbec99fa54ea4d10b35d0cb2d5b3d17492e51cf4a0282caf0025e1"

hill_map = get_data(day=12, year=2022, session=session)

test = [line.strip() for line in open(r"C:\Users\patrick.troy\Downloads\test.txt")]

print(test)

