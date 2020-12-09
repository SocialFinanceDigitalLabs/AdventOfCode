from typing import List


class Instruction:
    """
    Create an instruction from an input line

    >>> Instruction("jmp +3")
    jmp 3 0
    """

    def __init__(self, value: str):
        self.cmd, self.arg = Instruction.parse_instruction(value)
        self.execution_count = 0

    def __str__(self):
        return f"{self.cmd} {self.arg} {self.execution_count}"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def parse_instruction(value: str):
        """
        Parses an instruction input

        >>> Instruction.parse_instruction("nop +0")
        ('nop', 0)

        >>> Instruction.parse_instruction("acc +5")
        ('acc', 5)

        >>> Instruction.parse_instruction("jmp -5")
        ('jmp', -5)

        :param value:
        :return:
        """
        cmd, arg = value.split(" ")
        arg = int(arg)
        assert cmd in ["nop", "acc", "jmp"]
        return cmd, arg


class HandheldConsole:
    """
    An emulator for a handheld console bootcode.

    >>> con = HandheldConsole([Instruction("acc +5"), Instruction("acc -2"), Instruction("jmp -2")])
    >>> con.run()
    >>> con.accumulator
    5
    >>> con.run()
    >>> con.accumulator
    3
    >>> con.run()
    >>> con.address
    0
    >>> con.run()
    Traceback (most recent call last):
    ...
    RecursionError: Max recursion depth has been reached on 0 with 3
    """
    accumulator = 0
    address = 0

    def __init__(self, instructions: List[Instruction], max_recursion_depth=1):
        self.instructions = instructions
        self.max_recursion_depth = max_recursion_depth
        self.reset()

    def __str__(self):
        return f"add={self.address} acc={self.accumulator}"

    def reset(self):
        for i in self.instructions:
            i.execution_count = 0
        self.accumulator = 0
        self.address = 0

    def run(self):
        instruction = self.instructions[self.address]
        if instruction.execution_count >= self.max_recursion_depth:
            raise RecursionError(f"Max recursion depth has been reached on {self.address} with {self.accumulator}")
        self._execute_(instruction)
        return self.address < len(self.instructions)

    def _execute_(self, instruction):
        cmd = instruction.cmd
        if cmd == "nop":
            self.address += 1
        elif cmd == "acc":
            self.accumulator += instruction.arg
            self.address += 1
        elif cmd == "jmp":
            self.address += instruction.arg
        instruction.execution_count += 1


if __name__ == "__main__":
    import doctest
    doctest.testmod()
