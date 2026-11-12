#!/usr/bin/env python3
"""E03 quantitative git forensics for storytold/photocraft (stdlib only).

Usage:  UPSTREAM=/path/to/photocraft python3 scripts/e03_git_quant.py [UPSTREAM] [--pin SHA]
Writes: data/E03_*.csv (relative to the research repo root = parent of scripts/)
        and prints a short reconciliation report to stdout.

Everything is derived from `git log <PIN>` (all commits reachable from the pinned main),
`git rev-list --first-parent <PIN>`, refs/pull/*/head, refs/remotes/origin/*, and tags.
Read-only on the upstream clone.

Conventions (see evidence/E03-git-quant.md, "Method & caveats"):
- day/week buckets use the COMMITTER date converted to UTC; ISO weeks (YYYY-Www).
- hour-of-day uses the AUTHOR date, both in its own recorded tz offset ("local") and UTC.
- diffs: --no-renames numstat on non-merge commits only (merges have no numstat).
"""
import collections
import csv
import datetime as dt
import os
import re
import statistics
import subprocess
import sys

PIN_DEFAULT = "74330157cb601573ae4523a95bb9132822fc3918"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data")

args = [a for a in sys.argv[1:]]
PIN = PIN_DEFAULT
if "--pin" in args:
    i = args.index("--pin"); PIN = args[i + 1]; del args[i:i + 2]
UP = args[0] if args else os.environ.get("UPSTREAM")
if not UP:
    sys.exit("give upstream clone path as argument or env UPSTREAM")


def git(*a, inp=None):
    return subprocess.run(["git", "-C", UP] + list(a), input=inp, capture_output=True,
                          text=True, errors="replace", check=True).stdout


def wcsv(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def pct(xs, p):
    if not xs:
        return ""
    s = sorted(xs)
    k = max(0, min(len(s) - 1, int(-(-p * len(s) // 100)) - 1))  # nearest-rank
    return s[k]


def med(xs):
    return statistics.median(xs) if xs else ""


def isoweek(d):
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- load commits
FMT = "%x1e%H%x1f%P%x1f%an%x1f%ae%x1f%aI%x1f%cn%x1f%ce%x1f%cI%x1f%B%x1f"
raw = git("log", PIN, "--no-renames", "--numstat", "--format=" + FMT)
first_parent = set(git("rev-list", "--first-parent", PIN).split())
main_set = set(git("rev-list", PIN).split())

C = []  # list of dicts, git log order (newest first)
for rec in raw.split("\x1e")[1:]:
    parts = rec.split("\x1f")
    sha, par, an, ae, ai, cn, ce, ci, body = parts[:9]
    files = []
    for line in parts[9].splitlines():
        m = re.match(r"^(\d+|-)\t(\d+|-)\t(.*)$", line)
        if m:
            a = 0 if m.group(1) == "-" else int(m.group(1))
            d = 0 if m.group(2) == "-" else int(m.group(2))
            files.append((a, d, m.group(3)))
    ad = dt.datetime.fromisoformat(ai)
    cd = dt.datetime.fromisoformat(ci)
    C.append(dict(sha=sha, parents=par.split(), an=an, ae=ae.lower(), ad=ad, cn=cn, ce=ce.lower(),
                  cd=cd, body=body, subj=body.split("\n", 1)[0], files=files,
                  fp=sha in first_parent))
for c in C:
    c["merge"] = len(c["parents"]) > 1
    cu = c["cd"].astimezone(dt.timezone.utc)
    c["day"] = cu.date().isoformat()
    c["week"] = isoweek(cu.date())
    au = c["ad"].astimezone(dt.timezone.utc)
    c["aday"] = au.date().isoformat()
assert len(C) == len(main_set), (len(C), len(main_set))
NONMERGE = [c for c in C if not c["merge"]]

# ---------------------------------------------------------------- aliasing
# union names that share an e-mail (GitHub noreply addresses keyed by numeric user id)
par = {}


def find(x):
    while par.setdefault(x, x) != x:
        par[x] = par[par[x]]
        x = par[x]
    return x


name_cnt = collections.Counter(c["an"] for c in C)
SHARED_EMAILS = {"noreply@anthropic.com", "noreply@github.com", "noreply@openai.com"}
for c in C:
    e = c["ae"]
    m = re.match(r"(\d+)\+.*@users\.noreply\.github\.com$", e)
    key = "E:" + (m.group(1) if m else e)
    if e in SHARED_EMAILS or e.endswith(".invalid") or e.endswith(".local"):
        key = "E:" + e + ":" + c["an"]
    par[find("N:" + c["an"])] = find(key)
groups = collections.defaultdict(set)
for k in list(par):
    if k.startswith("N:"):
        groups[find(k)].add(k[2:])
CANON = {}
alias_rows = []
for g in groups.values():
    canon = sorted(g, key=lambda n: (-name_cnt[n], n))[0]
    for n in g:
        CANON[n] = canon
    if len(g) > 1:
        alias_rows.append((canon, "; ".join(sorted(g - {canon})), sum(name_cnt[n] for n in g)))
alias_rows.sort(key=lambda r: -r[2])
wcsv("E03_alias_map.csv", ["canonical_name", "merged_aliases", "commits_total"], alias_rows)
for c in C:
    c["auth"] = CANON[c["an"]]

# ---------------------------------------------------------------- attribution
CO_RE = re.compile(r"^[\s*>-]*co-authored-by:\s*(.*?)\s*(<([^>]*)>)?\s*$", re.I | re.M)
AI_NAME_RE = re.compile(r"^(Claude\b.*|GPT-?\d.*|(OpenAI )?Codex.*|Cursor( Agent)?|Copilot|Codebuff|"
                        r"Devin|DeepSeek.*|Qwen.*|Gemini.*|Grok.*)$", re.I)
AI_EMAIL_RE = re.compile(r"(@anthropic\.com|@openai\.com|@cursor\.com|@codebuff\.com|@qwen\.ai|"
                         r"@deepseek\.com|\+copilot@users\.noreply\.github\.com|"
                         r"\+devin-ai-integration\[bot\]@)", re.I)
REVIEW_BOT_RE = re.compile(r"coderabbit", re.I)
SESS_RE = {k: re.compile(r"^\s*" + k + r":\s*(.*)$", re.I | re.M)
           for k in ("Claude-Session", "Copilot-Session", "Model-Effort")}
GEN_RE = re.compile(r"generated with \[?(Claude Code|Codebuff|Codex)", re.I)


def ai_author(c):
    return (c["ae"].endswith("@anthropic.com") or c["ae"].endswith("@openai.com")
            or re.match(r"^(Claude|Claude Opus.*|Codex)$", c["an"]) is not None)


for c in C:
    ais, humans, bots = [], [], []
    for m in CO_RE.finditer(c["body"]):
        name, email = m.group(1).strip(), (m.group(3) or "").strip()
        if AI_NAME_RE.match(name) or AI_EMAIL_RE.search(email):
            if name not in ais:
                ais.append(name)
        elif REVIEW_BOT_RE.search(name):
            bots.append(name)
        else:
            humans.append(name)
    c["ai_co"] = ais
    c["human_co"] = humans
    c["bot_co"] = bots
    c["ai_auth"] = ai_author(c)
    c["sess"] = {k: [v.strip() for v in r.findall(c["body"])] for k, r in SESS_RE.items()}
    c["gen"] = bool(GEN_RE.search(c["body"]))
    c["ai_any"] = bool(ais or c["ai_auth"] or any(c["sess"].values()) or c["gen"])
    # trailer-block-only variant: last paragraph of the message
    last_par = c["body"].strip().split("\n\n")[-1]
    c["ai_co_trailer"] = any(AI_NAME_RE.match(m.group(1).strip()) or AI_EMAIL_RE.search(m.group(3) or "")
                             for m in CO_RE.finditer(last_par))

weeks = sorted({c["week"] for c in C})
days = sorted({c["day"] for c in C})

# ---- weekly attribution (non-merge)
rows = []
for w in weeks:
    cs = [c for c in NONMERGE if c["week"] == w]
    rows.append([w, len(cs), sum(bool(c["ai_co"]) for c in cs), sum(c["ai_co_trailer"] for c in cs),
                 sum(c["ai_auth"] for c in cs),
                 sum(bool(c["sess"]["Claude-Session"]) for c in cs),
                 sum(bool(c["sess"]["Copilot-Session"]) for c in cs),
                 sum(bool(c["sess"]["Model-Effort"]) for c in cs),
                 sum(c["gen"] for c in cs), sum(c["ai_any"] for c in cs),
                 sum(not c["ai_any"] for c in cs),
                 sum(bool(c["human_co"]) for c in cs),
                 sum(c["fp"] for c in cs), sum(c["fp"] and c["ai_any"] for c in cs)])
H_ATTR = ["week", "nonmerge", "ai_coauthor_any_line", "ai_coauthor_in_last_paragraph", "ai_author_identity",
          "claude_session", "copilot_session", "model_effort", "generated_with_line", "any_ai_attribution",
          "no_ai_attribution", "human_coauthor", "nonmerge_first_parent", "nonmerge_first_parent_any_ai"]
tot = ["TOTAL"] + [sum(r[i] for r in rows) for i in range(1, len(H_ATTR))]
wcsv("E03_attr_weekly.csv", H_ATTR, rows + [tot])
ATTR_TOT = dict(zip(H_ATTR, tot))

# ---- per model string
mod = collections.defaultdict(lambda: dict(nm=0, allc=0, fp=0, first=None, last=None, wk=collections.Counter()))
for c in C:
    for s in c["ai_co"]:
        r = mod[s]
        r["allc"] += 1
        if not c["merge"]:
            r["nm"] += 1
            r["wk"][c["week"]] += 1
            r["fp"] += c["fp"]
        r["first"] = min(r["first"] or c["day"], c["day"])
        r["last"] = max(r["last"] or c["day"], c["day"])
mrows = sorted(mod.items(), key=lambda kv: -kv[1]["allc"])
wcsv("E03_attr_models_summary.csv",
     ["coauthor_string", "nonmerge_commits", "nonmerge_first_parent_commits", "all_commits_incl_merges",
      "first_day_utc", "last_day_utc"],
     [[k, v["nm"], v["fp"], v["allc"], v["first"], v["last"]] for k, v in mrows])
wcsv("E03_attr_models_weekly.csv", ["week"] + [k for k, _ in mrows],
     [[w] + [v["wk"][w] for _, v in mrows] for w in weeks])
# human co-authors & review bots (for context)
hc = collections.Counter(n for c in NONMERGE for n in set(c["human_co"]))
bc = collections.Counter(n for c in NONMERGE for n in set(c["bot_co"]))
wcsv("E03_coauthors_nonai_top.csv", ["coauthor_string", "kind", "nonmerge_commits"],
     [[n, "review-bot", k] for n, k in bc.most_common()] + [[n, "other", k] for n, k in hc.most_common(30)])
# ai author identity
aa = collections.Counter((c["an"], c["merge"]) for c in C if c["ai_auth"])
wcsv("E03_ai_author_identity.csv", ["author_name", "is_merge", "commits"],
     [[a, m, k] for (a, m), k in aa.most_common()])
# model effort values
me = collections.Counter(v for c in C for v in c["sess"]["Model-Effort"])
wcsv("E03_model_effort_values.csv", ["model_effort_value", "lines"], me.most_common())
sess_distinct = {k: len({v for c in C for v in c["sess"][k]}) for k in SESS_RE}

# ---- per human author share (top 25 by commits, non-merge, canonical names)
ac = collections.Counter(c["auth"] for c in NONMERGE if not c["ai_auth"])  # human identities only
arows = []
for a, n in ac.most_common(25):
    cs = [c for c in NONMERGE if c["auth"] == a]
    arows.append([a, n, sum(bool(c["ai_co"]) for c in cs), round(100 * sum(bool(c["ai_co"]) for c in cs) / n, 1),
                  sum(c["ai_any"] for c in cs), round(100 * sum(c["ai_any"] for c in cs) / n, 1),
                  collections.Counter(s for c in cs for s in c["ai_co"]).most_common(1)[0][0]
                  if any(c["ai_co"] for c in cs) else ""])
wcsv("E03_attr_by_author.csv", ["author_canonical", "nonmerge_commits", "with_ai_coauthor", "pct_ai_coauthor",
                                "with_any_ai_attr", "pct_any_ai_attr", "most_common_ai_string"], arows)

# ---------------------------------------------------------------- 1. commit counts
def count_rows(key, keys):
    out, cum = [], 0
    byk = collections.defaultdict(list)
    for c in C:
        byk[c[key]].append(c)
    akey = "aday" if key == "day" else None
    aby = collections.Counter(c["aday"] for c in C) if akey else None
    for k in keys:
        cs = byk.get(k, [])
        cum += len(cs)
        r = [k, len(cs), sum(c["fp"] for c in cs), sum(c["merge"] for c in cs),
             sum(not c["merge"] for c in cs), sum(c["fp"] and not c["merge"] for c in cs),
             len({c["auth"] for c in cs}), len({c["auth"] for c in cs if not c["merge"]}), cum]
        if aby is not None:
            r.append(aby.get(k, 0))
        out.append(r)
    return out


HC = ["bucket", "total", "first_parent", "merges", "non_merge", "first_parent_non_merge",
      "distinct_authors_all", "distinct_authors_nonmerge", "cumulative_total"]
alldays = sorted(set(days) | {c["aday"] for c in C})
d0, d1 = dt.date.fromisoformat(alldays[0]), dt.date.fromisoformat(alldays[-1])
daylist = [(d0 + dt.timedelta(i)).isoformat() for i in range((d1 - d0).days + 1)]
drows = count_rows("day", daylist)
wcsv("E03_commits_daily.csv", HC + ["total_by_author_date_utc"], drows)
wrows = count_rows("week", weeks)
wcsv("E03_commits_weekly.csv", HC, wrows)
assert sum(r[1] for r in drows) == len(C) == sum(r[1] for r in wrows)
assert sum(r[-1] for r in drows) == len(C)

# ---------------------------------------------------------------- 3. authors
first_seen = {}
for c in sorted(C, key=lambda c: c["cd"]):
    first_seen.setdefault(c["auth"], c["week"])
arows = []
cumauth = 0
for w in weeks:
    new = sum(1 for a, fw in first_seen.items() if fw == w)
    cumauth += new
    arows.append([w, len({c["auth"] for c in C if c["week"] == w}), new, cumauth])
wcsv("E03_authors_weekly.csv", ["week", "distinct_authors", "newcomers", "cumulative_authors"], arows)
NEWDAILY = collections.Counter()
fsd = {}
for c in sorted(C, key=lambda c: c["cd"]):
    fsd.setdefault(c["auth"], c["day"])
for a, d in fsd.items():
    NEWDAILY[d] += 1
cum = 0
nd = []
for d in daylist:
    cum += NEWDAILY[d]
    nd.append([d, NEWDAILY[d], cum])
wcsv("E03_newcomers_daily.csv", ["day", "newcomers", "cumulative_authors"], nd)
allc = collections.Counter(c["auth"] for c in C)
trow = []
for a, n in allc.most_common(40):
    cs = [c for c in C if c["auth"] == a]
    trow.append([a, n, sum(not c["merge"] for c in cs), sum(c["merge"] for c in cs),
                 sum(c["fp"] for c in cs), min(c["aday"] for c in cs), max(c["aday"] for c in cs),
                 len({c["aday"] for c in cs})])
wcsv("E03_authors_top40.csv", ["author_canonical", "commits", "non_merge", "merges", "first_parent",
                               "first_author_day_utc", "last_author_day_utc", "active_author_days"], trow)
# who merges
MPR = re.compile(r"^Merge pull request #(\d+) from ([^/\s]+)/(\S+)")
mg_c = collections.Counter((c["cn"], c["auth"]) for c in C if c["merge"])
wcsv("E03_merge_commit_committers.csv", ["committer_name", "author_canonical", "merge_commits"],
     [[a, b, k] for (a, b), k in mg_c.most_common(40)])
mpr_merger, mpr_owner = collections.Counter(), collections.Counter()
mpr_list = []
for c in C:
    m = MPR.match(c["subj"])
    if m:
        mpr_merger[c["auth"]] += 1
        mpr_owner[m.group(2)] += 1
        mpr_list.append((c, int(m.group(1)), m.group(2), m.group(3)))
wcsv("E03_mergepr_by_merger.csv", ["merger_author_canonical", "merge_pull_request_commits"], mpr_merger.most_common())
wcsv("E03_mergepr_by_source_owner.csv", ["source_owner", "merge_pull_request_commits"], mpr_owner.most_common())
fp_merge_kind = collections.Counter()
for c in C:
    if c["merge"]:
        fp_merge_kind[("first_parent" if c["fp"] else "side", "MergePR" if MPR.match(c["subj"]) else "other")] += 1

# ---------------------------------------------------------------- 4. PR flow
SQ = re.compile(r"\(#(\d+)\)\s*$")
NUM = re.compile(r"#(\d+)\b")
merged_sq, merged_mc, fp_other_merge_num = {}, {}, {}
pr_day = collections.defaultdict(lambda: [0, 0, 0])
for c in C:
    if not c["fp"]:
        continue
    m = MPR.match(c["subj"])
    if m:
        merged_mc[int(m.group(1))] = c
        pr_day[c["day"]][1] += 1
        continue
    m = SQ.search(c["subj"])
    if m and not c["merge"]:
        merged_sq[int(m.group(1))] = c
        pr_day[c["day"]][0] += 1
    elif m:
        fp_other_merge_num[int(m.group(1))] = c
side_sq = sum(1 for c in C if not c["fp"] and not c["merge"] and SQ.search(c["subj"]))
# squash commits made by GitHub (web-flow) that sit on side branches: PRs squash-merged into
# another PR/integration branch which later reached main (stacked PRs)
side_gh_sq = {int(SQ.search(c["subj"]).group(1)) for c in C
              if not c["fp"] and not c["merge"] and c["cn"] == "GitHub" and SQ.search(c["subj"])}
mentioned = set()
maxnum_day = collections.defaultdict(int)
for c in C:
    for n in NUM.findall(c["subj"]):
        n = int(n)
        if n < 100000:
            mentioned.add(n)
            if c["fp"]:
                maxnum_day[c["day"]] = max(maxnum_day[c["day"]], n)
# PR heads
heads = {}
for line in git("for-each-ref", "--format=%(objectname) %(refname)", "refs/pull").splitlines():
    sha, ref = line.split()
    m = re.match(r"refs/pull/(\d+)/head$", ref)
    if m:
        heads[int(m.group(1))] = sha
hdates = {}
hd_raw = git("log", "--no-walk", "--format=%H %cI", "--stdin", inp="\n".join(set(heads.values())) + "\n")
for line in hd_raw.splitlines():
    s, d = line.split()
    hdates[s] = dt.datetime.fromisoformat(d).astimezone(dt.timezone.utc).date().isoformat()
merged_nums = set(merged_sq) | set(merged_mc)
cat = collections.Counter()
for n, s in heads.items():
    anc = s in main_set
    cat[("ancestor" if anc else "not_ancestor") + "+" + ("number_in_fp_subject" if n in merged_nums else
         ("number_in_side_github_squash" if n in side_gh_sq else
          ("number_mentioned_elsewhere" if n in mentioned else "number_absent")))] += 1
maxhead_day = collections.defaultdict(int)
for n, s in heads.items():
    maxhead_day[hdates[s]] = max(maxhead_day[hdates[s]], n)
prrows, cm, ch = [], 0, 0
for d in daylist:
    sq, mc, _ = pr_day[d]
    cm = max(cm, maxnum_day.get(d, 0))
    ch = max(ch, maxhead_day.get(d, 0))
    prrows.append([d, sq, mc, sq + mc, maxnum_day.get(d, ""), cm, ch,
                   sum(1 for n, s in heads.items() if hdates[s] == d)])
wcsv("E03_pr_daily.csv", ["day_utc", "squash_prs_landed", "merge_commit_prs_landed", "prs_landed",
                          "max_hash_number_in_fp_subjects_that_day", "running_max_number_main",
                          "running_max_pr_head_number_by_head_commit_date", "pr_heads_with_head_commit_that_day"],
     prrows)
wcsv("E03_pr_heads_status.csv", ["category", "pr_heads"], sorted(cat.items()))
assert sum(cat.values()) == len(heads)
prw = collections.defaultdict(lambda: [0, 0])
for n, c in merged_sq.items():
    prw[c["week"]][0] += 1
for n, c in merged_mc.items():
    prw[c["week"]][1] += 1
wcsv("E03_pr_weekly.csv", ["week", "squash_prs", "merge_commit_prs", "pct_squash"],
     [[w, prw[w][0], prw[w][1], round(100 * prw[w][0] / max(1, sum(prw[w])), 1)] for w in weeks])
PR_STATS = dict(squash=len(merged_sq), mergecommit=len(merged_mc), union=len(merged_nums),
                overlap=len(set(merged_sq) & set(merged_mc)), side_sq=side_sq,
                side_gh_sq=len(side_gh_sq), side_gh_sq_not_fp=len(side_gh_sq - merged_nums),
                fp_other_merge_num=len(fp_other_merge_num), heads=len(heads),
                heads_max=max(heads), heads_min=min(heads), mentioned=len(mentioned),
                maxnum=max(n for n in mentioned), merged_not_in_heads=len(merged_nums - set(heads)))

# first-parent landing kinds per week
fpk = collections.defaultdict(collections.Counter)
for c in C:
    if not c["fp"]:
        continue
    gh = c["cn"] == "GitHub"
    if c["merge"]:
        k = "merge_pr_commit" if MPR.match(c["subj"]) else ("other_merge_github" if gh else "other_merge_direct")
    else:
        k = ("squash_github_with_pr_number" if SQ.search(c["subj"]) else "github_nonmerge_no_number") if gh else \
            ("direct_push_with_number" if SQ.search(c["subj"]) else "direct_push_no_number")
    fpk[c["week"]][k] += 1
FPK = ["squash_github_with_pr_number", "github_nonmerge_no_number", "merge_pr_commit", "other_merge_github",
       "other_merge_direct", "direct_push_with_number", "direct_push_no_number"]
fr = [[w] + [fpk[w][k] for k in FPK] for w in weeks]
fr.append(["TOTAL"] + [sum(r[i] for r in fr) for i in range(1, len(FPK) + 1)])
wcsv("E03_first_parent_kinds_weekly.csv", ["week"] + FPK, fr)
direct_authors = collections.Counter(c["auth"] for c in C if c["fp"] and c["cn"] != "GitHub")
wcsv("E03_first_parent_direct_by_author.csv", ["author_canonical", "first_parent_commits_not_committed_by_GitHub"],
     direct_authors.most_common())

# ---------------------------------------------------------------- 5. branch taxonomy
PREFIXES = [("claude/", r"^claude/"), ("codex/", r"^codex/"), ("copilot/", r"^copilot/"),
            ("cursor/", r"^cursor/"), ("community/", r"^community/"), ("fix/", r"^fix/"),
            ("fix-*", r"^fix-"), ("feat/", r"^feat/"), ("feature/", r"^feature/"),
            ("issue-*", r"^issues?[-_/]"), ("pr/", r"^pr/"), ("sonar*", r"^sonar"), ("jobs/", r"^jobs/"),
            ("land/", r"^land/"), ("batch/", r"^batch/"), ("integ-batch*", r"^integ-?batch"),
            ("integration*", r"^integrat"), ("perf/", r"^perf/"), ("chore/", r"^chore/"),
            ("ci/ or ci-*", r"^ci[/-]"), ("docs/", r"^docs?/"), ("test/", r"^tests?/"),
            ("refactor/", r"^refactor/"), ("security/", r"^security/"), ("release*", r"^release"),
            ("switch-*", r"^switch-"), ("dependabot/", r"^dependabot/"), ("main/master", r"^(main|master)$")]
PREFIXES = [(l, re.compile(r, re.I)) for l, r in PREFIXES]


def prefix(b):
    for l, r in PREFIXES:
        if r.search(b):
            return l
    return "other (with /)" if "/" in b else "other (no /)"


remote = [r[len("refs/remotes/origin/"):] for r in git("for-each-ref", "--format=%(refname)",
                                                        "refs/remotes/origin").split() if not r.endswith("/HEAD")]
INTO = re.compile(r"^Merge .* into ['\"]?([^\s'\"]+)['\"]?")
src_occ, src_dist, into_occ, into_dist = collections.Counter(), collections.defaultdict(set), \
    collections.Counter(), collections.defaultdict(set)
bweek = collections.defaultdict(collections.Counter)
for c, n, owner, br in mpr_list:
    p = prefix(br)
    src_occ[p] += 1
    src_dist[p].add(owner + "/" + br)
    bweek[c["week"]][p] += 1
for c in C:
    if c["merge"] and not MPR.match(c["subj"]):
        m = INTO.match(c["subj"])
        if m:
            b = m.group(1).rstrip(".,:")
            if b.startswith("origin/"):
                b = b[7:]
            p = prefix(b)
            into_occ[p] += 1
            into_dist[p].add(b)
rem_c = collections.Counter(prefix(b) for b in remote)
labels = [l for l, _ in PREFIXES] + ["other (with /)", "other (no /)"]
wcsv("E03_branch_prefixes.csv", ["prefix", "remote_branches", "mergepr_source_occurrences",
                                 "mergepr_source_distinct", "sync_merge_into_occurrences",
                                 "sync_merge_into_distinct_branches"],
     [[l, rem_c[l], src_occ[l], len(src_dist[l]), into_occ[l], len(into_dist[l])] for l in labels] +
     [["TOTAL", sum(rem_c.values()), sum(src_occ.values()), sum(len(v) for v in src_dist.values()),
       sum(into_occ.values()), sum(len(v) for v in into_dist.values())]])
oth = collections.Counter()
for b in remote:
    if prefix(b).startswith("other"):
        oth["remote:" + (b.split("/")[0] + "/" if "/" in b else re.sub(r"-.*", "-*", b))] += 1
for p, s in into_dist.items():
    if p.startswith("other"):
        for b in s:
            oth["into:" + (b.split("/")[0] + "/" if "/" in b else re.sub(r"-.*", "-*", b))] += 1
wcsv("E03_branch_other_prefixes.csv", ["source:prefix", "distinct_branches"], oth.most_common(60))
wcsv("E03_branch_prefixes_weekly_mergepr.csv", ["week"] + labels,
     [[w] + [bweek[w][l] for l in labels] for w in weeks])
# sync-merge "into" weekly by prefix
iweek = collections.defaultdict(collections.Counter)
for c in C:
    if c["merge"] and not MPR.match(c["subj"]):
        m = INTO.match(c["subj"])
        if m:
            b = m.group(1).rstrip(".,:")
            iweek[c["week"]][prefix(b[7:] if b.startswith("origin/") else b)] += 1
wcsv("E03_branch_prefixes_weekly_into.csv", ["week"] + labels, [[w] + [iweek[w][l] for l in labels] for w in weeks])
BR_STATS = dict(remote=len(remote), mpr=len(mpr_list), into_occ=sum(into_occ.values()),
                into_dist=sum(len(v) for v in into_dist.values()),
                merges_unparsed=sum(1 for c in C if c["merge"] and not MPR.match(c["subj"]) and not INTO.match(c["subj"])))

# ---------------------------------------------------------------- 6. change size + tests
TESTPATH = re.compile(r"(^|/)tests?/|_tests?\.rs$|(^|/)tests?\.rs$|(^|/)testkit/")
# added #[test] / #[cfg(test)] lines: stream -U0 patches
test_add = collections.Counter()
p = subprocess.Popen(["git", "-C", UP, "log", PIN, "--no-merges", "--no-renames", "-p", "-U0",
                      "--format=%x1eC %H", "--", "*.rs"], stdout=subprocess.PIPE, text=True, errors="replace")
cur = None
TA = re.compile(r"^\+\s*#\[(test|cfg\(test\))\]")
for line in p.stdout:
    if line.startswith("\x1eC "):
        cur = line[3:].strip()
    elif line.startswith("+") and not line.startswith("+++") and TA.match(line):
        test_add[cur] += 1
p.wait()
for c in NONMERGE:
    c["ins"] = sum(f[0] for f in c["files"])
    c["dels"] = sum(f[1] for f in c["files"])
    c["nf"] = len(c["files"])
    c["tpath"] = any(TESTPATH.search(f[2]) for f in c["files"])
    c["tattr"] = test_add[c["sha"]] > 0
    c["tests"] = c["tpath"] or c["tattr"]


def sizerow(cs):
    i = [c["ins"] for c in cs]; d = [c["dels"] for c in cs]; f = [c["nf"] for c in cs]
    return [len(cs), med(i), pct(i, 90), max(i, default=""), med(d), pct(d, 90), max(d, default=""),
            med(f), pct(f, 90), max(f, default=""), sum(i), sum(d)]


HS = ["n", "ins_median", "ins_p90", "ins_max", "del_median", "del_p90", "del_max", "files_median",
      "files_p90", "files_max", "ins_sum", "del_sum"]
srows = []
for label, sel in [("all_nonmerge", lambda c: True), ("ai_attributed", lambda c: c["ai_any"]),
                   ("no_ai_attribution", lambda c: not c["ai_any"]), ("first_parent_squash", lambda c: c["fp"]),
                   ("side_branch", lambda c: not c["fp"]),
                   ("first_parent_ai", lambda c: c["fp"] and c["ai_any"]),
                   ("first_parent_no_ai", lambda c: c["fp"] and not c["ai_any"])]:
    srows.append([label] + sizerow([c for c in NONMERGE if sel(c)]))
wcsv("E03_size_summary.csv", ["subset"] + HS, srows)
wr = []
for w in weeks:
    for label, sel in [("all", lambda c: True), ("ai", lambda c: c["ai_any"]), ("no_ai", lambda c: not c["ai_any"])]:
        wr.append([w, label] + sizerow([c for c in NONMERGE if c["week"] == w and sel(c)]))
wcsv("E03_size_weekly.csv", ["week", "subset"] + HS, wr)
big = sorted(NONMERGE, key=lambda c: -(c["ins"] + c["dels"]))[:30]
wcsv("E03_largest30.csv", ["sha", "day_utc", "author", "ins", "del", "files", "first_parent", "ai_any", "subject"],
     [[c["sha"][:10], c["day"], c["auth"], c["ins"], c["dels"], c["nf"], c["fp"], c["ai_any"], c["subj"][:100]]
      for c in big])
tw = []
for w in weeks:
    cs = [c for c in NONMERGE if c["week"] == w]
    n = len(cs)
    tw.append([w, n, sum(c["tpath"] for c in cs), sum(c["tattr"] for c in cs), sum(c["tests"] for c in cs),
               round(100 * sum(c["tests"] for c in cs) / max(1, n), 1),
               sum(c["tests"] for c in cs if c["ai_any"]), sum(c["ai_any"] for c in cs),
               sum(c["tests"] for c in cs if not c["ai_any"]), sum(not c["ai_any"] for c in cs)])
tw.append(["TOTAL"] + [sum(r[i] for r in tw) if i != 5 else "" for i in range(1, 10)])
tw[-1][5] = round(100 * tw[-1][4] / tw[-1][1], 1)
wcsv("E03_tests_weekly.csv", ["week", "nonmerge", "touch_test_path", "adds_test_attr", "touches_tests_either",
                              "pct_tests", "ai_with_tests", "ai_total", "noai_with_tests", "noai_total"], tw)

# ---------------------------------------------------------------- 8. corrective activity
CORR = [("revert", r"\brevert"), ("Revert \"", r"^Revert \""), ("fix main", r"fix(es|ed)? main\b"),
        ("main red/broken", r"main (is )?(red|broken)|red main|unbreak main|broken main"),
        ("flaky", r"flak"), ("fix ci", r"fix(es|ed)? (the )?ci\b|\bci fix"), ("hotfix", r"hot-?fix"),
        ("regression", r"regress"), ("follow-up", r"follow-?up"),
        ("fmt", r"\b(cargo )?fmt\b|rustfmt|format(ting)? fix"), ("clippy", r"clippy")]
CORR = [(l, re.compile(r, re.I)) for l, r in CORR]
CC = re.compile(r"^(feat|fix|docs|test|tests|perf|ci|chore|refactor|style|build|revert|i18n|security)"
                r"(\([^)]*\))?!?:", re.I)
cr, ccr = [], []
cct = collections.Counter()
for w in weeks:
    cs = [c for c in NONMERGE if c["week"] == w]
    cr.append([w, len(cs)] + [sum(bool(r.search(c["subj"])) for c in cs) for _, r in CORR])
    t = collections.Counter((CC.match(c["subj"]).group(1).lower() if CC.match(c["subj"]) else "(none)") for c in cs)
    cct.update(t)
    ccr.append(t)
wcsv("E03_corrective_weekly.csv", ["week", "nonmerge"] + [l for l, _ in CORR],
     cr + [["TOTAL"] + [sum(r[i] for r in cr) for i in range(1, 2 + len(CORR))]])
tl = [k for k, _ in cct.most_common()]
wcsv("E03_cc_types_weekly.csv", ["week"] + tl + ["pct_fix_of_typed", "pct_typed"],
     [[w] + [t[k] for k in tl] + [round(100 * t["fix"] / max(1, sum(t.values()) - t["(none)"]), 1),
                                  round(100 * (sum(t.values()) - t["(none)"]) / max(1, sum(t.values())), 1)]
      for w, t in zip(weeks, ccr)] + [["TOTAL"] + [cct[k] for k in tl] +
                                      [round(100 * cct["fix"] / (sum(cct.values()) - cct["(none)"]), 1),
                                       round(100 * (sum(cct.values()) - cct["(none)"]) / sum(cct.values()), 1)]])
# first-parent-only variant (one row per landed change)
fpc = collections.Counter((CC.match(c["subj"]).group(1).lower() if CC.match(c["subj"]) else "(none)")
                          for c in NONMERGE if c["fp"])
wcsv("E03_cc_types_first_parent.csv", ["type", "first_parent_nonmerge"], fpc.most_common())
# fix-like subjects without CC prefix (plain English "Fix ...")
FIXW = re.compile(r"^(fix|fixes|fixed)\b", re.I)

# ---------------------------------------------------------------- 9. temporal
hrows = []
for h in range(24):
    def cnt(sel, utc):
        return sum(1 for c in C if sel(c) and (c["ad"].astimezone(dt.timezone.utc).hour if utc else c["ad"].hour) == h)
    hrows.append([h, cnt(lambda c: not c["merge"], False), cnt(lambda c: not c["merge"], True),
                  cnt(lambda c: not c["merge"] and not c["fp"], False), cnt(lambda c: not c["merge"] and not c["fp"], True),
                  cnt(lambda c: not c["merge"] and c["ai_any"], False), cnt(lambda c: not c["merge"] and c["ai_any"], True),
                  cnt(lambda c: not c["merge"] and not c["ai_any"], False), cnt(lambda c: not c["merge"] and not c["ai_any"], True)])
wcsv("E03_hours.csv", ["hour", "nonmerge_local", "nonmerge_utc", "side_branch_local", "side_branch_utc",
                       "ai_local", "ai_utc", "noai_local", "noai_utc"], hrows)
WD = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
wdr = []
for i, n in enumerate(WD):
    wdr.append([n, sum(1 for c in NONMERGE if c["ad"].weekday() == i),
                sum(1 for c in NONMERGE if c["ad"].astimezone(dt.timezone.utc).weekday() == i),
                sum(1 for c in NONMERGE if c["ai_any"] and c["ad"].weekday() == i)])
wcsv("E03_weekday.csv", ["weekday", "nonmerge_local", "nonmerge_utc", "ai_local"], wdr)
top10 = [a for a, _ in collections.Counter(c["auth"] for c in NONMERGE).most_common(10)]
wcsv("E03_hours_top_authors_utc.csv", ["author"] + [f"h{h:02d}" for h in range(24)] + ["distinct_tz_offsets"],
     [[a] + [sum(1 for c in NONMERGE if c["auth"] == a and c["ad"].astimezone(dt.timezone.utc).hour == h)
             for h in range(24)] +
      [";".join(sorted({c["ad"].strftime("%z") for c in NONMERGE if c["auth"] == a}))] for a in top10])
# per-author activity stretches (author timestamps, all commits by that author, gap <= 60 min)
stretch = []
byauth = collections.defaultdict(list)
for c in C:
    byauth[c["auth"]].append(c)
for a, cs in byauth.items():
    ts = sorted(c["ad"].timestamp() for c in cs)
    s = 0
    for i in range(1, len(ts) + 1):
        if i == len(ts) or ts[i] - ts[i - 1] > 3600:
            stretch.append((a, (ts[i - 1] - ts[s]) / 3600, i - s,
                            dt.datetime.fromtimestamp(ts[s], dt.timezone.utc).isoformat(timespec="minutes")))
            s = i
stretch.sort(key=lambda r: -r[1])
wcsv("E03_author_stretches_top30.csv", ["author", "hours", "commits", "start_utc"],
     [[a, round(h, 1), n, st] for a, h, n, st in stretch[:30]])
# repo-level quiet gaps (all commits, author+committer timestamps)
allts = sorted({c["cd"].timestamp() for c in C})
gaps = sorted(((allts[i] - allts[i - 1]) / 3600, allts[i - 1]) for i in range(1, len(allts)))[::-1][:10]
wcsv("E03_repo_quiet_gaps_top10.csv", ["hours_without_commit_committer_time", "gap_start_utc"],
     [[round(g, 2), dt.datetime.fromtimestamp(s, dt.timezone.utc).isoformat(timespec="minutes")] for g, s in gaps])


def area(path):
    p = path.split("/")
    return "/".join(p[:2]) if p[0] in ("crates", "apps") and len(p) > 2 else p[0]


busy = []
for a in [x for x, _ in collections.Counter(c["auth"] for c in NONMERGE).most_common(15)]:
    cs = [c for c in NONMERGE if c["auth"] == a]
    dcount = collections.Counter(c["aday"] for c in cs)
    bd, bn = dcount.most_common(1)[0]
    day = sorted((c for c in cs if c["aday"] == bd), key=lambda c: c["ad"])
    g = [(day[i]["ad"] - day[i - 1]["ad"]).total_seconds() / 60 for i in range(1, len(day))]
    pairs5 = disj5 = 0
    allcs = sorted(cs, key=lambda c: c["ad"])
    for i in range(1, len(allcs)):
        if (allcs[i]["ad"] - allcs[i - 1]["ad"]).total_seconds() <= 300:
            pairs5 += 1
            A = {area(f[2]) for f in allcs[i]["files"]}; B = {area(f[2]) for f in allcs[i - 1]["files"]}
            if A and B and not (A & B):
                disj5 += 1
    busy.append([a, len(cs), bd, bn, round(med(g), 1) if g else "", sum(1 for x in g if x <= 5), pairs5, disj5,
                 sum(1 for c in cs if c["ai_any"])])
wcsv("E03_author_busiest_days.csv", ["author", "nonmerge_commits", "busiest_author_day_utc", "commits_that_day",
                                     "median_gap_min_that_day", "gaps_le_5min_that_day",
                                     "all_consecutive_pairs_le_5min", "of_which_disjoint_areas", "ai_attributed"], busy)

# ---------------------------------------------------------------- 10. releases
tags = []
for line in git("for-each-ref", "--format=%(refname:short)%09%(*objectname)%09%(objectname)", "refs/tags").splitlines():
    t, deref, obj = line.split("\t")
    tags.append((t, deref or obj))
tinfo = []
for t, s in tags:
    cd = dt.datetime.fromisoformat(git("log", "-1", "--format=%cI", s).strip())
    tinfo.append((cd, t, s))
tinfo.sort()
rel = []
prev = None
for cd, t, s in tinfo:
    onmain = s in main_set
    onfp = s in first_parent
    if prev:
        n = int(git("rev-list", "--count", f"{prev[2]}..{s}").strip())
        nfp = int(git("rev-list", "--first-parent", "--count", f"{prev[2]}..{s}").strip())
        days_ = round((cd - prev[0]).total_seconds() / 86400, 2)
    else:
        n = int(git("rev-list", "--count", s).strip()); nfp = int(git("rev-list", "--first-parent", "--count", s).strip())
        days_ = ""
    rel.append([t, s[:10], cd.astimezone(dt.timezone.utc).isoformat(timespec="minutes"), onmain, onfp, n, nfp, days_])
    prev = (cd, t, s)
wcsv("E03_releases.csv", ["tag", "commit", "commit_date_utc", "reachable_from_main", "on_first_parent",
                          "commits_since_prev_tag", "first_parent_since_prev_tag", "days_since_prev_tag"], rel)

# ---------------------------------------------------------------- 11. hot spots
fc = collections.Counter()
fch = collections.Counter()
for c in NONMERGE:
    for a, d, pth in c["files"]:
        fc[pth] += 1
        fch[pth] += a + d
wcsv("E03_hotspots_top40.csv", ["path", "nonmerge_commits_touching", "lines_changed"],
     [[p_, n, fch[p_]] for p_, n in fc.most_common(40)])
SPEC = [("AGENTS.md", lambda p_: p_ == "AGENTS.md"),
        ("any AGENTS.md/CLAUDE.md", lambda p_: p_.split("/")[-1] in ("AGENTS.md", "CLAUDE.md")),
        ("docs/**", lambda p_: p_.startswith("docs/")), ("docs/*.md top", lambda p_: re.match(r"^docs/[^/]+\.md$", p_)),
        (".github/workflows/**", lambda p_: p_.startswith(".github/workflows/")),
        ("Cargo.lock", lambda p_: p_ == "Cargo.lock")]
sr = []
for w in weeks:
    cs = [c for c in NONMERGE if c["week"] == w]
    row = [w]
    for l, f in SPEC:
        row += [sum(1 for c in cs if any(f(x[2]) for x in c["files"])),
                sum(x[0] + x[1] for c in cs for x in c["files"] if f(x[2]))]
    sr.append(row)
hdr = ["week"]
for l, _ in SPEC:
    hdr += [l + " commits", l + " lines"]
sr.append(["TOTAL"] + [sum(r[i] for r in sr) for i in range(1, len(hdr))])
wcsv("E03_churn_special_weekly.csv", hdr, sr)

# ---------------------------------------------------------------- duplicates (double-counting check)
dup = collections.Counter((c["auth"], c["subj"].strip().lstrip("\ufeff")) for c in NONMERGE)
dup_commits = sum(n for n in dup.values() if n > 1)
dup_extra = sum(n - 1 for n in dup.values() if n > 1)
pdup = collections.Counter(tuple(sorted((f[2], f[0], f[1]) for f in c["files"])) + (c["subj"].strip(),)
                           for c in NONMERGE if c["files"])
pdup_extra = sum(n - 1 for n in pdup.values() if n > 1)
wcsv("E03_duplicates.csv", ["metric", "value"],
     [["nonmerge commits whose (author, subject) occurs more than once", dup_commits],
      ["extra copies beyond the first (author, subject)", dup_extra],
      ["extra copies with identical subject AND identical numstat (likely cherry-pick/rebase copies)", pdup_extra]])
# tags: which remote branches contain tags that are not reachable from main
tag_br = []
for r in rel:
    if not r[3]:
        brs = git("branch", "-r", "--contains", r[1]).split()
        tag_br.append([r[0], r[1], " ".join(b for b in brs if b != "->")[:300]])
wcsv("E03_tags_off_main.csv", ["tag", "commit", "remote_branches_containing"], tag_br)

# ---------------------------------------------------------------- report
print("commits", len(C), "nonmerge", len(NONMERGE), "merges", len(C) - len(NONMERGE), "first_parent", len(first_parent))
print("fp merges by kind", dict(fp_merge_kind))
print("attr totals", ATTR_TOT)
print("distinct session values", sess_distinct)
print("PR", PR_STATS)
print("PR heads", dict(cat))
print("branches", BR_STATS)
print("authors canonical", len(set(CANON.values())), "raw names", len(name_cnt))
print("cc first-parent", fpc.most_common())
print("plain 'Fix...' subjects (nonmerge)", sum(1 for c in NONMERGE if FIXW.match(c["subj"])))
print("dups", dup_commits, dup_extra, pdup_extra)
print("days", daylist[0], daylist[-1], "weeks", weeks)
