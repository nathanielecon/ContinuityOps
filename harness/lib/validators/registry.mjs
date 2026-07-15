// Allowlisted validator registry. Validator IDs map to pinned implementations;
// there is no path for a task to supply an arbitrary shell command. Unknown
// IDs fail closed (PLAN.md P0-T03 acceptance: "Unknown validator IDs fail
// closed"). Every validator is check-only and must not mutate the repository.

const REGISTRY = new Map();

/**
 * Register a pinned validator.
 * @param id       stable allowlisted identifier
 * @param impl     async ({repoRoot, task}) => { id, ok, findings: [] }
 * @param meta     { mutates: false } — mutating validators are rejected
 */
export function register(id, impl, meta = {}) {
  if (REGISTRY.has(id)) throw new Error(`validator ${id} already registered`);
  if (meta.mutates) throw new Error(`validator ${id} declares mutation; check-only validators required`);
  REGISTRY.set(id, { id, impl, meta });
}

export function isRegistered(id) {
  return REGISTRY.has(id);
}

export function listValidators() {
  return [...REGISTRY.keys()].sort();
}

/**
 * Run one validator by ID. Fails closed on unknown IDs.
 * Never throws for a validator "fail" — that is a normal result object.
 */
export async function runValidator(id, ctx) {
  const entry = REGISTRY.get(id);
  if (!entry) {
    return { id, ok: false, fail_closed: true, findings: [`unknown validator id '${id}' — rejected`] };
  }
  try {
    const result = await entry.impl(ctx);
    return { id, ok: !!result.ok, findings: result.findings || [] };
  } catch (err) {
    return { id, ok: false, findings: [`validator '${id}' threw: ${err.message}`] };
  }
}

/** Run a list of validator IDs; overall ok only if every one passes. */
export async function runAll(ids, ctx) {
  const results = [];
  for (const id of ids) results.push(await runValidator(id, ctx));
  return { ok: results.every((r) => r.ok), results };
}
