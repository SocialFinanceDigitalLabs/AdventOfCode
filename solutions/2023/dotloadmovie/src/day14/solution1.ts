import fs from 'fs';

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
  const input = fs
    .readFileSync(`${__dirname}/data/data.txt`, 'utf-8')
    .split('\n');

  let output = 0;

  let grid = input.map((val: any) => {
    return val.split('');
  });

  grid = rotateArray(grid);

  const tiltRow = (row: string[]) => {
    const raw = row.join('').split('#');

    const output = raw.map((fragment: any) => {
      return fragment.split('').sort().reverse().join('');
    });

    return output.join('#').split('');
  };

  const tiltedValues = grid.map((row: any) => {
    const tilted = tiltRow(row);

    return tilted.reduce((prev: any, curr: any, i) => {
      const val = curr === 'O' ? 1 * (row.length - i) : 0;
      const output = prev + val;

      return output;
    }, 0);
  });

  output = tiltedValues.reduce((prev: number, curr: number) => {
    return prev + curr;
  });

  return output;
};
