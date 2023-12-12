import fs from 'fs';

export const solution1 = () => {
  const input = fs
    .readFileSync(`${__dirname}/data/data.txt`, 'utf-8')
    .split('\n');

  let output = 0;

  const lines = input.map((line: string) => {
    return line.split(' ').map((item: string) => {
      return parseInt(item);
    });
  });

  const getDifferences = (line: number[]): number[] => {
    const output = [];

    for (let i = 1; i < line.length; i++) {
      output.push(line[i] - line[i - 1]);
    }

    return output;
  };

  const getExtrapolation = (line: number[]): number => {
    const calc: any[] = [line];

    while (
      calc[calc.length - 1].some((num: number) => {
        return num !== 0;
      })
    ) {
      const next = getDifferences(calc[calc.length - 1]);
      calc.push(next);
    }

    calc.reverse();

    for (let i = 0; i < calc.length; i++) {
      if (i === 0) {
        calc[i].push(0);
      } else {
        calc[i].push(
          calc[i][calc[i].length - 1] + calc[i - 1][calc[i - 1].length - 1]
        );
      }
    }

    calc.reverse();

    return calc[0][calc[0].length - 1];
  };

  const values = lines.map((line: number[]) => {
    return getExtrapolation(line);
  });

  return values.reduce((prev: any, curr: any) => {
    return prev + curr;
  });
};
