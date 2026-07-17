import { assertBottleneckProfile } from '../validators/core.mjs';

export function createBottleneckDispatch({ sessionId, issueId, specialist, failedCheck }) {
  const profile = {
    session_id: sessionId,
    supervisor_session_id: sessionId,
    issue_id: issueId,
    specialist,
    failed_check: failedCheck,
    purpose: 'diagnostic_handoff',
    can_write: false,
    can_expand_authority: false,
    allowed_outputs: ['诊断摘要', '复现步骤', '后续建议']
  };
  assertBottleneckProfile(profile);
  return profile;
}
