/**
 * Idempotency store (in-memory for unit tests; DynamoDB in production design).
 */
export class IdempotencyStore {
  constructor() {
    this.map = new Map();
  }

  seen(key) {
    return this.map.has(key);
  }

  record(key, result = { status: 'processed' }) {
    if (this.map.has(key)) return { duplicate: true, prior: this.map.get(key) };
    this.map.set(key, result);
    return { duplicate: false, result };
  }
}

export function processWithIdempotency(store, event, handler) {
  if (!event?.event_id) throw new Error('event_id required');
  if (store.seen(event.event_id)) {
    return { status: 'duplicate_skipped', event_id: event.event_id };
  }
  const result = handler(event);
  store.record(event.event_id, result);
  return { status: 'processed', event_id: event.event_id, result };
}
