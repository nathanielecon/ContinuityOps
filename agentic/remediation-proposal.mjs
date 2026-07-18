/** Build a remediation proposal that always requires human gate. */
export function proposeRemediation({ evidence, steps, destructive = false }) {
  if (!evidence?.candidate_sha) throw new Error('proposal_missing_evidence');
  return {
    evidence_ref: evidence,
    steps: steps ?? [],
    destructive,
    requires_human_gate: true,
    default_mutation_authority: false,
    status: 'awaiting_approval'
  };
}

export function detectPromptInjection(text) {
  const patterns = [
    /ignore (all|previous) instructions/i,
    /exfiltrate/i,
    /disable (the )?human gate/i,
    /apply without approval/i
  ];
  return patterns.some((p) => p.test(String(text ?? '')));
}

export function rejectForgedEvidence(evidence, expectedSha) {
  if (!evidence || evidence.candidate_sha !== expectedSha) {
    return { accept: false, reason: 'forged_or_stale_evidence' };
  }
  return { accept: true };
}
