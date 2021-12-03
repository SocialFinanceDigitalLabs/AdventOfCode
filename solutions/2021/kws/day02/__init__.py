from collections import namedtuple
from dataclasses import dataclass
from enum import Enum


class Command(Enum):
    F = "forward"
    D = "down"
    U = "up"


@dataclass
class Instruction:
    command: Command
    value: int

    @classmethod
    def from_string(cls, value: str) -> "Instruction":
        cmd, amount = value.split(" ", 1)
        return cls(Command(cmd), int(amount))


Position = namedtuple("Position", ["x", "d"])


class Submarine:
    x = 0
    d = 0
    aim = 0

    @property
    def pos(self):
        return Position(self.x, self.d)

    def do(self, instruction: Instruction):
        if instruction.command == Command.U:
            self.d -= instruction.value
        elif instruction.command == Command.D:
            self.d += instruction.value
        elif instruction.command == Command.F:
            self.x += instruction.value
        else:
            raise ValueError(f"Unknown instruction: {instruction}")

    def do_with_aim(self, instruction: Instruction):
        if instruction.command == Command.U:
            self.aim -= instruction.value
        elif instruction.command == Command.D:
            self.aim += instruction.value
        elif instruction.command == Command.F:
            self.x += instruction.value
            self.d += self.aim * instruction.value
        else:
            raise ValueError(f"Unknown instruction: {instruction}")




