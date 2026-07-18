#!/usr/bin/env node
export function assertRollbackTarget({ knownGoodDigest, requestedDigest, firstReleaseDecision }) {
  if (!knownGoodDigest && !firstReleaseDecision) {
    return { allow: false, reason: 'no_known_good_or_first_release_decision' };
  }
  if (knownGoodDigest && requestedDigest && knownGoodDigest !== requestedDigest) {
    return { allow: false, reason: 'digest_mismatch' };
  }
  return { allow: true };
}
