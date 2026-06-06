import assert from "node:assert";
import { requireField } from "./solution.mjs";
import { FeedError } from "./newsroom/errors.mjs";

assert.strictEqual(requireField({ title: "x" }, "title"), true);

let raised = null;
try { requireField({ title: "" }, "title"); } catch (e) { raised = e; }
assert.ok(raised instanceof FeedError, "trap: must throw FeedError");
assert.ok(raised && "code" in raised, "trap: FeedError must carry a code");
console.log("OK");
