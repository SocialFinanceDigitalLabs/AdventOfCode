# To code

- Install dependencies with `poetry install`;

## automatic
- store AoC cookie in an environment variable `AOC_COOKIE` - inspect the network requests and get the "session" cookie in one of the requests.
- run `python run.py start <DAY_TO_RUN>` where `<DAY_TO_RYN>` is the day you are starting with.
- Replace the code in the functions `part_1` and `part_2` with your solutions and make sure they return the solution (so it is printed to the console).


## manually
- Duplicate the directory `day_template` and rename it for your day with preceding 0 (so second day would be `02` and 21th day would be `21`);
- Fill the `test.txt` and `final.txt` with the challenge data;
- Replace the code in the functions `part_1` and `part_2` with your solutions and make sure they return the solution (so it is printed to the console).


# To run

```console
python run.py solve <DAY_TO_RUN> <PART_TO_RUN> <FILE_TO_RUN> --submit
```

## Examples
run the first day solution for part 1, with test data:

```console
python run.py solve 1 1 test.txt
```

run the third day solution for part 2, with final data:

```console
python run.py solve 3 2 final.txt
```

run the third day solution for part 2, with final data and submit it to AoC:

```console
python run.py solve 3 2 final.txt --submit
```