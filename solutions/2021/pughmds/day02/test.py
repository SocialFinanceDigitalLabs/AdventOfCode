from unittest import mock, TestCase, main

sample1 = [
    "forward 5",
    "down 5",
    "forward 8",
    "up 3",
    "down 8",
    "forward 2"
]

class TestFirst(TestCase):
    def test_input(self):
        from main import parseInput
        commands = parseInput(["forward 4"])
        self.assertEqual(commands, [{"command": "forward", "distance": 4}])

        commands = parseInput(["up 3"])
        self.assertEqual(commands, [{"command": "up", "distance": 3}])

        commands = parseInput(["down 12"])
        self.assertEqual(commands, [{"command": "down", "distance": 12}])

        commands = parseInput(["down 12"])
        self.assertEqual(commands, [{"command": "down", "distance": 12}])

        commands = parseInput(["up -7"])
        self.assertEqual(commands, [{"command": "up", "distance": -7}])

    def test_V1(self):
        from main import parseInput, traceDirectionsV1
        position = {"horizontal": 0, "depth": 0}
        commands = parseInput(sample1)
        position = traceDirectionsV1(commands, position)
        self.assertEqual(position["horizontal"] * position["depth"], 150)

    def test_V2(self):
        from main import parseInput, traceDirectionsV2
        position = {"horizontal": 0, "depth": 0, "aim": 0}
        commands = parseInput(sample1)
        position = traceDirectionsV2(commands, position)
        self.assertEqual(position["horizontal"] * position["depth"], 900)


if __name__ == '__main__':
    main()
