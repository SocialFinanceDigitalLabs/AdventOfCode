#!/usr/bin/env python
import argparse
import numpy as np
from collections import namedtuple

Schedule = namedtuple('Schedule', 't offset')


def __all_offsets(t, schedules):
    for s in schedules:
        print(s.t, t % s.t, end=", ")
    print()


def get_period(schedule, minimum):
    if schedule == minimum:
        return schedule.t

    corroffset = schedule.offset % minimum.t
    for t in range(0, max(schedule.t, schedule.offset)):
        offset = (t * schedule.t) % minimum.t
        if offset == corroffset:
            return t * schedule.t


def rollback(ix, schedules):
    amount = 0
    first = schedules[ix]
    right = schedules[0:ix]

    while first.offset != 0:
        lcm = np.lcm.reduce([s.t for s in right])
        schedules = [Schedule(s.t, (s.offset - lcm) % s.t) for s in schedules]
        amount += lcm
        first = schedules[ix]

    return amount, schedules


def find_periods(schedules):
    schedules = [Schedule(int(t), ix) for ix, t in enumerate(schedules.split(",")) if t != "x"]
    rollback_amount = 0
    for ix in range(0, len(schedules)):
        amount, schedules = rollback(ix, schedules)
        rollback_amount += amount

    print("First matching timestamp",  np.lcm.reduce([s.t for s in schedules]) % rollback_amount)


def day13(eta, schedules):
    eta = int(eta)
    times = [int(x) for x in schedules.split(",") if x != "x"]

    arrivals = [(a, a - eta % a) for a in times]
    arrivals.sort(key=lambda x: x[1])

    print(f"The first bus to arrive is bus {arrivals[0][0]} after {arrivals[0][1]} minutes: "
          f"{arrivals[0][0] * arrivals[0][1]}")

    find_periods(schedules)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Day 13 of Advent of Code 2020')
    parser.add_argument('--file', metavar='filename', type=argparse.FileType('rt'),
                        help='filename to your personal inputs')
    parser.add_argument('--sample', action='store_true', help='Run against sample input')

    args = parser.parse_args()

    if args.sample:
        day13("939", "7,13,x,x,59,x,31,19")
        find_periods("17,x,13,19")
        find_periods("67,7,59,61")
        find_periods("67,x,7,59,61")
        find_periods("67,7,x,59,61")
        find_periods("1789,37,47,1889")

    if args.file:
        with args.file as FILE:
            input_lines = FILE.readlines()
        day13(*input_lines)
