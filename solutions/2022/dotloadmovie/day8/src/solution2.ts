import fs from "fs";

export const solution2 = () => {
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
    if (grid[y] === undefined || grid[y][x] === undefined) {
      return -1;
    }

    return grid[y][x];
  };

  const getViewingDistances = (x: number, y: number) => {
    const element = grid[y][x];

    if (x === 0 || x === grid[y].length - 1) {
      return { total: 0 };
    }

    if (y === 0 || y === grid.length - 1) {
      return { total: 0 };
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

    //trees to left
    let stopLeft = false;
    for (let left = x - 1; left > -1; left--) {
      const item = getGridPosition(left, y);

      if (item !== -1 && !stopLeft) {
        blocking.left.push(item);

        if (item >= element) {
          stopLeft = true;
        }
      }
    }

    //trees to right
    let stopRight = false;
    for (let right = x + 1; right < grid[y].length + 1; right++) {
      const item = getGridPosition(right, y);
      if (item !== -1 && !stopRight) {
        blocking.right.push(item);

        if (item >= element) {
          stopRight = true;
        }
      }
    }

    //trees above
    let stopAbove = false;
    for (let above = y - 1; above > -1; above--) {
      const item = getGridPosition(x, above);

      if (item !== -1 && !stopAbove) {
        blocking.above.push(item);

        if (item >= element) {
          stopAbove = true;
        }
      }
    }

    //trees below
    let stopBelow = false;
    for (let below = y + 1; below < grid.length + 1; below++) {
      const item = getGridPosition(x, below);
      if (item !== -1 && !stopBelow) {
        blocking.below.push(item);

        if (item >= element) {
          stopBelow = true;
        }
      }
    }

    const values: number[] = [];

    Object.values(blocking).forEach((val) => {
      if (val.length > 0) {
        values.push(val.length);
      }
    });

    if (x === 15 && y === 52) {
      console.log(blocking, values, x, y);
    }

    const count = values.reduce((acc: number, curr: number) => {
      return acc * curr;
    });

    return { total: count, position: `${x},${y}` };
  };

  const outputs: any[] = [];

  grid.forEach((row, y) => {
    row.forEach((cell, x) => {
      outputs.push(getViewingDistances(x, y));
    });
  });

  //  console.log(getViewingDistances(15, 52));

  const response = outputs.sort((a: any, b: any) => {
    return b.total - a.total;
  })[0];

  console.log(response);

  return response.total;
};
