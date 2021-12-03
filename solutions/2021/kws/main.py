#! /usr/bin/env python

import argparse
import importlib

parser = argparse.ArgumentParser("Advent of Code")
parser.add_argument("day", type=int, help="The day to run")
parser.add_argument("input_id", type=str, help="The input id, e.g. 'sample'")

args = parser.parse_args()

day = f"day{args.day:02}"

module = importlib.import_module(f'{day}.__main__')
module.main(f'{day}/input_{args.input_id}.txt')
