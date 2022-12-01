import fs from "fs";

export const solution2 = () => {
  const input = fs.readFileSync("./data/data2.txt", "utf-8");

  const groups = input.split("\n\n");

  const output = groups
    .map((group) => {
      return group
        .split("\n")
        .map((el) => parseInt(el))
        .reduce((acc, curr): any => {
          return acc + curr;
        });
    })
    .sort((a, b) => {
      return a - b;
    })
    .reverse();

  const collective = output.slice(0, 3).reduce((acc, curr) => {
    return acc + curr;
  });

  return collective;
};
