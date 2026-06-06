import { requireField } from './solution.mjs';

// Test 1: truthy value returns true
const item = { title: 'Hello', count: 1 };
console.assert(requireField(item, 'title') === true, 'truthy string should return true');
console.assert(requireField(item, 'count') === true, 'truthy number should return true');

// Test 2: missing field throws
let threw = false;
try {
  requireField(item, 'missing');
} catch (e) {
  threw = true;
  console.assert(e.message.includes('missing'), `error message should mention the field: ${e.message}`);
}
console.assert(threw, 'missing field should throw');

// Test 3: falsy field throws
threw = false;
try {
  requireField({ name: '' }, 'name');
} catch (e) {
  threw = true;
}
console.assert(threw, 'empty string field should throw');

// Test 4: null field throws
threw = false;
try {
  requireField({ val: null }, 'val');
} catch (e) {
  threw = true;
}
console.assert(threw, 'null field should throw');

// Test 5: zero field throws
threw = false;
try {
  requireField({ val: 0 }, 'val');
} catch (e) {
  threw = true;
}
console.assert(threw, 'zero field should throw');

console.log('All tests passed.');
