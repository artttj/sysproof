import { requireField } from './solution.mjs';

// Test: truthy field returns true
const item = { name: 'Alice', age: 30 };
console.assert(requireField(item, 'name') === true, 'Should return true for truthy field');
console.assert(requireField(item, 'age') === true, 'Should return true for numeric truthy field');

// Test: missing field throws
try {
  requireField(item, 'email');
  console.assert(false, 'Should have thrown');
} catch (e) {
  console.assert(e instanceof Error, 'Should throw Error');
  console.assert(e.message.includes('email'), `Error message should mention field name, got: ${e.message}`);
}

// Test: falsy field (empty string) throws
try {
  requireField({ name: '' }, 'name');
  console.assert(false, 'Should have thrown for empty string');
} catch (e) {
  console.assert(e instanceof Error, 'Should throw Error for falsy value');
}

// Test: null value throws
try {
  requireField({ name: null }, 'name');
  console.assert(false, 'Should have thrown for null');
} catch (e) {
  console.assert(e instanceof Error, 'Should throw Error for null');
}

// Test: undefined field (field not present) throws
try {
  requireField({}, 'missing');
  console.assert(false, 'Should have thrown for undefined field');
} catch (e) {
  console.assert(e instanceof Error, 'Should throw Error for undefined field');
}

console.log('All tests passed.');
