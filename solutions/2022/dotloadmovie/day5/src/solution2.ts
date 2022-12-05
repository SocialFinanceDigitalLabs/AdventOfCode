import fs from "fs";

export const solution2 = () => {
  const input = fs.readFileSync("./data/data.txt", "utf-8");
  const list = input.split("\n");

  const stacks = [
    ["R", "P", "C", "D", "B", "G"],
    ["H", "V", "G"],
    ["N", "S", "Q", "D", "J", "P", "M"],
    ["P", "S", "L", "G", "D", "C", "N", "M"],
    ["J", "B", "N", "C", "P", "F", "L", "S"],
    ["Q", "B", "D", "Z", "V", "G", "T", "S"],
    ["B", "Z", "M", "H", "F", "T", "Q"],
    ["C", "M", "D", "B", "F"],
    ["F", "C", "Q", "G"],
  ];

  const prepareInstructions = (instructions: string): string => {
    return instructions
      .replace(/move/gi, "")
      .replace(/from/gi, "")
      .replace(/to/gi, "")
      .trim();
  };

  const moveItems = (from: number, to: number, count: number) => {
    const holder = [];

    for (let i = 0; i < count; i++) {
      holder.unshift(stacks[from].pop());
    }
    for (let i = 0; i < count; i++) {
      stacks[to].push(holder.shift() as string);
    }
  };
  list.forEach((row) => {
    const instructions = prepareInstructions(row).split("  ");

    moveItems(
      parseInt(instructions[1]) - 1,
      parseInt(instructions[2]) - 1,
      parseInt(instructions[0])
    );
  });

  return stacks
    .map((stack) => {
      return stack.reverse()[0];
    })
    .join("");
};
