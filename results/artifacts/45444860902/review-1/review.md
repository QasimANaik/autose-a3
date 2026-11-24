## AutoSE independent review, round 1: ✅ APPROVE

**Route:** `none` · **Reviewer model:** `gemini-3.5-flash-lite` · **Variant:** `baseline` · PR #24

The pull request cleanly and safely resolves issue #18 by adding `www.` pattern matching to the URL autolink plugin, correctly formatting URLs with `http://`, and updating parser trigger characters. All unit tests, ruff checks, and mypy type checks passed successfully without regressions.

### What the reviewer checked
- uv run python -c "import mistune; md = mistune.create_markdown(plugins=['url']); print(repr(md('alice: docs are at www.example.com/docs, or the old page https://example.com/old')))"
- uv run pytest -q --tb=short
- uv run ruff check .
- uv run mypy src/mistune

### Findings
None.

_The reviewer saw only the issue, the diff and the PR-head checkout. It cannot push. A human decides whether to merge._
