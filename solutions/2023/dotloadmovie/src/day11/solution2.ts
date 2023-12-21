import fs from 'fs';

type Pos = {
  x: number;
  y: number;
};

export const solution2 = () => {
  const expansionFactor = 999999;

  const readArrayCol = (colIdx: number, target: any): any[] => {
    const output: any = [];

    for (let i = 0; i < target.length; i++) {
      //data is always square...
      output.push(target[i][colIdx]);
    }

    return output;
  };

  const getManhattan = (start: Pos, end: Pos, offsets: Pos): number => {
    const xPoints = [start.x, end.x].sort();
    const yPoints = [start.y, end.y].sort();

    const x = Math.abs(xPoints[0] - xPoints[1]);
    const y = Math.abs(yPoints[0] - yPoints[1]);

    return x + y;
  };

  const getOffset = (pos: Pos): Pos => {
    const output: Pos = { x: 0, y: 0 };

    output.x =
      emptyCols.filter((num: number) => {
        return num < pos.x;
      }).length * expansionFactor;

    output.y =
      emptyRows.filter((num: number) => {
        return num < pos.y;
      }).length * expansionFactor;

    return output;
  };

  let output = 0;
  const emptyCols: number[] = [];
  const emptyRows: number[] = [];

  const input = fs
    .readFileSync(`${__dirname}/data/data.txt`, 'utf-8')
    .split('\n');

  const points: Pos[] = [];

  const universe = input.map((row: any) => {
    return row.split('');
  });

  universe.forEach((row: string[], i: number, arr: string[][]) => {
    if (i === 0) {
      row.forEach((col: string, j: number) => {
        const arrCol = readArrayCol(j, arr);

        if (arrCol.indexOf('#') < 0) {
          emptyCols.push(j);
        }
      });
    }

    let index = row.indexOf('#');
    if (index < 0) {
      emptyRows.push(i);
    }

    while (index > -1) {
      const offset = getOffset({ x: index, y: i });
      points.push({ x: index + offset.x, y: i + offset.y });
      index = row.indexOf('#', index + 1);
    }
  });

  points.forEach((point: Pos, idx: number) => {
    for (let i = idx + 1; i < points.length; i++) {
      const diff = getManhattan(point, points[i], { x: 0, y: 0 });
      output += diff;
    }
  });

  return output;
};
