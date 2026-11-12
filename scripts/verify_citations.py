#!/usr/bin/env python3
"""Verify git citations in research markdown against the upstream clone.

Usage: verify_citations.py <upstream-clone> <file-or-dir> [...]

Checks, for every markdown file given:
  1. `<sha>` tokens (9-40 hex chars, inside backticks or bare)   -> object exists
  2. `<sha>:<path>[:<line>[-<line>]]`                             -> path exists at that
     commit and the line number is within the file
  3. `HEAD:<path>[:<line>]`                                       -> same, against PIN
  4. `refs/pull/<N>/head`                                         -> ref exists

Exit status 1 if anything fails. Prints a per-file summary. Does not judge whether
the cited content supports the claim - only that the citation resolves.
"""
import os
import re
import subprocess
import sys
from functools import lru_cache

PIN = "74330157cb601573ae4523a95bb9132822fc3918"
SHA_RE = re.compile(r"(?<![0-9A-Za-z_/.-])([0-9a-f]{9,40})(?![0-9A-Za-z_])")
PATH_RE = re.compile(
    r"(?<![0-9A-Za-z_/.-])([0-9a-f]{9,40}|HEAD):([A-Za-z0-9_.][A-Za-z0-9_./@+-]*)(?::(\d+))?"
)
PULL_RE = re.compile(r"refs/pull/(\d+)/head")


def git(up, *args):
    return subprocess.run(["git", "-C", up, *args], capture_output=True, text=True)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    up = sys.argv[1]
    files = []
    for a in sys.argv[2:]:
        if os.path.isdir(a):
            for root, _, names in os.walk(a):
                files += [os.path.join(root, n) for n in sorted(names) if n.endswith(".md")]
        else:
            files.append(a)

    @lru_cache(maxsize=None)
    def obj_ok(sha):
        return git(up, "cat-file", "-e", sha + "^{object}").returncode == 0

    @lru_cache(maxsize=None)
    def blob_lines(rev, path):
        r = git(up, "cat-file", "-t", f"{rev}:{path}")
        if r.returncode != 0:
            return None
        if r.stdout.strip() == "tree":
            return -1
        out = subprocess.run(["git", "-C", up, "show", f"{rev}:{path}"], capture_output=True)
        return out.stdout.count(b"\n") + 1

    @lru_cache(maxsize=None)
    def ref_ok(ref):
        return git(up, "rev-parse", "--verify", "-q", ref).returncode == 0

    total_bad = 0
    for f in files:
        text = open(f, encoding="utf-8", errors="replace").read()
        bad, n = [], 0
        seen = set()
        for i, line in enumerate(text.splitlines(), 1):
            for m in PATH_RE.finditer(line):
                rev, path, ln = m.group(1), m.group(2).rstrip(".,;)"), m.group(3)
                key = ("p", rev, path, ln)
                if key in seen:
                    continue
                seen.add(key)
                n += 1
                real = PIN if rev == "HEAD" else rev
                if rev != "HEAD" and not obj_ok(real):
                    bad.append((i, f"unknown object {rev}"))
                    continue
                cnt = blob_lines(real, path)
                if cnt is None:
                    # tolerate trailing prose glued to the path (e.g. sha:word)
                    if "/" in path or "." in path:
                        bad.append((i, f"no such path {rev}:{path}"))
                    continue
                if ln and cnt > 0 and int(ln) > cnt:
                    bad.append((i, f"line {ln} > {cnt} in {rev}:{path}"))
            for m in SHA_RE.finditer(line):
                sha = m.group(1)
                if not re.search(r"[a-f]", sha) or not re.search(r"\d", sha):
                    continue  # pure digits / pure letters: not a sha
                key = ("s", sha)
                if key in seen:
                    continue
                seen.add(key)
                n += 1
                if not obj_ok(sha):
                    bad.append((i, f"unknown object {sha}"))
            for m in PULL_RE.finditer(line):
                key = ("r", m.group(0))
                if key in seen:
                    continue
                seen.add(key)
                n += 1
                if not ref_ok(m.group(0)):
                    bad.append((i, f"missing ref {m.group(0)}"))
        print(f"{f}: {n} citations checked, {len(bad)} unresolved")
        for i, msg in bad:
            print(f"  L{i}: {msg}")
        total_bad += len(bad)
    return 1 if total_bad else 0


if __name__ == "__main__":
    sys.exit(main())
