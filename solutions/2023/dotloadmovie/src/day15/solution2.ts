import fs from 'fs';
import { computeFragmentHash } from './solution1';

export const solution2 = () => {
  const input = fs
    .readFileSync(`${__dirname}/data/data.txt`, 'utf-8')
    .split(',');

  const removeItem = (arr: any, key: string): any => {
    const output = arr.filter((item: any) => {
      if (item.key !== key) {
        return true;
      }

      return false;
    });

    return output;
  };

  const addItem = (arr: any, key: string, value: number) => {
    let matched = false;

    arr.forEach((item: any) => {
      if (item.key === key) {
        item.value = value;

        matched = true;
      }
    });

    if (!matched) {
      arr.push({ key, value });
    }

    return arr;
  };

  const structure: any = {};

  input.forEach((item: any) => {
    const division: string = item.indexOf('=') > -1 ? '=' : '-';
    const partials = item.split(division);

    const value = computeFragmentHash(partials[0]);

    if (division === '-') {
      structure[`${value}`] = removeItem(
        structure[`${value}`] || [],
        partials[0]
      );
    } else {
      structure[`${value}`] = addItem(
        structure[`${value}`] || [],
        partials[0],
        Number(partials[1])
      );
    }
  });

  let output = 0;

  Object.keys(structure).forEach((key: string) => {
    const values = structure[key];

    if (values.length > 0) {
      const offset = Number(key) + 1;

      values.forEach((value: any, i: number) => {
        const total = offset * (i + 1) * value.value;
        output += total;
      });
    }
  });

  return output;
};
