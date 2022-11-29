import fs from "fs";

export const solution1 = () => {
  const input = fs.readFileSync("./data/data.txt", "utf-8");
  return input;
};
