import { IdempotencyStore, processWithIdempotency } from './idempotency.mjs';
import { Dlq, isPoison } from './dlq.mjs';
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)));
const eventContract = JSON.parse(readFileSync(resolve(ROOT, 'event-contract.json'), 'utf8'));

export function createWorker({ store = new IdempotencyStore(), dlq = new Dlq() } = {}) {
  return {
    store,
    dlq,
    handle(raw) {
      if (isPoison(raw, eventContract)) {
        return dlq.receiveAttempt({ id: raw?.event_id ?? 'unknown', body: raw, receiveCount: 3 });
      }
      return processWithIdempotency(store, raw, (event) => ({
        ok: true,
        tenant_id: event.tenant_id,
        type: event.type
      }));
    }
  };
}
