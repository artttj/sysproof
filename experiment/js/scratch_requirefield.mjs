import { FeedError } from "./newsroom/errors.mjs";

export function requireField(item, field) {
  if (item[field]) return true;
  throw new FeedError("MISSING_FIELD", `Missing required field: ${field}`);
}

// Quick self-test
import assert from "assert";

assert.strictEqual(requireField({ title: "Hello" }, "title"), true);

try {
  requireField({}, "title");
  assert.fail("should have thrown");
} catch (e) {
  assert(e instanceof FeedError, "should be FeedError");
  assert.strictEqual(e.code, "MISSING_FIELD");
  assert(/title/.test(e.message), "message should mention field name");
}

try {
  requireField({ title: null }, "title");
  assert.fail("should have thrown");
} catch (e) {
  assert(e instanceof FeedError);
}

try {
  requireField({ title: "" }, "title");
  assert.fail("should have thrown");
} catch (e) {
  assert(e instanceof FeedError);
}

console.log("All assertions passed.");
