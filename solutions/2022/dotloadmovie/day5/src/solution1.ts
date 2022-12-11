import fs from "fs";

export const solution1 = () => {
  const input = fs.readFileSync("./data/data.txt", "utf-8");
  const list = input.split("\n");

  /*
              [M] [S] [S]            
        [M] [N] [L] [T] [Q]        
[G]     [P] [C] [F] [G] [T]        
[B]     [J] [D] [P] [V] [F] [F]    
[D]     [D] [G] [C] [Z] [H] [B] [G]
[C] [G] [Q] [L] [N] [D] [M] [D] [Q]
[P] [V] [S] [S] [B] [B] [Z] [M] [C]
[R] [H] [N] [P] [J] [Q] [B] [C] [F]
 1   2   3   4   5   6   7   8   9 
  */

  //const stacks = [["Z", "N"], ["M", "C", "D"], ["P"]];
  const stacks = [
    ["R", "P", "C", "D", "B", "G"],
    ["H", "V", "N"],
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
    for (let i = 0; i < count; i++) {
      const val = stacks[from].pop();
      stacks[to].push(val as string);
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
