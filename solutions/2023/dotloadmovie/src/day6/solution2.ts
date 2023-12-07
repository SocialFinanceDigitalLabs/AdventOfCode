import fs from 'fs';

export const solution2 = () => {
  const input = fs.readFileSync(`${__dirname}/data/data.txt`, 'utf-8');
  const raw = input.split('\n');

  const times: any = Number(raw[0].split(':')[1].trim().replaceAll(' ', ''));

  const distances: any = Number(
    raw[1].split(':')[1].trim().replaceAll(' ', '')
  );

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

  const output = calculateValues(times, distances).length;

  return output;
};
