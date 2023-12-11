import fs from 'fs';

export const solution2 = () => {
  const input = fs.readFileSync(`${__dirname}/data/data.txt`, 'utf-8');

  const raw = input.split('\n\n');
  const steps = raw.shift()?.split('');

  const network: any = {};

  const gcd = (a: any, b: any) => {
    for (let temp = b; b !== 0; ) {
      b = a % b;
      a = temp;
      temp = b;
    }
    return a;
  };

  const lcm = (a: any, b: any) => {
    const gcdValue = gcd(a, b);
    return (a * b) / gcdValue;
  };

  raw[0].split('\n').forEach((row: any) => {
    const portions = row.split(' = ');
    const directions = portions[1].match(/[^()]+(?=\))/g)[0].split(', ');
    network[portions[0].trim()] = { L: directions[0], R: directions[1] };
  });

  const traceNetwork = (start: string): number => {
    let curr = start;
    let count = 0;
    let step = 0;

    while (curr.split('')[2] !== 'Z') {
      if (steps) {
        count = count + 1;
        curr = network[curr][steps[step]];

        step = step + 1 === steps.length ? 0 : step + 1;
      }
    }

    return count;
  };

  const runs = Object.keys(network).filter((element) => {
    return element.lastIndexOf('A') === 2;
  });

  const counts = runs.map((run) => {
    return traceNetwork(run);
  });

  return counts.reduce((prev: any, curr: any) => {
    return lcm(prev, curr);
  });
};
