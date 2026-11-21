# Stage map (planned; update after real runs)

| # | Stage | Agent / component | Input | Artifact | Check (who decides) | On failure |
|---|---|---|---|---|---|---|
| 1 | Requirements | Builder (`claude -p`, fresh context) + A1 skill | issue (untrusted, tagged) | `spec.md` | `spec_lint.py`: every AC has an id + Given/When/Then; LLM judge "testable?" → orchestrator rule decides | 1 retry, then STOP with reason |
| 2 | Design | Builder (fresh context) | spec.md + ARCHITECTURE.md + repo | `design.md` | `design_refs.py`: every named file/function exists (AST) → orchestrator | 1 retry, then STOP |
| 3 | Implementation | Builder (fresh context) | design.md + spec.md + repo | `diff.patch` (branch `autose/issue-N`) | `build_check.sh`: uv sync, import, ruff, mypy + `diff_guard.py` | ≤2 retries, then STOP |
| 4 | Testing | Builder (fresh context) | spec.md (ACs) + diff + repo | `test_report.md` | pytest exit code (old + new tests, ≥1 test per AC id) | back to 3 (≤2), then back to 2 (≤1), then STOP |
| 5 | Release | Orchestrator (no LLM, `gh` CLI) | all artifacts | `pr.md` + PR link | PR open + `tests.yml` run green (`gh run watch`) | back to 4 once, then STOP |
| 6 | Review | **Reviewer** (own job, different model, read-only) | issue + PR diff + PR-head checkout only | `review.md` + `verdict.json` | reviewer verdict; posted by `publish` job | code issue → 3, approach issue → 2; max 2 rounds |
| – | Merge | **Human maintainer** | PR + review | – | person decides | – |
