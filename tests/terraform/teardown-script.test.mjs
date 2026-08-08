import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, statSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const PATH = 'scripts/teardown/aws-cost-teardown.sh';
const src = readFileSync(resolve(ROOT, PATH), 'utf8');

// This file really deletes cloud resources. These tests guard the properties that
// keep it from being dangerous — they are cheap relative to the cost of getting
// any of them wrong (BF-2026-033).

test('teardown script is dry-run unless --apply is passed', () => {
  assert.match(src, /APPLY=0/);
  assert.match(src, /--apply.*APPLY=1|APPLY=1/s);
  // The dry-run branch must print rather than execute.
  assert.match(src, /\[dry-run\]/);
});

test('teardown refuses to remove the last CloudTrail trail', () => {
  // Deleting the duplicate must never leave the account with zero audit coverage,
  // e.g. if the surviving trail were renamed.
  assert.match(src, /TRAIL_KEEP.*NONE.*die|die.*only trail/s);
  assert.match(src, /project-a-lzlab-trail/);
});

test('teardown never touches irreversible or rebuild-critical resources', () => {
  // KMS deletion has a 7-30 day irreversible window; the S3 archive holds audit
  // data; ECR holds the digest-pinned image needed to rebuild Project C.
  const forbidden = [
    'schedule-key-deletion',
    'delete-alias',
    'delete-bucket',
    'rb s3://',
    'delete-repository',
    'delete-vpc',
  ];
  const found = forbidden.filter((cmd) => src.includes(cmd));
  assert.deepEqual(found, [], `teardown must not invoke: ${found}`);
});

test('target groups are resolved by name, not by load-balancer association', () => {
  // Once the ALB is deleted the association is gone, so an association-based
  // lookup silently orphans the target groups.
  assert.match(src, /describe-target-groups/);
  assert.match(src, /starts_with\(TargetGroupName/);
});

test('load balancer deletion is awaited before dependent cleanup', () => {
  // ENIs release asynchronously; deleting security groups too early just fails.
  assert.match(src, /wait load-balancers-deleted/);
  const lbIdx = src.indexOf('delete-load-balancer');
  const sgIdx = src.indexOf('delete-security-group');
  assert.ok(lbIdx > 0 && sgIdx > lbIdx, 'security-group deletion must come after the ALB');
});

test('service is drained before deletion', () => {
  const drain = src.indexOf('--desired-count 0');
  const del = src.indexOf('delete-service');
  assert.ok(drain > 0 && del > drain, 'desiredCount must reach 0 before delete-service');
  assert.match(src, /runningCount/);
});

test('script is executable', () => {
  const mode = statSync(resolve(ROOT, PATH)).mode;
  assert.ok(mode & 0o111, `${PATH} must be executable`);
});
