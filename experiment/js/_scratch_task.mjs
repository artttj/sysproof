import { FeedError } from "./newsroom/errors.mjs";

export function requireField(item, field) {
  if (item[field]) return true;
  throw new FeedError("MISSING_FIELD", `field '${field}' is missing`);
}

// Quick self-test
try {
  console.log(requireField({ title: "hello" }, "title")); // true
} catch (e) {
  console.error("Unexpected error:", e.message);
}

try {
  requireField({ title: "" }, "title");
  console.error("Should have thrown");
} catch (e) {
  console.log("Threw as expected:", e.message, "| code:", e.code);
}

try {
  requireField({}, "title");
  console.error("Should have thrown");
} catch (e) {
  console.log("Threw as expected:", e.message, "| code:", e.code);
}

try {
  requireField({ title: null }, "title");
  console.error("Should have thrown");
} catch (e) {
  console.log("Threw as expected:", e.message, "| code:", e.code);
}
