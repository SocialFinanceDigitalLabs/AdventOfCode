import fs from 'fs';

export const solution1 = () => {
  const input = fs.readFileSync(`${__dirname}/data/data.txt`, 'utf-8');
  const raw = input.split('\n');

  const times: any = raw[0]
    .split(':')[1]
    .trim()
    .split(/\s+/)
    .map((time) => {
      return Number(time);
    });

  const distances: any = raw[1]
    .split(':')[1]
    .trim()
    .split(/\s+/)
    .map((distance) => {
      return Number(distance);
    });

  const calculateValues = (time: any, distance: any) => {
    const output = [];

    for (let i = 1; i < time; i++) {
      const potential = i * (time - i);
      if (potential > distance) {
        output.push(i);
      }
    }

    return output;
  };

  const output = times.map((time: any, idx: any) => {
    return calculateValues(time, distances[idx]).length;
  });

  return output.reduce((prev: any, curr: any) => {
    return prev * curr;
  });
};
