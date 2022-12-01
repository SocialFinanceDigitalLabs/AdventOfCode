from unittest import mock, TestCase, main

sample0 = '''([])
{()()()}
<([{}])>
[<>({}){}[([])<>]]
(((((((((())))))))))'''

sample1 = '''(]
{()()()>
(((()))}
<([]){()}[{}])'''

sample2 = '''[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]'''

class TestFirst(TestCase):
    def test_calculate_score(self):
        from main import calculateScore

        self.assertEqual(0, calculateScore([True, True]))
        self.assertEqual(6, calculateScore([')', ')']))
        self.assertEqual(25140, calculateScore([')', '>']))
        self.assertEqual(54042, calculateScore([')','}','}',']','>','}',']',')','>',']']))

    def test_good_code(self):
        from main import parseRow, calculateScore
        code = sample0.split("\n")
        results = []
        for row in code:
            results.append(parseRow(row))

        self.assertEqual(results, [True, True, True, True, True])
        self.assertEqual(calculateScore(results), 0)

    def test_bad_code(self):
        from main import parseRow, calculateScore
        code = sample1.split("\n")
        results = []
        for row in code:
            results.append(parseRow(row))

        self.assertEqual(results, [']', '>', '}', ')'])
        self.assertEqual(calculateScore(results), 26394)

    def test_mixed_code(self):
        from main import parseRow, calculateScore
        code = sample2.split("\n")
        results = []
        for row in code:
            results.append(parseRow(row))

        self.assertEqual(results, [True, True, '}', True, ')', ']', True, ')', '>', True])
        self.assertEqual(calculateScore(results), 26397)

    def test_get_missing_brackets(self):
        from main import parseRowV2, findClosingBrackets, calculateP2Score
        # I should really break this more into simple functions to test, but I'm tired so...
        code = sample2.split("\n")
        results = []
        for row in code:
            results.append(parseRowV2(row))

        scores = []
        for row in results:
            if row:
                closeBrackets = findClosingBrackets(row)
                scores.append(calculateP2Score(closeBrackets))

        scores = sorted(scores)
        self.assertEqual(scores[int(len(scores)/2)], 288957)

if __name__ == '__main__':
    main()