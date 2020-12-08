#! /usr/bin/env python
import argparse

from tqdm import tqdm

import kws.bootcode as bc


def test_run(instructions):
    """
    Tries running the modified instruction to see if
    :param instructions:
    :return:
    """
    con = bc.HandheldConsole(instructions)
    try:
        while con.run():
            pass
    except RecursionError:
        return False, None

    return True, con


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Day 8 of Advent of Code 2020')
    parser.add_argument('file', metavar='filename', type=argparse.FileType('rt'),
                        help='filename to your personal inputs')
    parser.add_argument('--test', '-t', action='store_true')

    args = parser.parse_args()

    if args.test:
        import doctest
        doctest.testmod()
        doctest.testmod(bc)
        print("Tests completed")
        exit(0)

    with args.file as FILE:
        input_lines = FILE.readlines()

    instructions = [bc.Instruction(i) for i in input_lines]

    con = bc.HandheldConsole(instructions)

    try:
        while con.run():
            pass
    except RecursionError as ex:
        print(ex)

    con = None
    for i in tqdm(instructions):
        if i.cmd == "jmp":
            i.cmd = "nop"
            completed, con = test_run(instructions)
            if completed:
                break
            else:
                i.cmd = "jmp"

    if con is not None:
        print("Successful completion: ", con)
    else:
        print("No solution found.")
