# Stage map

Which agent handles each stage, its artifact, and the check that must pass before the run moves on. Every check is
decided by code (`autose/checks.py`, `autose/nodes.py`); no model decides whether a stage passed or where the run goes.
Diagram: [`stage-map.drawio`](stage-map.drawio) (page 1: stages and loop-backs; page 2: the Actions job graph).

| # | Stage | Agent / component (LangGraph node) | Input | Artifact | Check before moving on | On failure |
|---|---|---|---|---|---|---|
| 1 | Requirements | builder agent `understand` + A1 `requirements-spec` skill | issue in `<untrusted_issue>` tags | `spec.md` (SRS / REG / VAL) | every AC has an id and Given/When/Then; no vague words (A1 validator lexicon); A1 validator result recorded | retry 1, then `clarify` (questions, no code) |
| 2 | Design | builder agent `design` | SRS + `ARCHITECTURE.md` + repo | `design.md` | every named `src/` file and function exists (AST); new ones marked `(new)`; existing tests to update must exist and cite an AC (ADR-015) | retry 1, then stop |
| 3 | Implementation | builder agent `implement` | design + AC list (+ failures / review findings) | `diff.patch` | import, `ruff src`, strict `mypy`; edits outside `src/` and the declared test files are reverted | retry 2, then stop |
| 4 | Testing | `orchestrator` (code) → parallel `criterion_worker` × N + `e2e_worker`, merged by `merge` (code) | each worker: its ACs + src diff, own git worktree | `test_report.md` | full suite green; every AC id cited by a test; new tests ruff-clean | →3 (≤2); dispute: re-check failing new tests (≤1); →2 redesign (≤1); stop + draft PR listing failing tests (ADR-016) |
| 5 | Release | `release` (code, `gh`) | branch + artifacts | `pr.md` + PR link | PR open and `tests.yml` green (failed jobs re-run once for flaky timing tests) | →3 once, then stop |
| 6 | Review | independent `reviewer` in its own read-only job; `judge` (code) | linked issue + PR diff + PR-head checkout only | `review.md` + `verdict.json` | approve, or two rounds used; findings without evidence dropped | round 1 changes → `rework-1` (code → 3, approach → 2) → `review-2` |
| – | Merge | **human** | PR + review | – | a person decides; the bot never merges (CODEOWNERS ruleset) | – |

Models: every agent node uses `gemini-3.5-flash-lite` (fallback `gemini-3.1-flash-lite`), ADR-014.
