from day5_task1 import restacker
from day5_task2 import restacker_pro

with open("test_input_day5.txt", "r") as f:
    plan = f.read()


def test_restacker():
    assert restacker(plan) == "CMZ"


def test_restacker_pro():
    assert restacker_pro(plan) == "MCD"
