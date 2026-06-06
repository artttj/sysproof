import { FeedError } from "./newsroom/errors.mjs";

export function requireField(item, field) {
  if (item[field]) return true;
  throw new FeedError("MISSING_FIELD", `field "${field}" is missing`);
}

// quick smoke test
try {
  console.log(requireField({ title: "hello" }, "title")); // true
} catch (e) {
  console.error("unexpected error:", e.message);
}

try {
  requireField({ title: "" }, "title");
  console.error("should have thrown");
} catch (e) {
  console.log("caught missing empty string:", e.message);
  console.log("code:", e.code);
  console.log("name:", e.name);
}

try {
  requireField({}, "author");
  console.error("should have thrown");
} catch (e) {
  console.log("caught missing key:", e.message);
}
