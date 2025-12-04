
from collections import Counter
import click
from aocd import submit

from aoc_2024_kws.cli import main
from aoc_2024_kws.config import config
             
                            
@main.command()
@click.option("--sample", "-s", is_flag=True)
def day01(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day01.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day01.txt").read_text()
        
    data = input_data.splitlines()
    data = [tuple(map(int, line.split())) for line in data]

    list_a = [x[0] for x in data]
    list_b = [x[1] for x in data]

    list_a.sort()
    list_b.sort()

    pairwise = zip(list_a, list_b)

    differences = [abs(b - a) for a, b in pairwise]


    print(sum(differences))
    # submit(my_answer, part="a", day=01, year=2024)

    frequencies = Counter(list_b)

    similarity_score = 0
    for a in list_a:
        similarity_score += frequencies.get(a, 0) * a

    print(similarity_score)
    # submit(my_answer, part="b", day=01, year=2024)