## AutoSE independent review, round 1: ✅ APPROVE

**Route:** `none` · **Reviewer model:** `gemini-3.5-flash-lite` · **Variant:** `baseline` · PR #16

The pull request correctly handles trailing punctuation and balanced parentheses in URLs for the url plugin, verified through comprehensive new tests, passing test suites, and clean lint/type checks.

### What the reviewer checked
- uv run pytest -q --tb=short
- uv run ruff check .
- uv run mypy src
- uv run python -c issue reproduction examples

### Findings
None.

_The reviewer saw only the issue, the diff and the PR-head checkout. It cannot push. A human decides whether to merge._
