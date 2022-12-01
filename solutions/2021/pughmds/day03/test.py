from unittest import mock, TestCase, main

sample1 = [
    "00100",
    "11110",
    "10110",
    "10111",
    "10101",
    "01111",
    "00111",
    "11100",
    "10000",
    "11001",
    "00010",
    "01010"
]

class TestFirst(TestCase):
    def test_bit_count(self):
        from main import getBitCount
        result = getBitCount(["01010","11001", "11100"])
        self.assertEqual(result, [2, 3, 1, 1, 1])

        result = getBitCount(["11111", "11001", "00110"])
        self.assertEqual(result, [2, 2, 2, 2, 2])

        result = getBitCount(["00001", "10000", "01110"])
        self.assertEqual(result, [1, 1, 1, 1, 1])

        result = getBitCount(sample1)
        self.assertEqual(result, [7, 5, 8, 7, 5])

    def test_gamma_rate(self):
        from main import getGammaRate
        result = getGammaRate(["01010","11001", "11100"])
        self.assertEqual(result, "11000")

        result = getGammaRate(["11111", "11001", "00110"])
        self.assertEqual(result, "11111")

        result = getGammaRate(["00001", "10000", "01110"])
        self.assertEqual(result, "00000")

        result = getGammaRate(sample1)
        self.assertEqual(result, "10110")

    def test_epsilon_rate(self):
        from main import getGammaRate, getEpsilonRate
        gamma = getGammaRate(["01010","11001", "11100"])
        result = getEpsilonRate(gamma)
        self.assertEqual(result, "00111")

        gamma = getGammaRate(["11111", "11001", "00110"])
        result = getEpsilonRate(gamma)
        self.assertEqual(result, "00000")

        gamma = getGammaRate(["00001", "10000", "01110"])
        result = getEpsilonRate(gamma)
        self.assertEqual(result, "11111")

        gamma = getGammaRate(sample1)
        result = getEpsilonRate(gamma)
        self.assertEqual(result, "01001")

    def test_power_rate(self):
        from main import getPowerConsumptionFromRates
        result = getPowerConsumptionFromRates('00010','00100')
        self.assertEqual(result, 8)

        result = getPowerConsumptionFromRates('11001', '11110')
        self.assertEqual(result, 750)

    def test_V1(self):
        from main import getPowerConsumption
        power = getPowerConsumption(sample1)
        self.assertEqual(power, 198)

    def test_getO2Rating(self):
        from main import getO2Rating

        result = getO2Rating(["100", "011", "010", "110"])
        self.assertEqual(result, "110")

        result = getO2Rating(sample1)
        self.assertEqual(result, "10111")

    def test_getCO2Rating(self):
        from main import getCO2Rating

        result = getCO2Rating(sample1)
        self.assertEqual(result, "01010")

    def test_lifeSupportRating(self):
        from main import getLifeSupportRating

        result = getLifeSupportRating(sample1)
        self.assertEqual(result, 230)

if __name__ == '__main__':
    main()
