"""Replay of run 45379575388 (issue #1): a correct src fix that must change behaviour pinned by EXISTING
fixture tests (tests/fixtures/table.txt). Expect: merge fails on existing tests -> implement keeps code ->
loop_redesign -> design declares the fixture under '## Existing tests to update' -> implement updates only
that file -> merge passes -> release.
argv: <autose dir> <work repo> <out dir> <real src patch>
"""
import json
import re
import subprocess
import sys
from pathlib import Path

AUTOSE, REPO, OUT, PATCH = map(Path, sys.argv[1:5])
sys.path.insert(0, str(AUTOSE))

import agent  # noqa: E402
import nodes  # noqa: E402
import workers  # noqa: E402
from agent import AgentResult  # noqa: E402

calls = {"design": 0, "implement": 0}
SNEAKY = len(sys.argv) > 5  # implementer also edits an UNdeclared test file -> must be reverted


def regenerate_fixture(repo: Path, rel: str) -> None:
    """What a correct agent would do: re-derive expected output with the new behaviour."""
    code = (
        "import re,sys\nfrom mistune import create_markdown\n"
        "md=create_markdown(escape=False,plugins=['table'])\n"
        "p=sys.argv[1]; t=open(p).read()\n"
        "def f(m):\n    src=m.group(2)\n    return m.group(1)+src+'.\\n'+md(src)+m.group(4)\n"
        "t=re.sub(r'(`{32} example\\n)(.*?)(\\.\\n.*?)(`{32})',f,t,flags=re.S)\n"
        "open(p,'w').write(t)\n")
    subprocess.run([str(repo / ".venv/bin/python"), "-c", code, str(repo / rel)], cwd=repo, check=True,
                   env={"PYTHONPATH": str(repo / "src"), "PATH": "/usr/bin:/bin"})


def fake(name, text, model, policy, repo, out, cfg, skills=(), fallback_model=None):
    repo = Path(repo)
    if "Stage 1, Requirements" in text:
        d = repo / ".autose-work" / "spec"
        d.mkdir(parents=True, exist_ok=True)
        (d / "SRS-issue-1-v1.md").write_text(
            "### FR-001\n- **Acceptance criteria:**\n"
            "  - AC-FR-001-1: Given a table whose body row has fewer cells than the header, when rendered with plugins=['table'], then a table is produced with an empty td.\n"
            "  - AC-FR-001-2: Given a table whose body row has an extra cell, when rendered, then the extra cell is dropped and a table is produced.\n")
        (d / "REG-issue-1-v1.md").write_text("x")
        (d / "VAL-issue-1-v1.md").write_text("x")
    elif "Stage 2, Design" in text:
        calls["design"] += 1
        upd = ("- `tests/fixtures/table.txt`: AC-FR-001-2 (mismatched rows are now tables, as the issue asks)\n"
               if "EXISTING tests fail" in text else "None\n")
        (repo / ".autose-work" / "design.md").write_text(
            "## Summary\nx\n\n## Files and functions to change\n- `src/mistune/plugins/table.py`: `parse_table`\n\n"
            f"## Existing tests to update\n{upd}\n## Plan\n1. x\n")
    elif "Stage 3, Implementation" in text:
        calls["implement"] += 1
        if calls["implement"] == 1:
            subprocess.run(["git", "apply", str(PATCH)], cwd=repo, check=True)
        if "tests/fixtures/table.txt" in text and "You may ALSO edit" in text:
            regenerate_fixture(repo, "tests/fixtures/table.txt")
            if SNEAKY:
                (repo / "tests/fixtures/url.txt").write_text("sneaky edit")
    elif "test worker" in text or "e2e / regression worker" in text:
        f = re.search(r"ONE file: `([^`]+)`", text).group(1)
        ids = re.findall(r"- (AC-FR-\d{3}-\d+):", text.split("<acceptance_criteria>")[1])
        body = "import mistune\n\nmd = mistune.create_markdown(plugins=['table'])\n"
        for i, a in enumerate(ids or ["AC-FR-001-1"]):
            body += f"\n\ndef test_{i}():\n    \"\"\"{a}\"\"\"\n    assert '<table>' in md('| a | b |\\n|---|---|\\n| x |')\n"
        (repo / f).write_text(body)
    return AgentResult(name, model, "done", 0, False, 0.1, 3, 0, {"total_tokens": 1000})


for m in (agent, nodes, workers):
    m.run_agent = fake


def fake_gh(args, cwd=None, check=True, retries=3):
    class P:
        returncode = 0
        stdout = ""
    p = P()
    if args[:2] == ["issue", "view"]:
        p.stdout = json.dumps({"number": 1, "title": "table", "body": "rows with missing/extra cells", "url": "u"})
    return p


nodes.gh = fake_gh
nodes.Nodes._ensure_pr = lambda self, s: (99, "https://example/pr/99")
nodes.Nodes._wait_ci = lambda self, b, sha: (True, {"url": "ci", "conclusion": "success"})
import run  # noqa: E402

sys.argv = ["run.py", "build", "--issue", "1", "--repo", str(REPO), "--out", str(OUT)]
code = run.main()
print("EXIT", code, calls)
