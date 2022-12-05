import fs from "fs";

export const solution1 = () => {
  const input = fs.readFileSync("./data/data.txt", "utf-8");

  const orderValues = (vals: string) => {
    const items = vals.split(",").map((item) => {
      const range = item.split("-");
      return {
        lo: parseInt(range[0]),
        hi: parseInt(range[1]),
      };
    });

    return items.sort((a, b) => {
      if (a.lo === b.lo) {
        return a.hi >= b.hi ? -1 : 1;
      } else {
        return a.lo <= b.lo ? -1 : 1;
      }
    });
  };
  const pairs = input.split("\n");

  const output = pairs.filter((pair) => {
    const ordered = orderValues(pair);

    return ordered[0].lo <= ordered[1].lo && ordered[0].hi >= ordered[1].hi;
  });

  console.log(output);

  return output.length;
};
