export function recordModelRoute({ provider, model, mode, role }) {
  if (!provider || !model || !mode || !role) throw new Error('actual model route requires provider, model, mode, and role');
  return { provider, model, mode, role, recorded_at: new Date().toISOString() };
}
