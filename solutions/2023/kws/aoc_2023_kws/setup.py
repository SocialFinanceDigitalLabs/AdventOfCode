from pathlib import Path

import click
from aoc_2023_kws.cli import main
from aoc_2023_kws.config import config
from aocd import get_data
from dateutil.utils import today


@main.command()
@click.argument("day", type=int, default=today().day)
def create(day):
    """Create a new day"""
    day = str(day).zfill(2)
    filename = Path(__file__).parent / f"day_{day}.py"
    if filename.exists():
        click.echo(f"Day {day} already exists")
    else:
        filename.write_text(
            f"""
import click
from aocd import submit

from aoc_2023_kws.cli import main
from aoc_2023_kws.config import config
             
                            
@main.command()
@click.option("--sample", "-s", is_flag=True)
def day{day}(sample):
    if sample:
        input_data = (config.SAMPLE_DIR / "day{day}.txt").read_text()
    else:
        input_data = (config.USER_DIR / "day{day}.txt").read_text()
        
    # submit(my_answer, part="a", day={day}, year=2023)
"""
        )

    sample_file = config.SAMPLE_DIR / f"day{day}.txt"
    if not sample_file.exists():
        sample_file.touch()

    data = get_data(day=int(day), year=2023)

    data_file = config.USER_DIR / f"day{day}.txt"
    if not data_file.exists():
        data_file.write_text(data)
