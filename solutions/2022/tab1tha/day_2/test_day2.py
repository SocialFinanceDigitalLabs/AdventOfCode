from day2_task1 import strategy_score
from day2_task2 import planned_score


def test_strategy():
    elf_strategy = """A Y
B X
C Z"""
    score = strategy_score(elf_strategy)
    assert score == 15

def test_plan():
    elf_strategy = """A Y
B X
C Z"""
    score = planned_score(elf_strategy)
    assert score == 12
