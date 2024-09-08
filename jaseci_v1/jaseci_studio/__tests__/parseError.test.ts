import { test, expect } from "vitest";
import { parseErrors } from "../src/hooks/useRegisterArchetype";

test("parseErrors", async () => {
  let parsed = parseErrors([
    "main: line 1:7 - unparsed:main:0:0: - mismatched input 'test' expecting NAME",
  ]);

  expect(parsed).toStrictEqual([
    { line: 1, column: 7, message: "mismatched input 'test' expecting NAME" },
  ]);
});
