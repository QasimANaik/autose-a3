## AutoSE independent review, round 1: ✅ APPROVE

**Route:** `none` · **Reviewer model:** `gemini-3.5-flash-lite` · **Variant:** `baseline` · PR #11

The PR correctly implements the ordered table of contents option in render_toc_ul without breaking backward compatibility. All unit tests, integration tests, ruff checks, and strict mypy checks pass successfully.

### What the reviewer checked
- Ran pytest suite (1338 passed): `uv run pytest -q`
- Checked code style and linting with ruff: `uv run ruff check .`
- Checked type safety with mypy: `uv run mypy src/mistune`
- Verified issue example snippet output: `uv run python -c ...`
- Inspected code diff in src/mistune/toc.py and associated new test files

### Findings
None.

_The reviewer saw only the issue, the diff and the PR-head checkout. It cannot push. A human decides whether to merge._
