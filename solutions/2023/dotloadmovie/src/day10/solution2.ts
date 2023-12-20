import fs from 'fs';

type Position = {
  x: number;
  y: number;
};

type GridElement = {
  exits: Position[] | null;
  self: Position;
  char: string;
} | null;

interface List {
  [key: string]: GridElement;
}

export const solution2 = () => {
  const getPoints = (symbol: string, position: Position): Position[] | null => {
    let output = null;

    if (symbol === 'F') {
      output = [
        { x: position.x + 1, y: position.y },
        { x: position.x, y: position.y + 1 },
      ];
    }

    if (symbol === '|') {
      output = [
        { x: position.x, y: position.y + 1 },
        { x: position.x, y: position.y - 1 },
      ];
    }

    if (symbol === '-') {
      output = [
        { x: position.x + 1, y: position.y },
        { x: position.x - 1, y: position.y },
      ];
    }

    if (symbol === 'L') {
      output = [
        { x: position.x, y: position.y - 1 },
        { x: position.x + 1, y: position.y },
      ];
    }

    if (symbol === '7') {
      output = [
        { x: position.x - 1, y: position.y },
        { x: position.x, y: position.y + 1 },
      ];
    }

    if (symbol === 'J') {
      output = [
        { x: position.x, y: position.y - 1 },
        { x: position.x - 1, y: position.y },
      ];
    }

    return output;
  };

  const input = fs
    .readFileSync(`${__dirname}/data/data.txt`, 'utf-8')
    .split('\n');

  const start: Position = { x: 0, y: 0 };
  const firstStep: Position = { x: 31, y: 25 };

  const list: List = {};

  const grid = input.map((row: string, rowi: number) => {
    const output = row.split('');

    output.forEach((char: string, coli: number) => {
      if (char === 'S') {
        start.x = coli;
        start.y = rowi;
      }
    });

    return output;
  });

  const buildList = (): any => {
    let currPositions: any = { lastPos: start, thisPos: firstStep };
    let currChar = '';

    const step = (lastPos: Position, thisPos: Position): any => {
      const char = grid[thisPos.y][thisPos.x];
      const exits = getPoints(char, thisPos);

      currChar = char;

      list[`${thisPos.x}-${thisPos.y}`] = {
        exits,
        self: thisPos,
        char,
      };

      currPositions.thisPos = exits?.filter((pos: Position) => {
        if (pos.x === lastPos.x && pos.y === lastPos.y) {
          return false;
        }

        return true;
      })[0] || { x: -1, y: -1 };

      currPositions.lastPos = { ...thisPos };
    };

    while (currChar !== 'S') {
      step(currPositions.lastPos, currPositions.thisPos);
    }
  };

  const plotList = () => {
    grid.forEach((row: any, i: number) => {
      row.forEach((col: any, j: number) => {
        grid[i][j] = '';
      });
    });

    Object.values(list).forEach((el: GridElement) => {
      const mapped = grid[el?.self.y as number][el?.self.x as number];

      grid[el?.self.y as number][el?.self.x as number] = el?.char || '';
    });
  };

  const getClassName = (char: string) => {
    if (char === '-') {
      return 'cell-horiz';
    }

    if (char === '|') {
      return 'cell-vert';
    }

    if (char === '') {
      return 'cell-none';
    }

    return 'cell-' + char;
  };

  const exportGrid = () => {
    const output: any = grid.map((row: any) => {
      const rowOutput = row.map((col: any) => {
        return `<td class="${getClassName(col)}"><span>${col}</span></td>`;
      });

      return `<tr>${rowOutput.join('')}</tr>`;
    });

    const toRender = `<html><head><link rel="stylesheet" href="./styles.css" /></head><body><table><tbody>${output.join(
      ''
    )}</tbody></table><script src="./script.js"></script></body></html>`;

    fs.writeFileSync(`${__dirname}/html/table.html`, toRender);
  };

  buildList();

  plotList();

  exportGrid();

  const output = 10;

  return output;
};
