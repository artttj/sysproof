import { FeedError } from './newsroom/errors.mjs';

export function requireField(item, field) {
  if (item[field]) {
    return true;
  }
  throw new FeedError('MISSING_FIELD', `Missing required field: ${field}`);
}

// Tests
const item = { name: 'Alice', age: 30 };

console.assert(requireField(item, 'name') === true, 'truthy string should return true');
console.assert(requireField(item, 'age') === true, 'truthy number should return true');

let threw = false;
try {
  requireField(item, 'email');
} catch (e) {
  threw = true;
  console.assert(e instanceof FeedError, 'should throw FeedError');
  console.assert(e.code === 'MISSING_FIELD', 'code should be MISSING_FIELD');
  console.assert(e.message.includes('email'), 'message should mention field name');
}
console.assert(threw, 'should have thrown for missing field');

threw = false;
try {
  requireField({ empty: '' }, 'empty');
} catch (e) {
  threw = true;
  console.assert(e instanceof FeedError, 'should throw FeedError for falsy value');
}
console.assert(threw, 'should have thrown for falsy field');

threw = false;
try {
  requireField({ zero: 0 }, 'zero');
} catch (e) {
  threw = true;
  console.assert(e instanceof FeedError, 'should throw FeedError for 0');
}
console.assert(threw, 'should have thrown for zero value');

console.log('All assertions passed');
