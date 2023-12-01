# Advent of code 2022

This repository contains my solutions to the [Advent of Code 2022](https://adventofcode.com/2022) challenges
by [Kaj](https://github.com/kws) as part of the 
[Social Finance](https://www.socialfinance.org.uk) Advent of Code team.

## Running the code

The code is written in Python 3.10 and uses [Poetry](https://python-poetry.org/) for dependency management.

To run the code, first install Poetry and then run:

```bash
poetry install
poetry shell
aoc22 day<day> 
```

where `<day>` is the day number, e.g.

```bash
aoc22 day01 
```

First time you run the code you will be prompted for a username. This username
corresponds to the subdirectory within inputs that contains your personalised inputs.

