## AutoSE independent review, round 1: ❌ REQUEST CHANGES

**Route:** `code` · **Reviewer model:** `gemini-3.5-flash-lite` · **Variant:** `baseline` · PR #20

The PR correctly adds the `ordered` parameter to `render_toc_ul` but hardcodes `<ul>` for nested lists instead of respecting `ordered=True` at every nesting level, and the tests omit nested cases.

### What the reviewer checked
- uv run pytest -q --tb=short
- uv run ruff check . && uv run mypy src
- uv run python -c 'from mistune.toc import render_toc_ul; print(render_toc_ul([(1, "a", "A"), (2, "b", "B")], ordered=True))'

### Findings
| Severity | Where | Problem | Evidence | Suggestion |
|---|---|---|---|---|
| major | `src/mistune/toc.py:128` | Nested lists are hardcoded to `<ul>` and `</ul>` regardless of the `ordered` parameter value, violating the requirement that `<ol>` should be used at every nesting level. | Output of python test: <ol>\n<li>...\n<ul>\n...\n</ul>\n</li>\n</ol> | Define and use dynamic tag strings (`<{tag}>` and `</{tag}>`) for all inner list openings and closings in `render_toc_ul`. |
| minor | `tests/test_toc_ordered.py:4` | New tests only assert behavior on flat lists and do not test nested lists. | tests/test_toc_ordered.py only tests `[(1, "a", "A"), (1, "b", "B")]` and `[(1, "a", "A")]`. | Add test cases containing nested heading levels (e.g., level 1 and level 2 items) with `ordered=True` to verify all nesting levels render `<ol>`. |

_The reviewer saw only the issue, the diff and the PR-head checkout. It cannot push. A human decides whether to merge._
