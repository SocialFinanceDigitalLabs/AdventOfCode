from unittest import mock, TestCase, main

sample1 = """acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"""

sample2 = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

class TestFirst(TestCase):
    def test_parse(self):
        from main import parseInput

        signalPatterns, outputValues = parseInput(sample1)

        self.assertEqual(outputValues, [["cdfeb", "fcadb", "cdfeb", "cdbaf"]])

    def test_outputCount(self):
        from main import parseInput, countUnique

        signalPatterns, outputValues = parseInput(sample1)
        result = countUnique(outputValues[0])
        self.assertEqual(result, 0)

        result = countUnique(signalPatterns[0])
        self.assertEqual(result, 4)

        signalPatterns, outputValues = parseInput(sample2)
        total = 0
        for output in outputValues:
            total += countUnique(output)
        self.assertEqual(total, 26)

    def test_decoding(self):
        from main import parseInput, determineValue
        signalPatterns, outputValues = parseInput(sample1)
        result = determineValue(signalPatterns[0])
        self.assertEqual(result, ['cagedb', 'ab', 'gcdfa', 'fbcad', 'eafb', 'cdfbe', 'cdfgeb', 'dab', 'acedgfb', 'cefabd'])

    def test_easySampleScore(self):
        from main import run
        valueSum = run(sample1)

        self.assertEqual(valueSum, 5353)

    def test_easySampleScore(self):
        from main import run
        valueSum = run(sample2)

        self.assertEqual(valueSum, 61229)

if __name__ == '__main__':
    main()