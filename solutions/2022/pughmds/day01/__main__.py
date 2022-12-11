EXPECTED_TEST_ANSWER_PART1 = [24000]
EXPECTED_TEST_ANSWER_PART2 = [45000]


def set_max(calories, max_calories):
    """
    Returns the larger value
    """
    return calories if calories > max_calories else max_calories


def run(data):
    """
    Takes a list of values in "data" and returns sum of the largest
    group. Groups are separated by blank entries in the list.
    """
    max_calories = 0
    calories = 0
    for item in data:
        item = item.strip()
        if item != "":
            calories += int(item)
        else:
            max_calories = set_max(calories, max_calories)
            calories = 0
    max_calories = set_max(calories, max_calories)

    return max_calories


def run_p2(data):
    """
    Takes a list of values in "data" and returns sum of the largest
    group. Groups are separated by blank entries in the list.
    """
    calorie_list = []
    calories = 0
    for item in data:
        item = item.strip()
        if item != "":
            calories += int(item)
        else:
            calorie_list.append(calories)
            calories = 0
    calorie_list.append(calories)

    return sum(sorted(calorie_list, reverse=True)[:3])
