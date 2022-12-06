import fs from "fs";

export const solution1 = () => {
  const input = fs.readFileSync("./data/data.txt", "utf-8");
  const stream = input.split("");

  let position = -1;
  let buffer: string[] = [];
  const bufferLength = 4;

  const findRepeatChars = (chars: string[]): boolean => {
    const dedupe = chars.filter((char, i, arr) => {
      return arr.indexOf(char) === i;
    });

    if (dedupe.length < bufferLength) {
      return false;
    }

    return true;
  };

  stream.forEach((char, i) => {
    buffer.push(char);

    if (buffer.length > bufferLength) {
      buffer.shift();
      if (position < 0 && findRepeatChars(buffer.slice())) {
        position = i + 1;
      }
    }
  });

  return position;
};
