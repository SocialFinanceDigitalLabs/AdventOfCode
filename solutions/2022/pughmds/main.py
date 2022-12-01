import click
import importlib
from shared.file import open_into_list
from shared.output import show_results, show_test_results
from shared.test import run_tests


@click.command()
@click.option("--day", default=1, help="Which Day To Run")
@click.option("--test", is_flag=True, default=False, help="Add flag for test run")
@click.option("--part1", is_flag=True, default=False, help="Only Run Part 1")
@click.option("--part2", is_flag=True, default=False, help="Only Run Part 2")
def run(day, test, part1, part2):
    day = f"day{day:02}"
    module = importlib.import_module(f"{day}.__main__")

    if test:
        input_file_location = f"{day}/test.txt"
    else:
        input_file_location = f"{day}/input.txt"

    input_file = open_into_list(input_file_location)

    if part1:
        results = [
            {
                "Part": "Part 1",
                "Value": module.run(input_file),
                "Expected": module.EXPECTED_TEST_ANSWER_PART1,
            }
        ]
    elif part2:
        results = [
            {
                "Part": "Part 2",
                "Value": module.run_p2(input_file),
                "Expected": module.EXPECTED_TEST_ANSWER_PART2,
            }
        ]
    else:
        results = [
            {
                "Part": "Part 1",
                "Value": module.run(input_file),
                "Expected": module.EXPECTED_TEST_ANSWER_PART1,
            },
            {
                "Part": "Part 2",
                "Value": module.run_p2(input_file),
                "Expected": module.EXPECTED_TEST_ANSWER_PART2,
            },
        ]

    show_results(results, day)

    if test:
        run_tests(results)


if __name__ == "__main__":
    run()
