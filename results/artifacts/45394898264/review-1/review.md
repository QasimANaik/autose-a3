## AutoSE independent review, round 1: ✅ APPROVE

**Route:** `none` · **Reviewer model:** `gemini-3.5-flash-lite` · **Variant:** `baseline` · PR #17

The pull request successfully fixes table rendering when rows have missing or extra cells by padding or truncating cells to match the header length. All tests pass, fixtures are correctly updated for the new behavior, and linter/type checks pass cleanly.

### What the reviewer checked
- uv run python -c 'import mistune; md = mistune.create_markdown(plugins=["table"]); print(repr(md("| Name | Role |\n|------|------|\n| Ana |")))'
- uv run pytest -q --tb=short
- uv run ruff check .
- uv run mypy src

### Findings
None.

_The reviewer saw only the issue, the diff and the PR-head checkout. It cannot push. A human decides whether to merge._
