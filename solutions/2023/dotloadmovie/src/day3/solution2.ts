import fs from 'fs';

export const solution2 = () => {
  const input = fs.readFileSync(`${__dirname}/data/data.txt`, 'utf-8');
  const lines = input.split('\n');
  const matcher = /[0-9]+/g;
  let positions: any = {};

  const writePosition = (row: number, i: number, num: number): void => {
    if (positions[`${row}-${i}`]) {
      positions[`${row}-${i}`].push(num);
    } else {
      positions[`${row}-${i}`] = [num];
    }
  };
  const findSurroundingGears = (
    start: number,
    finish: number,
    row: number,
    num: string
  ): void => {
    // row above
    if (row > 0) {
      const rowAbove = lines[row - 1].split('');
      for (let i = start - 1; i <= finish + 1; i++) {
        if (rowAbove[i] === '*') {
          writePosition(row - 1, i, Number(num));
        }
      }
    }

    //this row
    const rowThis = lines[row].split('');
    if (rowThis[start - 1] && rowThis[start - 1] === '*') {
      writePosition(row, start - 1, Number(num));
    }

    if (rowThis[finish + 1] && rowThis[finish + 1] !== '.') {
      writePosition(row, finish + 1, Number(num));
    }

    //row below
    if (row < lines.length - 2) {
      const rowBelow = lines[row + 1].split('');
      for (let i = start - 1; i <= finish + 1; i++) {
        if (rowBelow[i] === '*') {
          writePosition(row + 1, i, Number(num));
        }
      }
    }
  };

  lines.forEach((line, rowIdx) => {
    const matches = Array.from(line.matchAll(matcher));

    matches.forEach((match) => {
      findSurroundingGears(
        match.index as number,
        (match.index as number) + (match[0].length - 1),
        rowIdx,
        match[0]
      );
    });
  });

  const valid = Object.values(positions).map((position: any) => {
    return position.length > 1
      ? position.reduce((prev: any, curr: any) => {
          return prev * curr;
        })
      : 0;
  });

  return valid.reduce((prev: any, curr: any) => {
    return prev + curr;
  });
};
