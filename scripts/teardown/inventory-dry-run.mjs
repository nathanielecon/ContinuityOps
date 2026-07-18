#!/usr/bin/env node
/** Teardown inventory dry-run — never destroys cloud resources. */
const inventory = {
  schema_version: '1.0',
  mode: 'dry_run',
  live_teardown_executed: false,
  resources: [
    { id: 'lab-asg-1', type: 'asg', action_if_approved: 'scale_to_zero' },
    { id: 'lab-ebs-orphan-1', type: 'ebs', action_if_approved: 'delete_snapshot_retain' }
  ],
  claim_level: 'L1',
  remaining_boundaries: ['No live teardown of cloud resources executed']
};
console.log(JSON.stringify(inventory, null, 2));
