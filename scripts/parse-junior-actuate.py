#!/usr/bin/env python3
"""Parse D-042 junior actuate intent markers from a comment body."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def parse_merge(text: str) -> dict:
    pr = re.search(r"(?m)^pr:\s*(\d+)\s*$", text)
    d037 = re.search(r"(?m)^d037_issue:\s*(\d+)\s*$", text)
    if not pr or not d037:
        raise SystemExit("merge intent requires numeric pr: and d037_issue:")
    return {"kind": "merge", "pr": int(pr.group(1)), "d037_issue": int(d037.group(1))}


def parse_dispatch(text: str) -> dict:
    target = re.search(r"(?m)^target_issue:\s*(\d+)\s*$", text)
    if not target:
        raise SystemExit("dispatch intent requires numeric target_issue:")
    m = re.search(r"<!--\s*continuityops-dispatch-v1\s*-->", text)
    rest = text[m.end() :] if m else text
    body = ""
    fm = re.search(r"```(?:text|markdown|md)?\n(.*?)```", rest, re.S)
    if fm and "@codex" in fm.group(1):
        body = fm.group(1).strip()
    else:
        ym = re.search(r"(?m)^body:\s*\|\s*\n((?:[ \t]+.*\n?)+)", rest)
        if ym:
            lines = []
            for line in ym.group(1).splitlines():
                if line.startswith("  "):
                    lines.append(line[2:])
                else:
                    lines.append(line.lstrip())
            candidate = "\n".join(lines).strip()
            if "@codex" in candidate:
                body = candidate
    if not body or "@codex" not in body:
        raise SystemExit("dispatch intent must include @codex body (fenced or body: |)")
    if re.search(r"ghp_|gho_|github_pat_|BEGIN (RSA |OPENSSH )?PRIVATE KEY", body, re.I):
        raise SystemExit("refused secret-like payload")
    return {"kind": "dispatch", "target_issue": int(target.group(1)), "body": body}


def latest_verdict(comments_json: str) -> str | None:
    comments = json.loads(comments_json)
    found = None
    for c in comments:
        if c.get("user", {}).get("login") != "chatgpt-codex-connector[bot]":
            continue
        body = c.get("body") or ""
        m = re.search(r'"verdict"\s*:\s*"(pass|fail)"', body)
        if m:
            found = m.group(1)
            continue
        if re.search(r"(?im)^\s*verdict\s*:\s*pass\b", body) or re.search(
            r"(?i)\bverdict\b[^\n]*\bpass\b", body
        ):
            found = "pass"
        elif re.search(r"(?im)^\s*verdict\s*:\s*fail\b", body) or re.search(
            r"(?i)\bverdict\b[^\n]*\bfail\b", body
        ):
            found = "fail"
    return found


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["intent", "verdict"])
    ap.add_argument("path")
    args = ap.parse_args()
    text = Path(args.path).read_text(encoding="utf-8")
    if args.mode == "verdict":
        v = latest_verdict(text)
        if not v:
            raise SystemExit("no bot verdict found")
        print(v)
        return
    if "<!-- continuityops-merge-v1" in text:
        print(json.dumps(parse_merge(text)))
    elif "<!-- continuityops-dispatch-v1" in text:
        print(json.dumps(parse_dispatch(text), ensure_ascii=False))
    else:
        raise SystemExit("no supported actuate marker")


if __name__ == "__main__":
    main()
