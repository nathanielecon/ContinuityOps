#!/usr/bin/env node
/**
 * Fail when the pinned EKS cluster version has left AWS standard support.
 *
 * Why this exists (BF-2026-029): the lab was pinned to Kubernetes 1.32, which
 * left EKS standard support in March 2026. Extended support bills
 * $0.60/cluster/hour instead of $0.10 — a 6x multiplier, ~$438/mo instead of
 * ~$73. Nothing in the repository could detect this. `BF-2026-012` bumped
 * 1.29 -> 1.32 to clear an apply failure and walked straight into it, and the
 * cost model in operations/finops kept assuming $0.10.
 *
 * Teardown discipline does not help here: the multiplier applies for every hour
 * the cluster exists, however briefly. Only the version pin fixes it.
 *
 * Dates below are AWS's end-of-standard-support calendar. They are hardcoded
 * deliberately: this check must work in the credential-free PR job, which has no
 * AWS access to query the live support status.
 *
 * MAINTENANCE: entries from 1.34 onward follow AWS's published 14-months-from-GA
 * cadence but were not confirmed against the AWS support calendar at authoring
 * time (docs.aws.amazon.com was unreachable). Verify before relying on them for
 * an upgrade decision, and extend the table as new versions ship.
 */

import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const EKS_MODULE = 'terraform/modules/eks/main.tf';

/** Kubernetes minor version -> end of EKS *standard* support (UTC date). */
const END_OF_STANDARD_SUPPORT = {
  '1.28': '2024-11-26',
  '1.29': '2025-03-23',
  '1.30': '2025-07-23',
  '1.31': '2025-11-26',
  '1.32': '2026-03-23',
  '1.33': '2026-07-23',
  '1.34': '2026-11-26',
  '1.35': '2027-03-23',
};

const EXTENDED_SUPPORT_HOURLY = 0.6;
const STANDARD_SUPPORT_HOURLY = 0.1;
const MULTIPLIER = Math.round(EXTENDED_SUPPORT_HOURLY / STANDARD_SUPPORT_HOURLY);

/** Warn this far ahead of end-of-standard-support so upgrades are never urgent. */
const WARN_WINDOW_DAYS = 60;

export function readPinnedVersion(source) {
  // Matches the `cluster_version` variable's default in the EKS module.
  const block = source.match(
    /variable\s+"cluster_version"\s*\{[^}]*default\s*=\s*"([^"]+)"/,
  );
  return block ? block[1] : null;
}

export function assessVersion(version, today = new Date()) {
  const endDate = END_OF_STANDARD_SUPPORT[version];

  if (!endDate) {
    return {
      version,
      known: false,
      inStandardSupport: null,
      note: `Version ${version} is not in the local support calendar. Update END_OF_STANDARD_SUPPORT in this script.`,
    };
  }

  const end = new Date(`${endDate}T00:00:00Z`);
  const inStandardSupport = today < end;
  const daysRemaining = Math.floor((end - today) / 86_400_000);

  return {
    version,
    known: true,
    endOfStandardSupport: endDate,
    inStandardSupport,
    daysRemaining,
    expiringSoon: inStandardSupport && daysRemaining <= WARN_WINDOW_DAYS,
    hourlyRate: inStandardSupport ? STANDARD_SUPPORT_HOURLY : EXTENDED_SUPPORT_HOURLY,
    monthlyEstimate: +(
      (inStandardSupport ? STANDARD_SUPPORT_HOURLY : EXTENDED_SUPPORT_HOURLY) * 730
    ).toFixed(2),
  };
}

/** Versions still in standard support today, cheapest-risk first. */
export function suggestVersions(today = new Date()) {
  return Object.entries(END_OF_STANDARD_SUPPORT)
    .filter(([, end]) => today < new Date(`${end}T00:00:00Z`))
    .sort((a, b) => a[1].localeCompare(b[1]))
    .map(([version, end]) => ({ version, endOfStandardSupport: end }));
}

function main() {
  const source = readFileSync(resolve(ROOT, EKS_MODULE), 'utf8');
  const version = readPinnedVersion(source);

  if (!version) {
    console.error(`FAIL: could not find cluster_version default in ${EKS_MODULE}`);
    process.exit(1);
  }

  const result = assessVersion(version);

  if (!result.known) {
    console.error(`FAIL: ${result.note}`);
    process.exit(1);
  }

  if (result.inStandardSupport) {
    console.log(
      `PASS: EKS ${version} is in standard support until ${result.endOfStandardSupport} ` +
        `($${STANDARD_SUPPORT_HOURLY}/cluster/hour, ~$${result.monthlyEstimate}/mo).`,
    );
    if (result.expiringSoon) {
      // Warn, don't fail: an upgrade should be planned work, not a red build on
      // an unrelated PR. The failure only lands once the cheap rate is gone.
      console.warn(
        `::warning::EKS ${version} leaves standard support in ${result.daysRemaining} days ` +
          `(${result.endOfStandardSupport}); the rate becomes $${EXTENDED_SUPPORT_HOURLY}/hr ` +
          `(~$${(EXTENDED_SUPPORT_HOURLY * 730).toFixed(0)}/mo). Plan the version bump now.`,
      );
    }
    return;
  }

  const options = suggestVersions()
    .map((o) => `${o.version} (standard until ${o.endOfStandardSupport})`)
    .join(', ');

  console.error(
    [
      `FAIL: EKS ${version} left standard support on ${result.endOfStandardSupport}.`,
      `It bills EXTENDED support at $${EXTENDED_SUPPORT_HOURLY}/cluster/hour`,
      `(~$${result.monthlyEstimate}/mo) — ${MULTIPLIER}x standard.`,
      '',
      `Fix: raise the cluster_version default in ${EKS_MODULE}.`,
      options ? `Still in standard support: ${options}` : 'Update the support calendar in this script.',
      '',
      'See BF-2026-029 in BREAK_FIX_LOG.md.',
    ].join('\n'),
  );
  process.exit(1);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
