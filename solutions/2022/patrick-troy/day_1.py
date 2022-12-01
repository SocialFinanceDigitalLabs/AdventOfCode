import pandas as pd

data = pd.read_csv(r"C:\Users\patrick.troy\Downloads\day_1.csv", skip_blank_lines=False, header=None)

# PART 1
max_calories = 0
current_calories = 0

for row in data[0]:
    if pd.notna(row):
        current_calories += row
    else:
        max_calories = current_calories if current_calories > max_calories else max_calories
        current_calories = 0

print(max_calories)

# PART 2
max_calories_each = 0
max_calories_all = []

for row in data[0]:
    if pd.notna(row):
        max_calories_each += row
    else:
        max_calories_all.append(max_calories_each)
        max_calories_each = 0

print(sum(sorted(max_calories_all)[-3:]))
