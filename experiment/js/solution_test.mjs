import { requireField } from './solution.mjs';

// Test 1: field present and truthy
const item1 = { name: 'Alice', age: 30 };
const result1 = requireField(item1, 'name');
console.assert(result1 === true, 'Should return true for truthy field');

// Test 2: field present but falsy (empty string)
let threw = false;
try {
  requireField({ name: '' }, 'name');
} catch (e) {
  threw = true;
  console.assert(e.message.includes('name'), 'Error should mention field name');
}
console.assert(threw, 'Should throw for falsy field');

// Test 3: field missing (undefined)
threw = false;
try {
  requireField({ age: 25 }, 'name');
} catch (e) {
  threw = true;
  console.assert(e.message.includes('name'), 'Error should mention field name');
}
console.assert(threw, 'Should throw for missing field');

// Test 4: field present with value 0 (falsy)
threw = false;
try {
  requireField({ count: 0 }, 'count');
} catch (e) {
  threw = true;
}
console.assert(threw, 'Should throw for 0 value (falsy)');

// Test 5: field present with false (falsy)
threw = false;
try {
  requireField({ active: false }, 'active');
} catch (e) {
  threw = true;
}
console.assert(threw, 'Should throw for false value (falsy)');

// Test 6: field present with null (falsy)
threw = false;
try {
  requireField({ data: null }, 'data');
} catch (e) {
  threw = true;
}
console.assert(threw, 'Should throw for null value (falsy)');

// Test 7: numeric truthy value
const result7 = requireField({ count: 42 }, 'count');
console.assert(result7 === true, 'Should return true for truthy numeric field');

console.log('All tests passed!');
