import fs from 'fs';

export const solution1 = () => {
  const input = fs.readFileSync(`${__dirname}/data/data.txt`, 'utf-8');

  const lines = input.split('\n');

  const cards = [
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    'T',
    'J',
    'Q',
    'K',
    'A',
  ];

  const getCards = (hand: any): any => {
    const raw = hand.split(' ');

    return raw[0].split('');
  };

  const calculateHand = (hand: any) => {
    const result: any = {};

    getCards(hand).forEach((card: string) => {
      result[card] ? (result[card] += 1) : (result[card] = 1);
    });

    const values = Object.values(result);

    values.sort((a: any, b: any) => {
      return b - a;
    });

    if (values.length === 1) {
      return 7;
    }

    if (values.length === 2) {
      if (values[0] === 4) {
        return 6;
      } else {
        return 5;
      }
    }

    if (values.length === 3) {
      if (values[0] === 3) {
        return 4;
      } else {
        return 3;
      }
    }

    if (values.length === 4) {
      return 2;
    }

    if (values.length === 5) {
      return 1;
    }
  };

  const compareCards = (hand1: any, hand2: any) => {
    const cards1 = getCards(hand1);
    const cards2 = getCards(hand2);

    for (let i = 0; i < cards1.length; i++) {
      if (cards.indexOf(cards1[i]) > cards.indexOf(cards2[i])) {
        return 1;
      }
      if (cards.indexOf(cards2[i]) > cards.indexOf(cards1[i])) {
        return 2;
      }
    }

    return 1;
  };
  const sorter = (a: any, b: any) => {
    const aVal: any = calculateHand(a);
    const bVal: any = calculateHand(b);
    let output: any = 0;

    if (aVal > bVal) {
      output = 1;
    } else if (bVal > aVal) {
      output = -1;
    } else {
      const comp = compareCards(a, b);

      output = comp === 1 ? 1 : -1;
    }

    return output;
  };

  lines.sort(sorter);

  const output = lines
    .map((line: any) => {
      return Number(line.split(' ')[1]);
    })
    .reduce((prev: number, curr: number, idx: number) => {
      return prev + curr * (idx + 1);
    });

  return output;
};
