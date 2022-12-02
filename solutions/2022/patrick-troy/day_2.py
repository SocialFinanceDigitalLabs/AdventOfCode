X = 1
Y = 2
Z = 3

win_combo = {"A": Y, "B": Z, "C": X}
draw_combo = {"A": X, "B": Y, "C": Z}
lose_combo = {"A": Z, "B": X, "C": Y}

converter = {"X": 1, "Y": 2, "Z": 3}

win = 6
draw = 3
lose = 0

points = 0

data = [line.strip() for line in open(r"C:\Users\patrick.troy\Downloads\day_2.txt")]

# PART 1
for combination in data:
    if combination[2] == "X":
        points += X
    if combination[2] == "Y":
        points += Y
    if combination[2] == "Z":
        points += Z

    if win_combo[combination[0]] == converter[combination[2]]:
        points += win
    if draw_combo[combination[0]] == converter[combination[2]]:
        points += draw
    elif lose_combo[combination[0]] == converter[combination[2]]:
        points += lose

print(points)

# PART 2
points = 0
secret_combo = {"X": "lose", "Y": "draw", "Z": "win"}

for combination in data:
    if secret_combo[combination[2]] == "lose":
        points += lose
        points += lose_combo[combination[0]]
    if secret_combo[combination[2]] == "draw":
        points += draw
        points += draw_combo[combination[0]]
    elif secret_combo[combination[2]] == "win":
        points += win
        points += win_combo[combination[0]]

print(points)
