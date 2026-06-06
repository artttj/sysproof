import { FeedError } from "./newsroom/errors.mjs";

export function requireField(item, field) {
  if (item[field]) {
    return true;
  }
  throw new FeedError("MISSING_FIELD", `field "${field}" is missing`);
}

// Self-test
const item = { title: "Hello", body: "" };

// Should return true for truthy field
const result = requireField(item, "title");
console.assert(result === true, "expected true for truthy field");

// Should throw for falsy/missing field
let threw = false;
try {
  requireField(item, "body");
} catch (e) {
  threw = true;
  console.assert(e.name === "FeedError", "expected FeedError");
  console.assert(e.code === "MISSING_FIELD", "expected MISSING_FIELD code");
}
console.assert(threw, "expected throw for falsy field");

threw = false;
try {
  requireField(item, "nonexistent");
} catch (e) {
  threw = true;
  console.assert(e.name === "FeedError", "expected FeedError for missing key");
}
console.assert(threw, "expected throw for missing key");

console.log("All assertions passed.");
