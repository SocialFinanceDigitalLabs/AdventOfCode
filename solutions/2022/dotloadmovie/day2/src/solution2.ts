import fs from "fs";

export const solution2 = () => {
  const getResult = (p1: string, p2: string): number => {
    const scores = {
      A: { score: 1, wins: "C", loses: "B" },
      B: { score: 2, wins: "A", loses: "C" },
      C: { score: 3, wins: "B", loses: "A" },
    };

    const score1 = scores[p1 as keyof typeof scores];

    let me = p1;

    if (p2 === "X") {
      me = score1.wins;
    }

    if (p2 === "Z") {
      me = score1.loses;
    }

    const score2 = scores[me as keyof typeof scores];

    let outcome = 3;

    if (score1.wins === me) {
      outcome = 0;
    }

    if (score1.loses === me) {
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
