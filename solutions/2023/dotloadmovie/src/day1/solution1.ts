import fs from 'fs';

export const solution1 = () => {
  const input = fs.readFileSync(`${__dirname}/data/data.txt`, 'utf-8');
  let output: any = [];

  const matcher = /\d+/g;

  const lines = input.split('\n');

  const raw = lines.map((line) => {
    const matches: any = line.match(matcher)?.join('').split('');

    const response: any = [];

    if (matches.length > 0) {
      response.push(Number(matches[0]));
    }

    if (matches.length > 0) {
      matches.reverse();
      response.push(Number(matches[0]));
    }

    return Number(response.join(''));
  });

  output = raw.reduce((prev, curr) => {
    return prev + curr;
  });

  return output;
};
