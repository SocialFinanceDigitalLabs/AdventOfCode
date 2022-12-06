import { solution1, solution2 } from "./index";

describe("tests", () => {
  test("test solution1", () => {
    const output = solution1();
    console.log(output);
    expect(output).toEqual(1287);
  });

  test("test solution2", () => {
    const output = solution2();
    console.log(output);
    expect(output).toEqual(3716);
  });
});
