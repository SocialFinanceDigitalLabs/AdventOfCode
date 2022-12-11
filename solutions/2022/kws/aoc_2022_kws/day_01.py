from aoc_2022_kws.cli import main
from aoc_2022_kws.config import config


@main.command()
def day01():
    input_data = (config.USER_DIR / "day01-pt1.txt").read_text()
    contents = {ix: lines for ix, lines in enumerate(input_data.split("\n\n"))}
    totals = {
        ix: sum(int(line) for line in lines.split("\n"))
        for ix, lines in contents.items()
    }
    max_value = max(totals.values())
    print(f"Part 1: {max_value}")

    ordered_elves = [(ix, value) for ix, value in totals.items()]
    ordered_elves.sort(key=lambda x: x[1], reverse=True)
    top_three = sum([v[1] for v in ordered_elves[:3]])
    print(f"Part 2: {top_three}")


if __name__ == "__main__":
    day01()
