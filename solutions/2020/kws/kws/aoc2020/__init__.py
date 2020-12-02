import re


def split_input(input, type=str):
    """
    Takes a long, potentially multiline string as input and splits it, and optionally converts it to
    the specified type.

    Whitespace is always stripped from start and end of the line

    >>> split_input("a b c d e f ")
    ['a', 'b', 'c', 'd', 'e', 'f']

    >>> split_input('''
    ... a
    ... b
    ... c
    ... d
    ... e
    ... f
    ... ''')
    ['a', 'b', 'c', 'd', 'e', 'f']

    >>> split_input("1 2 3 4 5 6 1010 2020", type=int)
    [1, 2, 3, 4, 5, 6, 1010, 2020]

    :param input:
    :param type: try to coerce the type into this type
    :return:
    """

    input = input.strip()
    values = re.split(r"\s+", input, flags=re.M)
    values = [type(v) for v in values]
    return values


if __name__ == "__main__":
    import doctest
    doctest.testmod()
