import assert from "node:assert/strict";
import { test } from "node:test";
import { KeywordMatcher, parseKeywords } from "../src/matching.ts";

const keywords = parseKeywords([
  { id: "shpargalka", words: ["шпаргалка", "чек лист"], url: "https://x" },
  { id: "guide", words: ["гайд"], url: "https://y" },
]);
const matcher = new KeywordMatcher(keywords);

test("whole word in any case and with punctuation", () => {
  for (const text of ["шпаргалка", "ШПАРГАЛКА!", "Мехоҳам шпаргалка 🔥", "  Шпаргалка."]) {
    assert.equal(matcher.match(text)?.id, "shpargalka", text);
  }
});

test("phrase with extra spaces", () => {
  assert.equal(matcher.match("Чек   лист лутфан")?.id, "shpargalka");
});

test("part of a word does not match", () => {
  assert.equal(matcher.match("гайдҳо хуб"), null);
  assert.equal(matcher.match("шпаргалкаро"), null);
});

test("other keyword and empty text", () => {
  assert.equal(matcher.match("гайд")?.id, "guide");
  assert.equal(matcher.match(""), null);
  assert.equal(matcher.match(undefined), null);
});

test("defaults for message and button", () => {
  assert.match(keywords[0].message, /\{url\}/);
  assert.ok(keywords[0].button);
});

test("rejects bad and duplicate ids", () => {
  assert.throws(() => parseKeywords([{ id: "шпаргалка", words: ["a"], url: "u" }]));
  assert.throws(() =>
    parseKeywords([
      { id: "a", words: ["x"], url: "u" },
      { id: "a", words: ["y"], url: "u" },
    ]),
  );
  assert.throws(() => parseKeywords([{ id: "a", words: [], url: "u" }]));
});

test("keywords.json is valid", async () => {
  const { default: raw } = await import("../keywords.json", { with: { type: "json" } });
  assert.ok(parseKeywords(raw).length > 0);
});
