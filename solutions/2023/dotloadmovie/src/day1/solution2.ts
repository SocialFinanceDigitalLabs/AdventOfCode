import fs from 'fs';

export const solution2 = () => {
  const input = fs.readFileSync(`${__dirname}/data/data.txt`, 'utf-8');
  let output: any = [];
  const sample: any = [];

  const matcher = /\d|one|two|three|four|five|six|seven|eight|nine/g;

  const translation: any = [
    'zero',
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine',
  ];

  const lines = input.split('\n');

  const raw = lines.map((line) => {
    let matches = [];

    for (let i = 0; i < line.length; i++) {
      if (!isNaN(Number(line[i]))) {
        matches.push(line[i]);
      }

      const sub = line.substring(i);

      translation.forEach((num: string, idx: number) => {
        if (sub.indexOf(num) === 0) {
          matches.push(idx);
        }
      });
    }

    const response: any = [];

    response.push(Number(matches[0]));
    matches.reverse();
    response.push(Number(matches[0]));

    sample.push(response.join(','));

    return Number(response.join(''));
  });

  fs.writeFileSync(`${__dirname}/data/sample.txt`, sample.join('\n'));

  output = raw.reduce((prev, curr) => {
    return prev + curr;
  });

  return output;
};
