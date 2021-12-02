from unittest import mock, TestCase, main

sample1 = [
    199,
    200,
    208,
    210,
    200,
    207,
    240,
    269,
    260,
    263,
]

class TestFirst(TestCase):
    def test_sample(self):
        from task import countChanges
        result = countChanges(sample1)
        print(result)
        self.assertEqual(result["increase"], 7)

class TestSecond(TestCase):
    def test_sample(self):
        from task import countSumChanges
        result = countSumChanges(sample1)
        print(result)
        self.assertEqual(result["increase"], 5)

if __name__ == '__main__':
    main()
