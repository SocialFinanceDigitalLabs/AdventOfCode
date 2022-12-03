import fs from "fs";

type rowStr = string[];

export const solution2 = () => {
  const input = fs.readFileSync("./data/data.txt", "utf-8");
  const strings = "-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
  const rows = input.split("\n");
  const groups: rowStr[] = [];

  rows.forEach((row, i) => {
    if (i % 3 === 0) {
      groups.unshift([]);
    }

    groups[0].push(row);
  });

  const items = groups.map((group) => {
    const first = group[0].split("");

    let output = "";

    first.forEach((char) => {
      if (group[1].indexOf(char) > -1 && group[2].indexOf(char) > -1) {
        output = char;
      }
    });

    return strings.indexOf(output);
  });

  const total = items.reduce((acc, curr) => {
    return acc + curr;
  });

  return total;
};
