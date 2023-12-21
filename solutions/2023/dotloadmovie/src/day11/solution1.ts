import fs from 'fs';

type Pos = {
  x: number;
  y: number;
};

const rotateArray = (arr: any): any => {
  //assumes all arrays are the same length
  const output: any = {};

  arr.forEach((row: any) => {
    row.forEach((digit: any, i: any) => {
      if (!output[i]) {
        output[i] = [];
      }

      output[i].push(digit);
    });
  });

  return Object.values(output);
};

export const solution1 = () => {
  const expandRows = (grid: any): any => {
    const indices: number[] = [];
    const space = new Array(grid[0].length).fill('.').join('');

    grid.forEach((row: any, i: number) => {
      if (row.indexOf('#') < 0) {
        indices.push(i);
      }
    });

    indices.forEach((index: any, count: number) => {
      grid.splice(index + count, 0, space);
    });

    return grid;
  };

  const expandCols = (grid: any) => {
    const indices: number[] = [];

    const rotated = rotateArray(grid);
    const space = new Array(rotated[0].length).fill('.');

    rotated.forEach((row: any, i: number) => {
      if (row.indexOf('#') < 0) {
        indices.push(i);
      }
    });

    indices.forEach((index: any, count: number) => {
      rotated.splice(index + count, 0, space);
    });

    return rotateArray(rotated);
  };

  const getManhattan = (start: Pos, end: Pos): number => {
    //const output = start.x - end.x + (start.y - end.y);

    const x = Math.abs(start.x - end.x);
    const y = Math.abs(start.y - end.y);

    //return output >= 0 ? output : Math.abs(output);
    return x + y;
  };

  const input = fs
    .readFileSync(`${__dirname}/data/data.txt`, 'utf-8')
    .split('\n');

  const points: Pos[] = [];

  const universe = expandCols(
    expandRows(input).map((row: any) => {
      return row.split('');
    })
  );

  let count = 0;

  universe.forEach((row: any, y: number) => {
    row.forEach((cell: string, x: number) => {
      if (cell === '#') {
        universe[y][x] = count;
        count += 1;
        points.push({ x, y });
      }
    });
  });

  let output = 0;

  points.forEach((point: Pos, idx: number) => {
    for (let i = idx + 1; i < points.length; i++) {
      output += getManhattan(point, points[i]);
    }
  });

  return output;
};
