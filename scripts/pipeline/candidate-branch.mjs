/**
 * Candidate branch naming convention (D-047).
 * Intermediate fixer landings go to candidate/portfolio-<7sha>;
 * main only after fresh council pass.
 */

/**
 * @param {string} sha full or short SHA
 * @returns {string}
 */
export function candidateBranchName(sha) {
  const short = String(sha || '')
    .replace(/[^0-9a-f]/gi, '')
    .slice(0, 7)
    .toLowerCase();
  if (short.length < 7) {
    throw new Error('candidateBranchName requires at least 7 hex chars');
  }
  return `candidate/portfolio-${short}`;
}

/**
 * @param {string} branch
 * @returns {boolean}
 */
export function isCandidateBranch(branch) {
  return /^candidate\/portfolio-[0-9a-f]{7}$/i.test(String(branch || ''));
}

/**
 * Whether a merge target is allowed for a given hop.
 * @param {'candidate' | 'main'} hopTarget
 * @param {string} branch
 */
export function assertMergeTarget(hopTarget, branch) {
  if (hopTarget === 'main') {
    if (branch !== 'main') {
      throw new Error(`fresh-pass merge target must be main, got ${branch}`);
    }
    return true;
  }
  if (hopTarget === 'candidate') {
    if (!isCandidateBranch(branch) && branch !== 'main') {
      // creating candidate from main tip is ok; landing target must be candidate
      throw new Error(`candidate hop requires candidate/* branch, got ${branch}`);
    }
    return true;
  }
  throw new Error(`unknown hopTarget ${hopTarget}`);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const sha = process.argv[2] || '';
  process.stdout.write(JSON.stringify({ branch: candidateBranchName(sha) }) + '\n');
}
