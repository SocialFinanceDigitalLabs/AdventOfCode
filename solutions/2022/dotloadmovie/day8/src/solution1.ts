import fs from "fs";

export const solution1 = () => {
  const input = fs.readFileSync("./data/data.txt", "utf-8");

  const parseToGrid = (items: string) => {
    return items.split("\n").map((row: string) => {
      return row.split("").map((item: string) => {
        return parseInt(item);
      });
    });
  };

  const grid = parseToGrid(input);

  const getGridPosition = (x: number, y: number) => {
    if (!grid[y] || !grid[y][x]) {
      return null;
    }

    return grid[y][x];
  };

  const getIsVisible = (x: number, y: number) => {
    const element = grid[y][x];

    if (x === 0 || x === grid[y].length - 1) {
      return true;
    }

    if (y === 0 || y === grid.length - 1) {
      return true;
    }

    interface Values {
      above: number[];
      below: number[];
      left: number[];
      right: number[];
    }

    const blocking: Values = {
      above: [],
      left: [],
      below: [],
      right: [],
    };
    const count = 0;

    //trees to left
    for (let left = 0; left < x; left++) {
      blocking.left.push(grid[y][left]);
    }

    //trees to right
    for (let right = x + 1; right < grid[y].length; right++) {
      blocking.right.push(grid[y][right]);
    }

    //trees above
    for (let above = 0; above < y; above++) {
      blocking.above.push(grid[above][x]);
    }

    //trees below
    for (let below = y + 1; below < grid.length; below++) {
      blocking.below.push(grid[below][x]);
    }

    console.log(blocking, `--> ${element}, ${x}, ${y}`);

    const hiddenAbove =
      blocking.above.filter((tree) => {
        return tree >= element;
      }).length > 0;

    const hiddenBelow =
      blocking.below.filter((tree) => {
        return tree >= element;
      }).length > 0;

    const hiddenLeft =
      blocking.left.filter((tree) => {
        return tree >= element;
      }).length > 0;

    const hiddenRight =
      blocking.right.filter((tree) => {
        return tree >= element;
      }).length > 0;

    return !(hiddenAbove && hiddenBelow && hiddenLeft && hiddenRight);
  };

  const visible: string[] = [];
  const hidden: string[] = [];

  grid.forEach((row, y) => {
    row.forEach((cell, x) => {
      if (getIsVisible(x, y)) {
        visible.push(`${x}, ${y} -- ${grid[y][x]}`);
      } else {
        hidden.push(`${x}, ${y} -- ${grid[y][x]}`);
      }
    });
  });

  //  console.log(hidden);

  return visible.length;
};
