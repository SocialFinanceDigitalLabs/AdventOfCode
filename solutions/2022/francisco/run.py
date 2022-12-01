import typer

def main(
    day: int,
    part: int = typer.Argument(1, help="part of the daily exercises (usually 1 or 2)"),
    file: str = typer.Argument(
        "test.txt",
        help="name of the .txt data file to use (usually test.txt or final.txt)",
    ),
):
    main_file = __import__(f"{str(day).zfill(2)}.main").main
    main_function = getattr(main_file, f"part_{part}")
    res = main_function(f"{file}")
    print(res)


if __name__ == "__main__":
    typer.run(main)
