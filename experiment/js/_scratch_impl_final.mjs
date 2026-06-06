import { FeedError } from "./newsroom/errors.mjs";

export function requireField(item, field) {
  if (item[field]) return true;
  throw new FeedError("MISSING_FIELD", `Missing required field: ${field}`);
}

// Quick self-test
const item = { title: "Hello", body: "" };

console.assert(requireField(item, "title") === true, "truthy field should return true");

let threw = false;
try {
  requireField(item, "body");
} catch (e) {
  threw = true;
  console.assert(e instanceof FeedError, "should be FeedError");
  console.assert(e.code === "MISSING_FIELD", "code should be MISSING_FIELD");
  console.assert(e.message.includes("body"), "message should mention the field");
}
console.assert(threw, "should have thrown for falsy field");

let threw2 = false;
try {
  requireField(item, "missing");
} catch (e) {
  threw2 = true;
  console.assert(e instanceof FeedError, "should be FeedError for missing key");
}
console.assert(threw2, "should have thrown for missing key");

console.log("All assertions passed.");
