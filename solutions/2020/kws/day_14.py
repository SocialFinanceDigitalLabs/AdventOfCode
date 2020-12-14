#!/usr/bin/env python
import argparse
import re

def get_ones_mask(mask):
    """
    Calculates the mask used to set 1 values

    >>> get_ones_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")
    64

    >>> f"{get_ones_mask('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X'):b}"
    '1000000'

    :param mask:
    :return:
    """
    return int(mask.replace("X", "0"), 2)


def get_zeroes_mask(mask):
    """
    Calculates the mask used to set 0 values

    >>> get_zeroes_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")
    68719476733

    >>> f"{get_zeroes_mask('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X'):b}"
    '111111111111111111111111111111111101'

    :param mask:
    :return:
    """
    return int(mask.replace("X", "1"), 2)


def apply_mask(mask, value):
    """
    Apply the mask to the given value

    >>> f'{apply_mask("X1XX", "0000"):b}'
    '100'

    >>> f'{apply_mask("X1XX", "1111"):b}'
    '1111'

    >>> f'{apply_mask("X0XX", "1111"):b}'
    '1011'

    >>> f'{apply_mask("X0XX", "0000"):b}'
    '0'

    >>> f'{apply_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", "000000000000000000000000000000001011"):b}'
    '1001001'

    >>> apply_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", "000000000000000000000000000000001011")
    73

    >>> apply_mask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", 11)
    73

    :param mask:
    :param value:
    :return:
    """

    if isinstance(value, str):
        int_value = int(value, 2)
    else:
        int_value = value
    int_value |= get_ones_mask(mask)
    int_value &= get_zeroes_mask(mask)

    return int_value


def apply_insane_floating_mask(mask, value):
    """

    >>> apply_insane_floating_mask("00", 0)
    {0}

    >>> apply_insane_floating_mask("11", 0)
    {3}

    >>> apply_insane_floating_mask("XX", 0)
    {0, 1, 2, 3}

    >>> apply_insane_floating_mask("X1", 0)
    {1, 3}

    >>> apply_insane_floating_mask("000000000000000000000000000000X1001X", 42)
    {58, 59, 26, 27}

    :param mask:
    :param value:
    :return:
    """

    if isinstance(value, str):
        int_value = int(value, 2)
    else:
        int_value = value

    int_value |= get_ones_mask(mask)

    possible_values = {int_value, }
    for ix, v in enumerate(mask[::-1]):
        if v == "X":
            bit = ix
            values_0 = {v & ~(2**bit) for v in possible_values}
            values_1 = {v | (2**bit) for v in possible_values}
            possible_values |= values_0
            possible_values |= values_1

    return possible_values


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Day 14 of Advent of Code 2020')
    parser.add_argument('file', metavar='filename', type=argparse.FileType('rt'), nargs="?",
                        help='filename to your personal inputs', )
    parser.add_argument('--test', '-t', action='store_true')

    args = parser.parse_args()

    if args.test:
        import doctest
        doctest.testmod()
        print("Tests completed")
        exit(0)

    if args.file:
        with args.file as FILE:
            input_lines = FILE.readlines()

        memory = dict()
        mask=''
        for line in input_lines:
            if "mask" in line:
                mask = line.split("=")[1].strip()
            else:
                m = re.match(r"mem\[(\d+)\] = (\d+)", line)
                address = m.group(1)
                value = m.group(2)

                output_value = apply_mask(mask, int(value))
                memory[address] = output_value

        print(memory)
        print(sum(memory.values()))

        mask=''
        memory={}
        for line in input_lines:
            if "mask" in line:
                mask = line.split("=")[1].strip()
            else:
                m = re.match(r"mem\[(\d+)\] = (\d+)", line)
                address = int(m.group(1))
                value = int(m.group(2))

                addresses = apply_insane_floating_mask(mask, address)
                for a in addresses:
                    memory[a] = value

        print(memory)
        print(sum(memory.values()))
