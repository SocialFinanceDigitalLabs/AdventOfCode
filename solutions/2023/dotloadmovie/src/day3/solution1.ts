import fs from 'fs';

export const solution1 = () => {
  const input = fs.readFileSync(`${__dirname}/data/data.txt`, 'utf-8');
  const lines = input.split('\n');
  const matcher = /[0-9]+/g;

  const getSurroundingXY = (
    start: number,
    finish: number,
    row: number
  ): any[] => {
    const output: any = [];

    // row above
    if (row > 0) {
      const rowAbove = lines[row - 1].split('');
      for (let i = start - 1; i <= finish + 1; i++) {
        if (rowAbove[i] !== '.' && !matcher.test(rowAbove[i])) {
          output.push(rowAbove[i]);
        }
      }
    }

    //this row
    const rowThis = lines[row].split('');
    if (rowThis[start - 1] && rowThis[start - 1] !== '.') {
      output.push(rowThis[start - 1]);
    }

    if (rowThis[finish + 1] && rowThis[finish + 1] !== '.') {
      output.push(rowThis[start + 1]);
    }

    //row below
    if (row < lines.length - 2) {
      const rowBelow = lines[row + 1].split('');
      for (let i = start - 1; i <= finish + 1; i++) {
        if (rowBelow[i] !== '.' && !matcher.test(rowBelow[i])) {
          output.push(rowBelow[i]);
        }
      }
    }

    return output.join('');
  };

  let totals: any = [];

  lines.forEach((line, rowIdx) => {
    const matches = Array.from(line.matchAll(matcher));

    const coords = matches.map((match) => {
      const result = getSurroundingXY(
        match.index as number,
        (match.index as number) + (match[0].length - 1),
        rowIdx
      );

      return result.length > 0 ? Number(match) : 0;
    });

    totals = totals.concat(coords);
  });

  return totals.reduce((prev: any, curr: any) => {
    return prev + curr;
  });
};
