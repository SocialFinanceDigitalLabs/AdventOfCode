def get_calibration_values(line:str) -> int:
    digits = [c for c in line if c.isdigit()]
    return int("".join([digits[0], digits[-1]]))

def calib_sum(cal_values:list) -> int:
    return sum(cal_values)

if __name__ == "__main__":
    with open("day1\input1.txt", "r") as f:
        cal_values = [get_calibration_values(line) for line in f]
    print(calib_sum(cal_values))