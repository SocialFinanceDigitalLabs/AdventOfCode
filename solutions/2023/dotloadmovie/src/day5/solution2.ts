import fs from 'fs';

export const solution2 = () => {
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

  let rawSeeds: any = raw.shift()?.split(' ');
  rawSeeds?.shift();
  rawSeeds = rawSeeds?.map((seed: any) => {
    return Number(seed.trim());
  });

  let output = -1;

  const maps = raw.map((section: any) => {
    return parseMap(section);
  });

  const generateSeedsFromRange = (start: number, length: number) => {
    for (let i = start; i < start + length; i++) {
      let value = i,
        j = 0;

      while (j < maps.length) {
        value = getDestinationFromSource(maps[j].map, value);
        j++;
      }

      if (output === -1) {
        output = value;
      } else {
        if (value < output) {
          output = value;
        }
      }
    }
  };

  for (let i = 0; i < rawSeeds.length; i += 2) {
    generateSeedsFromRange(rawSeeds[i], rawSeeds[i + 1]);
  }

  return output;
};
