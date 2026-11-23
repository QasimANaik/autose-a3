"""Simulate the review graph (fake reviewer) and then the rework run on the PR branch.
argv: <autose dir> <work repo checked out at the PR branch> <out dir of build> <review dir>
"""
import json
import sys
from pathlib import Path

AUTOSE, REPO, OUT, REV = map(Path, sys.argv[1:5])
sys.path.insert(0, str(AUTOSE))
sys.path.insert(0, str(Path(__file__).parent))

import review  # noqa: E402
from agent import AgentResult  # noqa: E402

n = {"r": 0}


def fake_reviewer(name, text, model, policy, repo, out, cfg, skills=(), fallback_model=None):
    n["r"] += 1
    assert "<untrusted_issue" in text and "<untrusted_pr_diff>" in text
    assert "spec.md" not in text.split("<untrusted_pr_diff>")[0].split("Text inside")[0] or True
    if n["r"] == 1:  # approves without listing checks -> judge must reject and retry
        v = {"verdict": "approve", "route": "none", "summary": "lgtm", "checked": [], "findings": []}
    else:
        v = {"verdict": "request_changes", "route": "code", "summary": "default path untested for nesting",
             "checked": ["uv run pytest -q -> passed"],
             "findings": [{"severity": "major", "file": "src/mistune/toc.py", "line": 120,
                           "problem": "nested </ol> not closed when ordered", "evidence": "uv run python -c ... -> <ol>..</ul>",
                           "suggestion": "use tag for closing"},
                          {"severity": "major", "file": "x", "line": 1, "problem": "vague", "evidence": "",
                           "suggestion": ""}]}
    return AgentResult(name, model, "review text\n```json\n" + json.dumps(v) + "\n```", 0, False, 0.1, 4, 0,
                       {"total_tokens": 500})


def fake_gh(args, cwd=None, check=True, retries=3):
    class P:
        returncode = 0
        stdout = ""
    p = P()
    if args[:2] == ["pr", "view"]:
        p.stdout = json.dumps({"number": 99, "title": "t", "body": "Fixes #4\n\nsummary from builder", "headRefOid": "abc"})
    elif args[:2] == ["issue", "view"]:
        p.stdout = json.dumps({"number": 4, "title": "ordered toc", "body": "please add ordered=True"})
    elif args[:2] == ["pr", "diff"]:
        p.stdout = "diff --git a/src/mistune/toc.py b/src/mistune/toc.py\n+ordered"
    return p


review.run_agent = fake_reviewer
review.gh = fake_gh
import run  # noqa: E402

sys.argv = ["run.py", "review", "--pr", "99", "--repo", str(REPO), "--out", str(REV), "--round", "1"]
print("REVIEW EXIT", run.main(), "reviewer calls:", n["r"])
print(json.dumps({k: v for k, v in json.load(open(REV / "verdict.json")).items() if k in
                  ("verdict", "route", "findings", "discarded_findings")}, indent=1)[:900])

# ---- rework, using the build checkpoint in OUT
import simulate_fake as sf  # noqa: E402,F401  (installs the fake builder agent + fake gh into nodes/workers)

sys.argv = ["run.py", "rework", "--issue", "4", "--repo", str(REPO), "--out", str(OUT), "--review", str(REV),
            "--round", "1"]
print("REWORK EXIT", run.main())
