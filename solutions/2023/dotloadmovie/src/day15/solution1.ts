import fs from 'fs';

export const computeFragmentHash = (fragment: string) => {
  let output = 0;
  const chars = fragment.split('');

  for (let i = 0; i < chars.length; i++) {
    output += fragment.charCodeAt(i);
    output *= 17;
    output = output % 256;
  }

  return output;
};

export const solution1 = () => {
  const input = fs
    .readFileSync(`${__dirname}/data/data.txt`, 'utf-8')
    .split(',');

  const values = input.map(computeFragmentHash);

  return values.reduce((prev: number, curr: number) => {
    return prev + curr;
  });
};
