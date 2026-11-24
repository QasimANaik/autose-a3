"""Replay of run 45351202045 (issue #4): correct implementation, one wrong AC, a worker that tests it literally.
Expect: merge fails -> implement keeps its code -> loop_dispute -> worker re-checks + AC-CONFLICT -> release.
argv: <autose dir> <work repo> <out dir> [stubborn]   (stubborn: the worker never fixes the test -> clear stop)
"""
import json
import sys
from pathlib import Path

AUTOSE, REPO, OUT = map(Path, sys.argv[1:4])
STUBBORN = len(sys.argv) > 4
sys.path.insert(0, str(AUTOSE))

import agent  # noqa: E402
import nodes  # noqa: E402
import workers  # noqa: E402
from agent import AgentResult  # noqa: E402

GOOD_IMPL = None
calls = {"implement": 0, "rechecks": 0}
FLAT = '<ol>\n<li><a href="#a">A</a></li>\n<li><a href="#b">B</a></li>\n</ol>\n'
NESTED = '<ol>\n<li><a href="#a">A</a>\n<ol>\n<li><a href="#b">B</a></li>\n</ol>\n</li>\n</ol>\n'


def fake(name, text, model, policy, repo, out, cfg, skills=(), fallback_model=None):
    repo = Path(repo)
    resp = "done"
    if "Stage 1, Requirements" in text:
        d = repo / ".autose-work" / "spec"
        d.mkdir(parents=True, exist_ok=True)
        (d / "SRS-issue-4-v1.md").write_text(
            "### FR-001\n- **Acceptance criteria:**\n"
            "  - AC-FR-001-1: Given nested items, when render_toc_ul(items, ordered=True) is called, then the output is a FLAT ol list.\n"
            "  - AC-FR-001-2: Given nested items, when render_toc_ul(items, ordered=True) is called, then it starts with <ol>.\n")
        (d / "REG-issue-4-v1.md").write_text("x")
        (d / "VAL-issue-4-v1.md").write_text("x")
    elif "Stage 2, Design" in text:
        (repo / ".autose-work" / "design.md").write_text(
            "## Summary\nx\n\n## Files and functions to change\n- `src/mistune/toc.py`: `render_toc_ul`\n\n## Plan\n1. x\n")
    elif "Stage 3, Implementation" in text:
        calls["implement"] += 1
        if calls["implement"] == 1:  # the real agent's (correct) change from run 45351202045
            import subprocess
            subprocess.run(["git", "apply", str(Path(__file__).parent / "run3_diff.patch")], cwd=repo, check=True)
        # later calls: the implementer believes the code is right and changes nothing
    elif "test worker" in text or "e2e / regression worker" in text:
        import re
        f = re.search(r"ONE file: `([^`]+)`", text).group(1)
        recheck = "RE-CHECK" in text
        if recheck:
            calls["rechecks"] += 1
        expected = NESTED if (recheck and not STUBBORN) else FLAT
        body = ("from mistune.toc import render_toc_ul\n\nITEMS = [(1, 'a', 'A'), (2, 'b', 'B')]\n\n\n"
                f"def test_ac_fr_001_1():\n    \"\"\"AC-FR-001-1\"\"\"\n    assert render_toc_ul(ITEMS, ordered=True) == {expected!r}\n\n\n"
                "def test_ac_fr_001_2():\n    \"\"\"AC-FR-001-2\"\"\"\n    assert render_toc_ul(ITEMS, ordered=True).startswith('<ol>')\n")
        (repo / f).write_text(body)
        if recheck and not STUBBORN:
            resp = "AC-CONFLICT: AC-FR-001-1: a flat list contradicts mistune's nested TOC structure; tested nesting."
    return AgentResult(name, model, resp, 0, False, 0.1, 3, 0, {"total_tokens": 1000})


for m in (agent, nodes, workers):
    m.run_agent = fake


def fake_gh(args, cwd=None, check=True, retries=3):
    class P:
        returncode = 0
        stdout = ""
    p = P()
    if args[:2] == ["issue", "view"]:
        p.stdout = json.dumps({"number": 4, "title": "ordered toc", "body": "add ordered=True", "url": "u"})
    return p


nodes.gh = fake_gh
nodes.Nodes._ensure_pr = lambda self, s: (99, "https://example/pr/99")
nodes.Nodes._wait_ci = lambda self, b, sha: (True, {"url": "ci", "conclusion": "success"})
import run  # noqa: E402

sys.argv = ["run.py", "build", "--issue", "4", "--repo", str(REPO), "--out", str(OUT)]
code = run.main()
print("EXIT", code, "implement calls:", calls["implement"], "re-checks:", calls["rechecks"])
