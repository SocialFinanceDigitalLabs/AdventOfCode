import fs from "fs";

export const solution1 = () => {
  const input = fs.readFileSync("./data/data1.txt", "utf-8");

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

  return output[0];
};
