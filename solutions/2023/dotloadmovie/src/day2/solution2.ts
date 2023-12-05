import fs from 'fs';

export const solution2 = () => {
  const input = fs.readFileSync(`${__dirname}/data/data.txt`, 'utf-8');

  const games = input.split('\n');

  const matches: any = [];

  const hand = {
    red: 12,
    green: 13,
    blue: 14,
  };

  games.forEach((game, idx) => {
    const draw = game.split(': ')[1].split(';');
    const result: any = {
      red: 0,
      green: 0,
      blue: 0,
    };

    draw.forEach((turn) => {
      turn.split(',').forEach((color) => {
        const match = color.trim().split(' ');

        if (result[match[1]] < Number(match[0])) {
          result[match[1]] = Number(match[0]);
        }
      });
    });

    matches.push(result.red * result.blue * result.green);
  });

  return matches.reduce((prev: number, curr: number) => {
    return prev + curr;
  });
};
