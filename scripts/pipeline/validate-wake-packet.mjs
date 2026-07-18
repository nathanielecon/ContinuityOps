/**
 * Validate junior exception wake packet (D-047).
 */

const REQUIRED = [
  'schema_version',
  'kind',
  'tip_sha',
  'fail_evidence_paths',
  'write_scope',
  'allowed_decisions',
  'fail_class',
  'strike_count',
  'lock_or_interface_cite',
  'notes_zh',
];

const ALLOWED_DECISIONS = new Set(['reject', 'rebind_scope', 'escalate']);

/**
 * Extract first fenced ```json block or parse whole text.
 * @param {string} text
 * @returns {unknown}
 */
export function extractJsonPacket(text) {
  const body = String(text || '');
  const m = body.match(/```json\s*([\s\S]*?)```/i);
  if (m) return JSON.parse(m[1]);
  return JSON.parse(body);
}

/**
 * @param {unknown} packet
 * @returns {{ ok: true, packet: object } | { ok: false, errors: string[] }}
 */
export function validateWakePacket(packet) {
  const errors = [];
  if (!packet || typeof packet !== 'object' || Array.isArray(packet)) {
    return { ok: false, errors: ['packet must be an object'] };
  }
  const p = /** @type {Record<string, unknown>} */ (packet);
  for (const key of REQUIRED) {
    if (!(key in p) || p[key] === undefined || p[key] === '') {
      errors.push(`missing required field: ${key}`);
    }
  }
  if (p.schema_version !== '1.0') {
    errors.push('schema_version must be "1.0"');
  }
  if (p.kind !== 'junior_exception_wake') {
    errors.push('kind must be "junior_exception_wake"');
  }
  if (typeof p.tip_sha === 'string' && !/^[0-9a-f]{40}$/i.test(p.tip_sha)) {
    errors.push('tip_sha must be 40-hex');
  }
  if (!Array.isArray(p.fail_evidence_paths)) {
    errors.push('fail_evidence_paths must be an array');
  }
  if (!Array.isArray(p.write_scope)) {
    errors.push('write_scope must be an array');
  }
  if (!Array.isArray(p.allowed_decisions)) {
    errors.push('allowed_decisions must be an array');
  } else {
    for (const d of p.allowed_decisions) {
      if (!ALLOWED_DECISIONS.has(d)) {
        errors.push(`allowed_decisions contains invalid value: ${d}`);
      }
    }
    const set = new Set(p.allowed_decisions);
    for (const need of ALLOWED_DECISIONS) {
      if (!set.has(need)) {
        errors.push(`allowed_decisions must include ${need}`);
      }
    }
  }
  if (typeof p.strike_count !== 'number' || !Number.isInteger(p.strike_count) || p.strike_count < 1) {
    errors.push('strike_count must be an integer >= 1');
  }
  if (p.lock_or_interface_cite !== null && typeof p.lock_or_interface_cite !== 'string') {
    errors.push('lock_or_interface_cite must be string or null');
  }
  if (typeof p.notes_zh !== 'string') {
    errors.push('notes_zh must be a string');
  }
  if (errors.length) return { ok: false, errors };
  return { ok: true, packet: p };
}

/**
 * Cross-lane rule: if write_scope spans multiple top-level roots, require cite.
 * @param {object} packet
 * @returns {{ ok: true } | { ok: false, errors: string[] }}
 */
export function validateCrossLaneCite(packet) {
  const scope = Array.isArray(packet.write_scope) ? packet.write_scope : [];
  const roots = new Set(
    scope.map((p) => String(p).split(/[\\/]/)[0]).filter(Boolean)
  );
  if (roots.size <= 1) return { ok: true };
  if (packet.lock_or_interface_cite === null || packet.lock_or_interface_cite === '') {
    return {
      ok: false,
      errors: ['cross-lane write_scope requires lock_or_interface_cite; else escalate'],
    };
  }
  return { ok: true };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const fs = await import('node:fs');
  const raw = fs.readFileSync(process.argv[2] || '/dev/stdin', 'utf8');
  let packet;
  try {
    packet = extractJsonPacket(raw);
  } catch (e) {
    process.stdout.write(JSON.stringify({ ok: false, errors: [String(e.message || e)] }) + '\n');
    process.exit(1);
  }
  const result = validateWakePacket(packet);
  if (!result.ok) {
    process.stdout.write(JSON.stringify(result) + '\n');
    process.exit(1);
  }
  const cross = validateCrossLaneCite(result.packet);
  if (!cross.ok) {
    process.stdout.write(JSON.stringify(cross) + '\n');
    process.exit(1);
  }
  process.stdout.write(JSON.stringify({ ok: true, packet: result.packet }) + '\n');
}
