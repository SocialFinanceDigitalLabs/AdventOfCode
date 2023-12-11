import fs from 'fs';

export const solution1 = () => {
  const input = fs.readFileSync(`${__dirname}/data/data.txt`, 'utf-8');

  const raw = input.split('\n\n');
  const steps = raw.shift()?.split('');

  const network: any = {};

  raw[0].split('\n').forEach((row: any) => {
    const portions = row.split(' = ');
    const directions = portions[1].match(/[^()]+(?=\))/g)[0].split(', ');
    network[portions[0].trim()] = { L: directions[0], R: directions[1] };
  });

  let count = 0;
  let step = 0;
  const traceNetwork = () => {
    let curr = 'AAA';

    while (curr !== 'ZZZ') {
      if (steps) {
        count = count + 1;
        curr = network[curr][steps[step]];

        step = step + 1 === steps.length ? 0 : step + 1;
      }
    }
  };

  traceNetwork();

  console.log(count);

  return count;
};
