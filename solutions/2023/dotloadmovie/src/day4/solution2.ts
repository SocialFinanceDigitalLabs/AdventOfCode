import fs from 'fs';

export const solution2 = () => {
  const input = fs
    .readFileSync(`${__dirname}/data/data.txt`, 'utf-8')
    .replaceAll('  ', ' ');

  const lines: any = input.split('\n').map((line, i) => {
    return { line, count: 1 };
  });

  const samples: any = [];

  const checkCard = (theirs: any, ours: any, current: number): any => {
    const matches = theirs.filter((num: string) => {
      return ours.indexOf(num) > -1;
    });

    for (let i = current + 1; i < current + (matches.length + 1); i++) {
      lines[i].count += 1;
    }
  };

  lines.forEach((line: any, idx: number) => {
    const sections = line.line.split(/\:|\|/);

    for (let i = 0; i < line.count; i++) {
      checkCard(
        sections[1].trim().split(' '),
        sections[2].trim().split(' '),
        idx
      );
    }
  });

  let output = 0;

  lines.forEach((line: any) => {
    output += line.count;
  });

  return output;
};
