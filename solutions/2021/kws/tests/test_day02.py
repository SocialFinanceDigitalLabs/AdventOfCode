import unittest

import day02


class TestDay02(unittest.TestCase):

    def test_parse_instruction(self):
        self.assertEqual(day02.Instruction.from_string("up 4"), day02.Instruction(day02.Command.U, 4))
        self.assertEqual(day02.Instruction.from_string("down 2"), day02.Instruction(day02.Command.D, 2))
        self.assertEqual(day02.Instruction.from_string("forward -5"), day02.Instruction(day02.Command.F, -5))

    def test_submarine(self):
        sub = day02.Submarine()
        self.assertEqual(sub.pos, (0, 0))

        sub.do(day02.Instruction(day02.Command.D, 5))
        self.assertEqual(sub.pos, (0, 5))

        sub.do(day02.Instruction(day02.Command.U, 3))
        self.assertEqual(sub.pos, (0, 2))

        sub.do(day02.Instruction(day02.Command.F, 10))
        self.assertEqual(sub.pos, (10, 2))

    def test_submarine_with_aim(self):
        sub = day02.Submarine()
        self.assertEqual(sub.pos, (0, 0))

        sub.do_with_aim(day02.Instruction(day02.Command.F, 5))
        self.assertEqual(sub.pos, (5, 0))

        sub.do_with_aim(day02.Instruction(day02.Command.D, 5))
        self.assertEqual(sub.pos, (5, 0))

        sub.do_with_aim(day02.Instruction(day02.Command.F, 8))
        self.assertEqual(sub.pos, (13, 40))


if __name__ == '__main__':
    unittest.main()
