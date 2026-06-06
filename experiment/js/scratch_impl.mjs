export function requireField(item, field) {
  if (item[field]) {
    return true;
  }
  throw new Error(`Missing required field: ${field}`);
}

// Test it
const item = { name: 'Alice', age: 30 };

console.log(requireField(item, 'name')); // true
console.log(requireField(item, 'age'));  // true

try {
  requireField(item, 'email');
} catch (e) {
  console.log('Caught:', e.message);
}

try {
  requireField({ empty: '' }, 'empty');
} catch (e) {
  console.log('Caught falsy:', e.message);
}

try {
  requireField({}, 'missing');
} catch (e) {
  console.log('Caught missing:', e.message);
}
