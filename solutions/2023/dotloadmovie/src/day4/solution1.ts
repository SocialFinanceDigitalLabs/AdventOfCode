import fs from 'fs';

export const solution1 = () => {
  const input = fs
    .readFileSync(`${__dirname}/data/data.txt`, 'utf-8')
    .replaceAll('  ', ' ');

  const lines = input.split('\n');

  const checkCard = (theirs: any, ours: any): any => {
    const matches = theirs.filter((num: string) => {
      return ours.indexOf(num) > -1;
    });

    let result = 0;

    for (let i = 0; i < matches.length; i++) {
      result = i === 0 ? 1 : result * 2;
    }

    return result;
  };

  const results = lines.map((line: any) => {
    const sections = line.split(/\:|\|/);

    return checkCard(
      sections[1].trim().split(' '),
      sections[2].trim().split(' ')
    );
  });

  return results.reduce((curr, next) => {
    return curr + next;
  });
};
