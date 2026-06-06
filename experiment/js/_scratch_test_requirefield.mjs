import { requireField } from './solution.mjs';
import { FeedError } from './newsroom/errors.mjs';

// Test 1: truthy field returns true
const item = { title: 'Hello', body: 'World' };
const result = requireField(item, 'title');
console.assert(result === true, 'Expected true for present truthy field');
console.log('Test 1 passed: returns true for truthy field');

// Test 2: throws FeedError for missing field
try {
  requireField({}, 'title');
  console.error('Test 2 FAILED: should have thrown');
} catch (e) {
  console.assert(e instanceof FeedError, 'Expected FeedError');
  console.assert(e.code === 'MISSING_FIELD', `Expected code MISSING_FIELD, got ${e.code}`);
  console.assert(e.message.includes('title'), `Expected message to mention field name, got: ${e.message}`);
  console.log('Test 2 passed: throws FeedError for missing field');
}

// Test 3: throws for falsy field (empty string)
try {
  requireField({ title: '' }, 'title');
  console.error('Test 3 FAILED: should have thrown for empty string');
} catch (e) {
  console.assert(e instanceof FeedError, 'Expected FeedError');
  console.log('Test 3 passed: throws FeedError for falsy (empty string) field');
}

// Test 4: throws for null field
try {
  requireField({ title: null }, 'title');
  console.error('Test 4 FAILED: should have thrown for null');
} catch (e) {
  console.assert(e instanceof FeedError, 'Expected FeedError');
  console.log('Test 4 passed: throws FeedError for null field');
}

// Test 5: returns true for numeric truthy value
const result2 = requireField({ count: 42 }, 'count');
console.assert(result2 === true, 'Expected true for numeric truthy field');
console.log('Test 5 passed: returns true for numeric truthy field');

console.log('\nAll tests passed!');
