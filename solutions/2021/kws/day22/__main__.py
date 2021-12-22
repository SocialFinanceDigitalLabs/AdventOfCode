# Advent of Code 2021 Day 22
from common import standard_setup
import day22
from day22 import database


def main(*argv):
    lines = standard_setup(*argv)

    with database.Database.open() as db:
        for line in lines:
            xr, yr, zr, value = day22.parse_input(line)
            xr = day22.limit(*xr, -50, 50)
            yr = day22.limit(*yr, -50, 50)
            zr = day22.limit(*zr, -50, 50)
            if xr is None or yr is None or zr is None:
                continue
            db.set_many(xr, yr, zr, value)
        print(db.count_values(1))

    print("   ")

    with database.Database.open() as db:
        for line in lines:
            xr, yr, zr, value = day22.parse_input(line)
            db.set_many(xr, yr, zr, value)
        print(db.count_values(1))


if __name__ == "__main__":
    main()

