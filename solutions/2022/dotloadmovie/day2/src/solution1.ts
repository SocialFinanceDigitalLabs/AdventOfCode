import fs from "fs";

export const solution1 = () => {
  const getResult = (p1: string, p2: string): number => {
    const scores = {
      A: { score: 1, wins: "Z", loses: "Y" },
      B: { score: 2, wins: "X", loses: "Z" },
      C: { score: 3, wins: "Y", loses: "X" },
      X: { score: 1, wins: "C", loses: "B" },
      Y: { score: 2, wins: "A", loses: "C" },
      Z: { score: 3, wins: "B", loses: "A" },
    };

    const score1 = scores[p1 as keyof typeof scores];
    const score2 = scores[p2 as keyof typeof scores];

    let outcome = 3;

    if (score1.wins === p2) {
      outcome = 0;
    }

    if (score1.loses === p2) {
      outcome = 6;
    }

    return score2.score + outcome;
  };

  const input = fs.readFileSync("./data/data1.txt", "utf-8");
  const rows = input.split("\n");

  const values = rows.map((row) => {
    const positions = row.split(" ");

    return getResult(positions[0], positions[1]);
  });

  const total = values.reduce((acc, curr) => {
    return acc + curr;
  });

  return total;
};
