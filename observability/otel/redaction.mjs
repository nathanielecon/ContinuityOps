const SECRET_KEYS = /password|secret|api[_-]?key|authorization|token/i;
const TENANT_SENSITIVE = /ssn|card_number|email_raw/i;

export function redactValue(key, value) {
  if (SECRET_KEYS.test(key) || TENANT_SENSITIVE.test(key)) return '[REDACTED]';
  if (value && typeof value === 'object' && !Array.isArray(value)) {
    return redactObject(value);
  }
  return value;
}

export function redactObject(input) {
  if (input == null || typeof input !== 'object') return input;
  if (Array.isArray(input)) return input.map((item, idx) => redactValue(String(idx), item));
  const out = {};
  for (const [key, value] of Object.entries(input)) {
    out[key] = redactValue(key, value);
  }
  return out;
}

export function assertNoSecrets(obj, path = '') {
  if (obj == null || typeof obj !== 'object') return;
  for (const [key, value] of Object.entries(obj)) {
    const next = path ? `${path}.${key}` : key;
    if (typeof value === 'string' && SECRET_KEYS.test(key) && value !== '[REDACTED]') {
      throw new Error(`unredacted secret at ${next}`);
    }
    if (typeof value === 'object') assertNoSecrets(value, next);
  }
}
