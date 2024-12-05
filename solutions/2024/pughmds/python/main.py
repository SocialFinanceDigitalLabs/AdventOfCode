import click
import importlib
from input_processing.parse_file import open_file
from input_processing.run import create_result

import json
import glob
import re


@click.command()
@click.option("--day", default=1, help="Which Day To Run")
@click.option("--test", is_flag=True, default=False, help="Add flag for test run")
@click.option("--part1", is_flag=True, default=False, help="Only Run Part 1")
@click.option("--part2", is_flag=True, default=False, help="Only Run Part 2")
def run(day, test, part1, part2):
    day = f"day{day:02}"
    module = importlib.import_module(f"{day}.main")

    if test:
        input_file_locations = glob.glob(f"./sample_data/{day}_*test*.txt")
    else:
        input_file_locations = [f"./sample_data/{day}.txt"]

    results = []
    for file in input_file_locations:
        input_file_data = open_file(file)
        if test:
            testnum = int(re.findall(r"\d+", file)[-1]) - 1
        else:
            testnum = 0

        if part1:
            try:
                res = create_result(1, module.EXPECTED_TEST_ANSWER_PART1[testnum])
            except Exception as err:
                print(module.EXPECTED_TEST_ANSWER_PART1)
                return
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

        if test:
            res["file"] = file
    print(f"day {day} results:")
    print(json.dumps(results,sort_keys=True, indent=4))


if __name__ == "__main__":
    run()
