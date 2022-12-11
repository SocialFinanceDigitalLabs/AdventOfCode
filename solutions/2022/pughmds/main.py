import click
import importlib
from shared.file import open_into_list
from shared.output import show_results, show_test_results
from shared.test import display_test_results
from shared.exec import create_result
import glob
import re

@click.command()
@click.option("--day", default=1, help="Which Day To Run")
@click.option("--test", is_flag=True, default=False, help="Add flag for test run")
@click.option("--part1", is_flag=True, default=False, help="Only Run Part 1")
@click.option("--part2", is_flag=True, default=False, help="Only Run Part 2")
def run(day, test, part1, part2):
    day = f"day{day:02}"
    module = importlib.import_module(f"{day}.__main__")

    if test:
        input_file_locations = glob.glob(f"{day}/test*.txt")
    else:
        input_file_locations = [f"{day}/input.txt"]

    results = []
    for file in input_file_locations:
        input_file_data = open_into_list(file)
        if test:
            testnum = int(re.findall(r'\d+', file)[-1]) - 1
        else:
            testnum = 0

        if part1:
            res = create_result(1, module.EXPECTED_TEST_ANSWER_PART1[testnum])
            res["Value"] = module.run(input_file_data)
            results.append(res)
        elif part2:
            res = create_result(2, module.EXPECTED_TEST_ANSWER_PART2[testnum])
            res["Value"] = module.run_p2(input_file_data)
            results.append(res)
        else:
            res = create_result(1, module.EXPECTED_TEST_ANSWER_PART1[testnum])
            res["Value"] = module.run(input_file_data)
            results.append(res)
            res = create_result(2, module.EXPECTED_TEST_ANSWER_PART2[testnum])
            res["Value"] = module.run_p2(input_file_data)
            results.append(res)

    show_results(results, day)

    if test:
        display_test_results(results)


if __name__ == "__main__":
    run()
