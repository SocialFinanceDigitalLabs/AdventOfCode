import click
from aocd import submit
import re

from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config
             
                            
@main.command()
@click.option("--sample", "-s", is_flag=True)
def day03(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day03.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day03.txt").read_text()
        
    exp = re.compile(r"mul\((\d{1,3},\d{1,3})\)")

    matches = exp.findall(input_data)
    pairs = [tuple(int(x) for x in match.split(",")) for match in matches]
    products = [a * b for a, b in pairs]
    product_sum = sum(products)

    print(product_sum)
    # submit(product_sum, part="a", day=3, year=2024)

    if sample:
        input_data = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

    exp = re.compile(r"mul\((\d{1,3},\d{1,3})\)|(do\(\))|(don't\(\))")
    matches = exp.findall(input_data)

    enabled = True

    pairs = []
    for match in matches:
        if match[2]:
            enabled = False
        elif match[1]:
            enabled = True
        elif match[0]:
            if enabled:
                pairs.append(tuple(int(x) for x in match[0].split(",")))

    products = [a * b for a, b in pairs]
    product_sum = sum(products)

    print(product_sum)
    # submit(product_sum, part="b", day=3, year=2024)
