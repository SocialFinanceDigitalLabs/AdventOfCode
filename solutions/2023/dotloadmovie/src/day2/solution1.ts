import fs from 'fs';

export const solution1 = () => {
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

    const result = draw.filter((turn) => {
      const colors: any = { red: 0, blue: 0, green: 0 };

      turn.split(',').forEach((color) => {
        const match = color.trim().split(' ');
        colors[match[1]] = Number(match[0]);
      });

      return (
        hand.red >= colors.red &&
        hand.blue >= colors.blue &&
        hand.green >= colors.green
      );
    });

    if (result.length === draw.length) {
      matches.push(idx + 1);
    }
  });

  return matches.reduce((prev: number, curr: number) => {
    return prev + curr;
  });
};
