import re

EXPECTED_TEST_ANSWER_PART1 = [142, 209]
EXPECTED_TEST_ANSWER_PART2 = [142, 281]

NUMBERS = {
    "one": {"Value": "1"},
    "two": {"Value": "2"},
    "three": {"Value": "3"},
    "four": {"Value": "4"},
    "five": {"Value": "5"},
    "six": {"Value": "6"},
    "seven": {"Value": "7"},
    "eight": {"Value": "8"},
    "nine": {"Value": "9"},
}


def getDigitsFromString(row):
    digits = re.findall(r"\d", row)
    value = 0
    if digits:
        value = int(digits[0] + digits[-1])

    return value


def run(data):
    """
    Takes a list of values in "data" and returns the total
    of first and last digits concatenated in the string
    """
    total = 0
    for row in data:
        value = getDigitsFromString(row)
        total += value
    return total


def replaceNumericalWords(row: str, lowestValue: dict, highestValue: dict) -> str:
    """
    Take where we found the first and last numerical words in the string, and replace them with
    the related values
    """
    newstr = row[: lowestValue["Value"]]
    newstr += NUMBERS[lowestValue["Key"]]["Value"]
    newstr += row[
        lowestValue["Value"] + len(lowestValue["Key"]) : highestValue["Value"]
    ]
    newstr += NUMBERS[highestValue["Key"]]["Value"]
    newstr += row[highestValue["Value"] + len(highestValue["Key"]) :]
    return newstr


def run_p2(data):
    """
    Takes a list of values in "data" and returns the total
    of first and last digits concatenated in the string.
    First and last digits now include number words
    """
    total = 0

    for row in data:
        lowestValue = {"Key": "", "Value": 99}
        highestValue = {"Key": "", "Value": -1}
        for key in NUMBERS.keys():
            if key not in row:
                continue
            findFirst = row.find(key)
            findLast = row.rfind(key)
            if findFirst < lowestValue["Value"]:
                lowestValue["Key"] = key
                lowestValue["Value"] = findFirst
            if findLast > highestValue["Value"]:
                highestValue["Key"] = key
                highestValue["Value"] = findLast

        if lowestValue["Value"] != 99:
            row = replaceNumericalWords(row, lowestValue, highestValue)

        value = getDigitsFromString(row)
        total += value
    return total
