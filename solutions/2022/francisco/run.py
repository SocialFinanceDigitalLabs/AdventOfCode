import typer
from util import new_day, submit_answer

app = typer.Typer()


@app.command()
def solve(
    day: int,
    part: int = typer.Argument(1, help="part of the daily exercises (usually 1 or 2)"),
    file: str = typer.Argument(
        "test.txt",
        help="name of the .txt data file to use (usually test.txt or final.txt)",
    ),
    submit: bool = typer.Option(False, "--submit"),
):
    main_file = __import__(f"{str(day).zfill(2)}.main").main
    main_function = getattr(main_file, f"part_{part}")
    answer = main_function(f"{file}")
    print(answer)

    if submit:
        submit_answer(day, answer, part)


@app.command()
def start(day: int):
    new_day(day)


if __name__ == "__main__":
    app()
