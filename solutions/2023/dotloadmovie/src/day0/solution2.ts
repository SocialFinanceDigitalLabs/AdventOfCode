import fs from 'fs';

export const solution2 = () => {
  const input = fs.readFileSync(`${__dirname}/data/data.txt`, 'utf-8');
  return input;
};
