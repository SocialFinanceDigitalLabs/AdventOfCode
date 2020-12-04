#! /usr/bin/env python
import argparse
import re


def parse_record(record):
    fields = re.split(r"\s+", record, flags=re.M)
    r = {f.split(":", 1)[0].strip(): f.split(":", 1)[1].strip() for f in fields if ":" in f}
    return r


def parse_content(file_content):
    """
    Parses the input file by separating records, and then turning each record into a dict

    >>> parse_content("a:1 b:2\\nc:3 \\n\\n a:11 b:22")
    [{'a': '1', 'b': '2', 'c': '3'}, {'a': '11', 'b': '22'}]

    :param file_content:
    :return:
    """
    records = re.split(r"\n\n", file_content, flags=re.M)
    parsed = [parse_record(r) for r in records]

    return parsed


def is_valid(record):
    if len(record) == 7:
        return "cid" not in record

    return len(record) == 8


def is_four_digits(value, min, max):
    return len(value) == 4 and min <= int(value) <= max


def is_valid_part_2(record):
    """
    >>> is_valid_part_2(parse_record("eyr:1972 cid:100 hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926"))
    False
    >>> is_valid_part_2(parse_record("iyr:2019 hcl:#602927 eyr:1967 hgt:170cm ecl:grn pid:012533040 byr:1946"))
    False
    >>> is_valid_part_2(parse_record("hcl:dab227 iyr:2012 ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277"))
    False
    >>> is_valid_part_2(parse_record("hgt:59cm ecl:zzz eyr:2038 hcl:74454a iyr:2023 pid:3556412378 byr:2007"))
    False
    >>> is_valid_part_2(parse_record("pid:087499704 hgt:74in ecl:gun iyr:2012 eyr:2030 byr:1980 hcl:#623a2f"))
    False
    >>> is_valid_part_2(parse_record("pid:87499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2f"))
    False
    >>> is_valid_part_2(parse_record("pid:8749a9704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2f"))
    False
    >>> is_valid_part_2(parse_record("pid:8749a9704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2f"))
    False
    >>> is_valid_part_2(parse_record("pid:087499704 hgt:74in ecl:grn iyr:02012 eyr:2030 byr:1980 hcl:#623a2f"))
    False
    >>> is_valid_part_2(parse_record("pid:087499704 hgt:74in ecl:grn iyr:2009 eyr:2030 byr:1980 hcl:#623a2f"))
    False
    >>> is_valid_part_2(parse_record("pid:087499704 hgt:74in ecl:grn iyr:2021 eyr:2030 byr:1980 hcl:#623a2f"))
    False
    >>> is_valid_part_2(parse_record("pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623g2f"))
    False
    >>> is_valid_part_2(parse_record("pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2fe"))
    False
    >>> is_valid_part_2(parse_record("pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2"))
    False
    >>> is_valid_part_2(parse_record("pid:087499704 hgt:74in ecl:grne iyr:2012 eyr:2030 byr:1980 hcl:#623a2f"))
    False
    >>> is_valid_part_2(parse_record("pid:0087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2f"))
    False

    >>> is_valid_part_2(parse_record("pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2f"))
    True
    >>> is_valid_part_2(parse_record("pid:087499704 hgt:74in ecl:grn iyr:2010 eyr:2030 byr:1980 hcl:#623a2f"))
    True
    >>> is_valid_part_2(parse_record("pid:087499704 hgt:74in ecl:grn iyr:2020 eyr:2030 byr:1980 hcl:#623a2f"))
    True
    >>> is_valid_part_2(parse_record("eyr:2029 ecl:blu cid:129 byr:1989 iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm"))
    True
    >>> is_valid_part_2(parse_record("hcl:#888785 hgt:164cm byr:2001 iyr:2015 cid:88 pid:545766238 ecl:hzl eyr:2022"))
    True
    >>> is_valid_part_2(parse_record("iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"))
    True


    :param record:
    :return:
    """

    try:
        valid = is_valid(record)
        valid &= is_four_digits(record['byr'], 1920, 2002)
        valid &= is_four_digits(record['iyr'], 2010, 2020)
        valid &= is_four_digits(record['eyr'], 2020, 2030)

        height = re.match(r"(\d+)(in|cm)", record['hgt'])
        if height.group(2) == "in":
            valid &= 59 <= int(height.group(1)) <= 76
        else:
            valid &= 150 <= int(height.group(1)) <= 193

        hcl = re.match(r"^#[0-9a-f]{6}$", record['hcl'])
        valid &= hcl is not None

        valid &= record['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

        pid = re.match(r"^\d{9}$", record['pid'])
        valid &= pid is not None


    except:
        return False

    return valid


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Day 3 of Advent of Code 2020')
    parser.add_argument('file', metavar='filename', type=argparse.FileType('rt'),
                        help='filename to your personal inputs')
    parser.add_argument('--test', '-t', action='store_true')

    args = parser.parse_args()

    if args.test:
        import doctest

        doctest.testmod()

        print("Tests completed")
        exit(0)

    with args.file as FILE:
        file_content = FILE.read()

    file_data = parse_content(file_content)

    print(f"There are {len(file_data)} records in the input")

    valid = [record for record in file_data if is_valid(record)]
    invalid = [record for record in file_data if is_valid(record)]
    print(f"There are {len(valid)}/{len(invalid)} valid passport records in PART 1")

    valid_pt2 = [record for record in file_data if is_valid_part_2(record)]
    print(f"There are {len(valid_pt2)} valid passport records in PART 2")
