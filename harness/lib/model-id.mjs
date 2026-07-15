// Shared model-id honesty check. An "aspirational" id claims an engine this
// environment cannot actually invoke (Codex/GPT-5/Grok). Such an id is only
// acceptable when it carries a DELIMITED simulated/planned marker (e.g.
// "-sim", "_planned", "-not-run") — never as an incidental substring.

const ASPIRATIONAL = [/codex/i, /gpt-?5/i, /grok/i];
const MARKER = /[-_](sim|simulated|planned|not-?run)(?:$|[-_])/i;

export function isAspirationalModelId(id) {
  if (!id) return false;
  return ASPIRATIONAL.some((re) => re.test(id)) && !MARKER.test(id);
}
