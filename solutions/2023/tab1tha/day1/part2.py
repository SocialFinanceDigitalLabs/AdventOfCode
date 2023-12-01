from part1 import calib_sum


def words_and_nums(line: str) -> str:
    word_to_num = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    nums_found = []
    #  step through a line in steps of five: max(len(word_to_num.keys)) = 5
    for i in range(0, len(line)):
        if line[i].isdigit():
            nums_found.append(line[i])
        for num_word in word_to_num.keys():
            #  if a word number is in the line, replace it with the corresponding number
            if i + 5 <= len(line):
                phrase = line[i : i + 5]
            else:
                phrase = line[i:]
            if phrase.startswith(num_word):
                nums_found.append(int(word_to_num[num_word]))

    first_num = nums_found[0]
    if len(nums_found) > 1:
        last_num = nums_found[-1]
    else:
        last_num = first_num
    cal_value = f"{first_num}{last_num}"
    return int(cal_value)


def day2_part2(filepath: str):
    with open(filepath, "r") as f:
        cal_values = [words_and_nums(line) for line in f.readlines()]
    return calib_sum(cal_values)


if __name__ == "__main__":
    result = day2_part2(filepath="day1\input1.txt")
    print(result)
