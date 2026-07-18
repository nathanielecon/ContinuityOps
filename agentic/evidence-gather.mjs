/** Collect a remediation evidence pack (read-only). */
export function gatherEvidence({ alertId, candidateSha, paths }) {
  if (!alertId || !/^[0-9a-f]{40}$/.test(candidateSha)) {
    throw new Error('evidence_gather_invalid');
  }
  return {
    alert_id: alertId,
    candidate_sha: candidateSha,
    paths: paths ?? [],
    mutation: false,
    collected_at: new Date().toISOString()
  };
}
