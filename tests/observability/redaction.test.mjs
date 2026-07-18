import test from 'node:test';
import assert from 'node:assert/strict';
import { redactObject, assertNoSecrets } from '../../observability/otel/redaction.mjs';

test('redacts secrets and tenant-sensitive fields', () => {
  const input = {
    message: 'ok',
    password: 'hunter2',
    authorization: 'Bearer abc',
    tenant_id: 't1',
    payload: { ssn: '123-45-6789', order_id: 'o1' }
  };
  const out = redactObject(input);
  assert.equal(out.password, '[REDACTED]');
  assert.equal(out.authorization, '[REDACTED]');
  assert.equal(out.payload.ssn, '[REDACTED]');
  assert.equal(out.payload.order_id, 'o1');
  assert.equal(out.tenant_id, 't1');
  assertNoSecrets(out);
});
