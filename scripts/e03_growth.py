#!/usr/bin/env python3
"""E03 codebase growth snapshots (stdlib only).

Usage:  UPSTREAM=/path/to/photocraft python3 scripts/e03_growth.py [UPSTREAM] [--pin SHA]
Writes: data/E03_growth.csv, data/E03_growth_crates.csv

Snapshots = the last FIRST-PARENT commit of `main` (by committer time, UTC) in each ISO week,
plus the last first-parent commit of each UTC day for the first 14 days, plus the pin itself.
Per snapshot (from `git ls-tree -r -l` + blob contents via `git cat-file --batch`):
  rust_files      count of *.rs paths
  rust_loc        non-blank lines across *.rs files
  test_attrs      lines matching ^\\s*#\\[test\\]   (plain #[test] only)
  cfg_test_attrs  lines matching ^\\s*#\\[cfg\\(test\\)\\]
  crates          Cargo.toml files that contain a [package] table (workspace member packages)
  docs_md_top     docs/*.md (direct children); docs_md_all docs/**/*.md
  agents_md_bytes/lines  size of root AGENTS.md (blank if absent)
Crate LOC groups: crates/<x>, apps/<x>, else the top-level directory (xtask, tests, ...).
"""
import collections
import csv
import datetime as dt
import os
import re
import subprocess
import sys

PIN = "74330157cb601573ae4523a95bb9132822fc3918"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data")
args = sys.argv[1:]
if "--pin" in args:
    i = args.index("--pin"); PIN = args[i + 1]; del args[i:i + 2]
UP = args[0] if args else os.environ.get("UPSTREAM")
if not UP:
    sys.exit("give upstream clone path as argument or env UPSTREAM")


def git(*a):
    return subprocess.run(["git", "-C", UP] + list(a), capture_output=True, text=True, errors="replace",
                          check=True).stdout


fp = []
for line in git("rev-list", "--first-parent", "--format=%H %ct", PIN).splitlines():
    if line.startswith("commit "):
        continue
    s, t = line.split()
    fp.append((int(t), s))
fp.sort()
lastweek, lastday = {}, {}
for t, s in fp:
    d = dt.datetime.fromtimestamp(t, dt.timezone.utc).date()
    y, w, _ = d.isocalendar()
    lastweek[f"{y}-W{w:02d}"] = (t, s)
    lastday[d.isoformat()] = (t, s)
d0 = dt.datetime.fromtimestamp(fp[0][0], dt.timezone.utc).date()
snaps = {}
for k, v in lastweek.items():
    snaps.setdefault(v[1], (v[0], set()))[1].add("week-end " + k)
for k, v in lastday.items():
    if (dt.date.fromisoformat(k) - d0).days < 14:
        snaps.setdefault(v[1], (v[0], set()))[1].add("day-end " + k)
snaps.setdefault(PIN, (int(git("log", "-1", "--format=%ct", PIN)), set()))[1].add("pin")

cat = subprocess.Popen(["git", "-C", UP, "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
cache = {}
T1 = re.compile(rb"^\s*#\[test\]", re.M)
T2 = re.compile(rb"^\s*#\[cfg\(test\)\]", re.M)


def blob(sha):
    cat.stdin.write(sha.encode() + b"\n"); cat.stdin.flush()
    hdr = cat.stdout.readline().split()
    n = int(hdr[2])
    data = cat.stdout.read(n); cat.stdout.read(1)
    return data


def rs_stats(sha):
    if sha not in cache:
        b = blob(sha)
        cache[sha] = (sum(1 for l in b.split(b"\n") if l.strip()), len(T1.findall(b)), len(T2.findall(b)))
    return cache[sha]


def group(path):
    p = path.split("/")
    if p[0] in ("crates", "apps") and len(p) > 2:
        return p[0] + "/" + p[1]
    return p[0] if len(p) > 1 else "(root)"


rows, crow = [], []
allgroups = set()
gdata = {}
for sha, (t, lab) in sorted(snaps.items(), key=lambda kv: kv[1][0]):
    rf = loc = ta = tc = crates = dtop = dall = 0
    am_b = am_l = ""
    g = collections.Counter()
    for line in git("ls-tree", "-r", "-l", sha).splitlines():
        meta, path = line.split("\t", 1)
        mode, typ, bsha, size = meta.split()
        if typ != "blob":
            continue
        if path.endswith(".rs"):
            l, a, b = rs_stats(bsha)
            rf += 1; loc += l; ta += a; tc += b; g[group(path)] += l
        elif path.endswith("Cargo.toml"):
            if re.search(rb"^\[package\]", blob(bsha), re.M):
                crates += 1
        if re.match(r"^docs/[^/]+\.md$", path):
            dtop += 1
        if path.startswith("docs/") and path.endswith(".md"):
            dall += 1
        if path == "AGENTS.md":
            b = blob(bsha); am_b = len(b); am_l = b.count(b"\n")
    when = dt.datetime.fromtimestamp(t, dt.timezone.utc).isoformat(timespec="minutes")
    rows.append([" | ".join(sorted(lab)), sha[:10], when, rf, loc, ta, tc, crates, dtop, dall, am_b, am_l])
    gdata[sha] = (when, g)
    allgroups |= set(g)
cat.stdin.close(); cat.wait()
with open(os.path.join(OUT, "E03_growth.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["snapshot", "commit", "commit_time_utc", "rust_files", "rust_loc_nonblank", "test_attrs",
                "cfg_test_attrs", "packages_cargo_toml", "docs_md_top", "docs_md_all", "agents_md_bytes",
                "agents_md_lines"])
    w.writerows(rows)
last = gdata[PIN][1]
order = sorted(allgroups, key=lambda x: -last.get(x, 0))
with open(os.path.join(OUT, "E03_growth_crates.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["commit", "commit_time_utc"] + order)
    for sha, (t, lab) in sorted(snaps.items(), key=lambda kv: kv[1][0]):
        when, g = gdata[sha]
        w.writerow([sha[:10], when] + [g.get(x, 0) for x in order])
for r in rows:
    print(r)
