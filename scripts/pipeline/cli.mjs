#!/usr/bin/env node
/**
 * CLI entry for zero-hop parsers (D-047).
 * Usage: node scripts/pipeline/cli.mjs <command> [args...]
 */
import { readFileSync } from 'node:fs';
import { detectPublish } from './detect-publish.mjs';
import { parseLatestVerdict, parseVerdictFromBody } from './parse-verdict.mjs';
import { extractMergeReady } from './extract-merge-ready.mjs';
import {
  extractJsonPacket,
  validateWakePacket,
  validateCrossLaneCite,
} from './validate-wake-packet.mjs';
import {
  failClassHash,
  failClassLabel,
  countFailClassStrikes,
  nextStrikeLabel,
} from './fail-class.mjs';
import {
  hopKey,
  evaluateIdempotency,
  claimMarker,
  doneMarker,
} from './idempotency.mjs';
import { candidateBranchName, isCandidateBranch } from './candidate-branch.mjs';
import { parseChiefPage } from './parse-chief-page.mjs';

function readInput() {
  const path = process.argv[3];
  if (!path || path === '-') return readFileSync(0, 'utf8');
  return readFileSync(path, 'utf8');
}

function out(obj) {
  process.stdout.write(JSON.stringify(obj) + '\n');
}

const cmd = process.argv[2];
try {
  switch (cmd) {
    case 'detect-publish':
      out(detectPublish(readInput()));
      break;
    case 'parse-verdict': {
      const raw = readInput();
      try {
        out({ verdict: parseLatestVerdict(JSON.parse(raw)) });
      } catch {
        out({ verdict: parseVerdictFromBody(raw) });
      }
      break;
    }
    case 'merge-ready':
      out({ merge_ready: extractMergeReady(readInput()) });
      break;
    case 'validate-wake': {
      const packet = extractJsonPacket(readInput());
      const v = validateWakePacket(packet);
      if (!v.ok) {
        out(v);
        process.exit(1);
      }
      const c = validateCrossLaneCite(v.packet);
      if (!c.ok) {
        out(c);
        process.exit(1);
      }
      out({ ok: true, packet: v.packet });
      break;
    }
    case 'fail-class-hash': {
      const fp = process.argv.slice(3).join(' ');
      const hash = failClassHash(fp);
      out({ hash, label: failClassLabel(hash) });
      break;
    }
    case 'fail-class-count':
      out(countFailClassStrikes(JSON.parse(readInput())));
      break;
    case 'next-strike': {
      const hash = process.argv[3];
      const cur = Number(process.argv[4] || '1');
      out({ label: nextStrikeLabel(hash, cur) });
      break;
    }
    case 'hop-key':
      out({ key: hopKey(JSON.parse(readInput())) });
      break;
    case 'idempotency':
      out(evaluateIdempotency(JSON.parse(readInput())));
      break;
    case 'claim-marker':
      out({ body: claimMarker(process.argv[3]) });
      break;
    case 'done-marker':
      out({ body: doneMarker(process.argv[3]) });
      break;
    case 'candidate-branch':
      out({ branch: candidateBranchName(process.argv[3] || '') });
      break;
    case 'is-candidate':
      out({ ok: isCandidateBranch(process.argv[3] || '') });
      break;
    case 'parse-chief-page':
      out(parseChiefPage(readInput()));
      break;
    default:
      console.error(
        'commands: detect-publish|parse-verdict|merge-ready|validate-wake|fail-class-hash|fail-class-count|next-strike|hop-key|idempotency|claim-marker|done-marker|candidate-branch|is-candidate|parse-chief-page'
      );
      process.exit(2);
  }
} catch (e) {
  console.error(String(e && e.stack ? e.stack : e));
  process.exit(1);
}
