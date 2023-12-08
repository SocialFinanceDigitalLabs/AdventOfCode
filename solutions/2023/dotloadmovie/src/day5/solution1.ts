import fs from 'fs';

export const solution1 = () => {
  const input = fs.readFileSync(`${__dirname}/data/data.txt`, 'utf-8');

  const parseMap = (input: any): any => {
    const rows = input.split('\n');

    const output = {
      name: rows.shift().split('map')[0].trim(),
      map: [],
    };

    output.map = rows.map((row: any) => {
      const vals = row.trim().split(' ');
      return {
        dest: Number(vals[0]),
        src: Number(vals[1]),
        range: Number(vals[2]),
      };
    });

    return output;
  };

  const getDestinationFromSource = (map: any, input: any) => {
    let output = -1,
      i = 0;

    while (output === -1 && i < map.length) {
      if (input >= map[i].src && input <= map[i].src + map[i].range) {
        output = input - map[i].src + map[i].dest;
        break;
      }
      i++;
    }

    output = output > -1 ? output : input;

    return output;
  };

  const raw = input.split('\n\n');

  let seeds: any = raw.shift()?.split(' ');
  seeds?.shift();
  seeds = seeds?.map((seed: any) => {
    return Number(seed.trim());
  });

  const maps = raw.map((section: any) => {
    return parseMap(section);
  });

  const output = seeds.map((seed: any) => {
    let value = seed,
      i = 0;

    while (i < maps.length) {
      value = getDestinationFromSource(maps[i].map, value);
      i++;
    }

    return value;
  });

  output.sort((a: any, b: any) => {
    return a - b;
  });

  return output[0];
};
