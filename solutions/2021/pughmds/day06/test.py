from unittest import mock, TestCase, main
import numpy as np

sample1 = """3,4,3,1,2"""

class TestFirst(TestCase):
    def test_v1_part1(self):
        from main import step, parseInput

        fish = parseInput(sample1)
        for i in range(0,80):
            fish = step(fish)

        self.assertEqual(len(fish), 5934)

    def test_v2_part1(self):
        from main import stepV2, parseInput

        fish = parseInput(sample1)
        fishTrack = np.array([
            len(fish[fish == 0]),
            len(fish[fish == 1]),
            len(fish[fish == 2]),
            len(fish[fish == 3]),
            len(fish[fish == 4]),
            len(fish[fish == 5]),
            len(fish[fish == 6]),
            len(fish[fish == 7]),
            len(fish[fish == 8])
        ], dtype=np.int64)
        for i in range(0, 80):
            fishTrack = stepV2(fishTrack)

        self.assertEqual(np.sum(fishTrack), 5934)

    def test_v2_part2(self):
        from main import stepV2, parseInput

        fish = parseInput(sample1)
        fishTrack = np.array([
            len(fish[fish == 0]),
            len(fish[fish == 1]),
            len(fish[fish == 2]),
            len(fish[fish == 3]),
            len(fish[fish == 4]),
            len(fish[fish == 5]),
            len(fish[fish == 6]),
            len(fish[fish == 7]),
            len(fish[fish == 8])
        ], dtype=np.int64)
        for i in range(0, 256):
            fishTrack = stepV2(fishTrack)

        self.assertEqual(np.sum(fishTrack), 26984457539)

if __name__ == '__main__':
    main()
