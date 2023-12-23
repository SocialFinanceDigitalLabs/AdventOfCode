import math

EXPECTED_TEST_ANSWER_PART1 = [114]
EXPECTED_TEST_ANSWER_PART2 = [2]

from math import factorial
from fractions import Fraction


class sequence:
    """
    Adapted and cleaned up version of this code:
    https://codereview.stackexchange.com/questions/277964/calculating-the-nth-term-of-a-sequence-python-3-9-5
    """

    def __init__(self, *values, sequence=True):
        self.sequence = sequence
        self.originalValues = values
        self.values = values
        self.calc = []
        self.generate_terms()

    def determine_pattern(self, temp_values, difference):
        pattern = False
        iter_count = 1
        while not pattern:
            difference_length = len(temp_values) - 1
            for n in range(difference_length):
                difference.append(
                    Fraction(temp_values[n + 1]) - Fraction(temp_values[n])
                )

            # checks if all values in 'pattern' are equal (if so, then the pattern is found)
            pattern = [difference[0]] * difference_length == difference

            # didn't find a pattern with n^x, lets raise the iterCount and try with n^x+1
            if not pattern:
                temp_values = difference
                difference = []
                iter_count += 1
        return pattern, difference, iter_count

    def generate_terms(self):
        difference = []
        temp_values = self.values

        while [temp_values[0]] * len(temp_values) != temp_values:
            pattern, difference, iter_count = self.determine_pattern(
                temp_values, difference
            )

            # this is essentially difference[0] / factorial(iterCount)
            coefficient_of_n = Fraction(difference[0], factorial(iter_count))

            # adds the found pattern to self.calc so it can be used in calculations later on
            self.calc.append([coefficient_of_n, iter_count])

            # makes a list of the nth term of the found pattern and...
            pattern_found = [
                coefficient_of_n * (n**iter_count)
                for n in range(1, len(self.values) + 1)
            ]

            temp_values = []
            difference = []

            # ...takes that away from the original values
            for n in range(len(self.values)):
                temp_values.append(
                    Fraction(self.values[n]) - Fraction(pattern_found[n])
                )

            self.values = temp_values

        self.values = list(self.originalValues)

        if temp_values[0] != 0:
            # takes that value away from the list and adds it to the nth term
            self.calc.append([temp_values[0], 0])

    def calculate(self, n):
        """
        Calculates the nth value of the sequence of numbers provided.
        nth_term_data[0] = a (coefficient of n)
        nth_term_data[1] = b (power of n)
        data is presented like: an^b
        """

        if not isinstance(n, int):
            raise ValueError("nthTerm.calculate(n) only accepts integer values of 'n'.")

        value_of_n = 0
        for nth_term_data in self.calc:
            coefficient, power = nth_term_data
            if power == 0:
                value_of_n += coefficient
            else:
                value_of_n += nth_term_data[0] * (n ** nth_term_data[1])

        return int(value_of_n) if value_of_n.denominator == 1 else value_of_n


def run(data):
    total = 0
    for line in data:
        numbers = [int(num) for num in line.split()]
        result = sequence(*numbers)
        total += result.calculate(len(numbers) + 1)
    return total


def run_p2(data):
    total = 0
    for line in data:
        numbers = [int(num) for num in line.split()]
        result = sequence(*numbers)
        total += result.calculate(0)
    return total
