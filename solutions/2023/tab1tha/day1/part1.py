def get_calibration_values(line: str) -> int:
    digits = [c for c in line if c.isdigit()]
    if len(digits) > 1:
        return int("".join([digits[0], digits[-1]]))
    else:
        return int("".join([digits[0], digits[0]]))


def calib_sum(cal_values: list) -> int:
    return sum(cal_values)


def day1_part1(filepath: str):
    with open(filepath, "r") as f:
        cal_values = [get_calibration_values(line) for line in f]
    return calib_sum(cal_values)


if __name__ == "__main__":
    result = day1_part1(filepath="day1\input1.txt")
    print(result)
