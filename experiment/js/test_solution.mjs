import { requireField } from './solution.mjs';

// Test 1: field present and truthy -> returns true
const item1 = { title: 'Hello', author: 'Alice' };
const result1 = requireField(item1, 'title');
console.assert(result1 === true, 'Expected true for present truthy field');
console.log('Test 1 passed: returns true for present truthy field');

// Test 2: field missing -> throws error
try {
  requireField({}, 'title');
  console.log('Test 2 FAILED: should have thrown');
} catch (e) {
  console.log('Test 2 passed: throws for missing field:', e.message);
}

// Test 3: field present but falsy (empty string) -> throws error
try {
  requireField({ title: '' }, 'title');
  console.log('Test 3 FAILED: should have thrown');
} catch (e) {
  console.log('Test 3 passed: throws for falsy field:', e.message);
}

// Test 4: field present but null -> throws error
try {
  requireField({ title: null }, 'title');
  console.log('Test 4 FAILED: should have thrown');
} catch (e) {
  console.log('Test 4 passed: throws for null field:', e.message);
}

// Test 5: field present and 0 (falsy number) -> throws error
try {
  requireField({ count: 0 }, 'count');
  console.log('Test 5 FAILED: should have thrown');
} catch (e) {
  console.log('Test 5 passed: throws for 0 value:', e.message);
}

console.log('All tests passed!');
