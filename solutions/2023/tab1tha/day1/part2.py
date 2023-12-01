from part1 import get_calibration_values, calib_sum
def word_to_num(line:str) -> str:
    word_to_num = {"one":"1", "two":"2", "three":"3", "four":"4", "five":"5",
                   "six":"6", "seven":"7", "eight":"8", "nine":"9", "zero":"0"}
    #  step through a line in steps of five: max(len(word_to_num.keys)) = 5
    for i in range(0, len(line)):
        for num_word in word_to_num.keys():
            #  if a word is in the line, replace it with the corresponding number
            if num_word in line[i:i+5]:
                line = line.replace(num_word, word_to_num[num_word])
    return line

if __name__ == "__main__":
    with open("day1\input1.txt", "r") as f:
        cal_values = [get_calibration_values(word_to_num(line)) for line in f]
    print(calib_sum(cal_values))