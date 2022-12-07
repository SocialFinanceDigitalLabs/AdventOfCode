import fs from "fs";
import { get } from "lodash";

export const solution1 = () => {
  const input = fs.readFileSync("./data/data.txt", "utf-8");

  const tree: any = { "/": {} };

  const walkTree = () => {
    const output: number[] = [];

    const walk = (obj: any): any => {
      const level: number[] = [];

      Object.values(obj).forEach((item: any) => {
        if (item.size) {
          level.push(item.size);
        } else {
          level.push(walk(item));
        }
      });

      const total = level.reduce((acc, curr) => {
        return acc + curr;
      });

      output.push(total);
      return total;
    };

    walk(tree);

    return output;
  };

  const makeTree = () => {
    const commands = input.split("\n");
    let path: string[] = [];

    const loop = (actions: string[], subtree: any) => {
      const action = actions.shift();
      let newTree = subtree;

      if (action) {
        if (action[0] === "$") {
          const directive = action.split(" ");
          if (directive[1] === "cd") {
            if (directive[2] === "..") {
              path.pop();
            } else {
              path.push(directive[2]);
            }

            newTree = get(tree, path.join("."));
          }
        } else {
          const file = action.split(" ");
          if (file[0] === "dir") {
            subtree[file[1]] = {};
          } else {
            subtree[file[1]] = { size: parseInt(file[0]) };
          }
        }
      }

      if (actions.length > 0) {
        loop(actions, newTree);
      }
    };

    loop(commands, tree);
  };

  makeTree();
  const output = walkTree().reduce((acc, curr) => {
    return acc + (curr <= 100000 ? curr : 0);
  });

  return output;
};
