import fs from 'fs';

export const solution2 = () => {
  const input = fs
    .readFileSync(`${__dirname}/data/data.txt`, 'utf-8')
    .split('\n');

  const grid = input.map((row) => {
    return row.split('');
  });
  let output = 0;

  const readArrayCol = (colIdx: number, target: any): any[] => {
    const output: any = [];

    for (let i = 0; i < target.length; i++) {
      //data is always square...
      output.push(target[i][colIdx]);
    }

    return output;
  };

  const writeArrayCol = (
    colIdx: number,
    contents: string[],
    target: any
  ): void => {
    for (let i = 0; i < target.length; i++) {
      //data is always square...
      target[i][colIdx] = contents[i];
    }
  };

  const tiltRow = (row: any[], invert: boolean = false): any[] => {
    const raw = row.join('').split('#');

    const output = raw.map((fragment: any) => {
      if (invert) {
        return fragment.split('').sort().join('');
      }

      return fragment.split('').sort().reverse().join('');
    });

    return output.join('#').split('');
  };

  const tiltTableVert = (target: any, south: boolean = false) => {
    for (let i = 0; i < target.length; i++) {
      const sortedRow = tiltRow(readArrayCol(i, target), south);
      writeArrayCol(i, sortedRow, target);
    }

    return target.slice();
  };

  const tiltTableHoriz = (target: any, east: boolean = false) => {
    for (let i = 0; i < target.length; i++) {
      target[i] = tiltRow(target[i], east);
    }

    return target.slice();
  };

  const rotateTable = (target: any): any => {
    let output = target.slice();

    output = tiltTableVert(output);
    output = tiltTableHoriz(output);
    output = tiltTableVert(output, true);
    output = tiltTableHoriz(output, true);

    return output;
  };

  const calculateLoad = (calcGrid: any): number => {
    const cols = [];

    for (let i = 0; i < calcGrid.length; i++) {
      cols.push(readArrayCol(i, calcGrid));
    }

    const tiltedValues = cols.map((col: any) => {
      return col.reduce((prev: any, curr: any, i: number) => {
        const val = curr === 'O' ? 1 * (col.length - i) : 0;
        const output = prev + val;

        return output;
      }, 0);
    });

    output = tiltedValues.reduce((prev: number, curr: number) => {
      return prev + curr;
    });

    return output;
  };

  let matches: any = [];
  let temp = grid.slice();

  for (let i = 0; i < 1000; i++) {
    temp = rotateTable(temp);

    const val = JSON.stringify(temp.slice());

    if (matches.indexOf(val) > -1) {
      matches.push(val);
      break;
    } else {
      matches.push(val);
    }
  }

  return calculateLoad(
    JSON.parse(
      matches[
        matches.length -
          Math.cbrt(matches.length - (1000000000 % matches.length))
      ]
    )
  );
};
