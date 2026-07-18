#!/usr/bin/env node
/**
 * Fail if this process appears to be a PR job with AWS credentials configured.
 * Used by terraform-pr.yml to keep untrusted PRs credential-free.
 */
const awsKeys = [
  'AWS_ACCESS_KEY_ID',
  'AWS_SECRET_ACCESS_KEY',
  'AWS_SESSION_TOKEN',
  'AWS_SECURITY_TOKEN'
];

const present = awsKeys.filter((k) => process.env[k] && String(process.env[k]).trim() !== '');
if (present.length > 0) {
  console.error(`PR readonly assertion failed: found ${present.join(', ')}`);
  process.exit(1);
}

const eventName = process.env.GITHUB_EVENT_NAME || '';
if (eventName === 'pull_request' && process.env.AWS_ROLE_ARN) {
  console.error('PR readonly assertion failed: AWS_ROLE_ARN set on pull_request');
  process.exit(1);
}

console.log(JSON.stringify({
  ok: true,
  check: 'assert-pr-readonly',
  event_name: eventName || 'local',
  aws_keys_present: present
}, null, 2));
