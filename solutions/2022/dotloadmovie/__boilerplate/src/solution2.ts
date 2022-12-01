import fs from "fs";

export const solution2 = () => {
  const input = fs.readFileSync("./data/data.txt", "utf-8");
  return input;
};
