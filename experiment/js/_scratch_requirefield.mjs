import { FeedError } from "./newsroom/errors.mjs";

export function requireField(item, field) {
  if (item[field]) return true;
  throw new FeedError("MISSING_FIELD", `Missing required field: ${field}`);
}

// Quick self-test
const item = { title: "Hello", body: "" };

// Should return true
console.assert(requireField(item, "title") === true, "present field should return true");

// Should throw for falsy value
let threw = false;
try {
  requireField(item, "body");
} catch (e) {
  threw = true;
  console.assert(e instanceof FeedError, "should be FeedError");
  console.assert(e.code === "MISSING_FIELD", "code should be MISSING_FIELD");
}
console.assert(threw, "should have thrown for falsy field");

// Should throw for absent key
threw = false;
try {
  requireField(item, "author");
} catch (e) {
  threw = true;
  console.assert(e instanceof FeedError, "should be FeedError for absent key");
}
console.assert(threw, "should have thrown for absent key");

console.log("All assertions passed.");
