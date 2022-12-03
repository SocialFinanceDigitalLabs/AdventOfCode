import fs from "fs";

export const solution1 = () => {
  const input = fs.readFileSync("./data/data.txt", "utf-8");
  const strings = "-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
  const rows = input.split("\n");

  const items = rows.map((row) => {
    const first = row.substring(0, row.length / 2).split("");
    const second = row.substring(row.length / 2).split("");

    let match = "";

    first.forEach((char) => {
      if (second.indexOf(char) > -1) {
        match = second[second.indexOf(char)];
      }
    });

    return strings.indexOf(match);
  });

  const total = items.reduce((acc, curr) => {
    return acc + curr;
  });

  return total;
};
