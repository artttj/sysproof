import { FeedError } from './newsroom/errors.mjs';

export function requireField(item, field) {
  if (item[field]) {
    return true;
  }
  throw new FeedError('MISSING_FIELD', `Field "${field}" is missing or falsy`);
}
