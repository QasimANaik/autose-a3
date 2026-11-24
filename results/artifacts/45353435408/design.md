## Summary
This change adds an optional `ordered=False` keyword parameter to `render_toc_ul` in `src/mistune/toc.py`. When `ordered=True`, table of contents generation uses `<ol>` instead of `<ul>` tags across all nesting levels, while preserving existing `<ul>` behavior when omitted or `False`. This provides built-in support for numbered tables of contents in Mistune without duplicating upstream utility functions.

## Files and functions to change
- `src/mistune/toc.py`: `render_toc_ul`
- `tests/test_hooks.py`: `TestTocHook.test_render_ordered_toc (new)`, `TestTocHook.test_render_unordered_toc (new)`

## Plan
1. Update `render_toc_ul` function signature in `src/mistune/toc.py` to accept `ordered: bool = False` and define tag selector `tag = "ol" if ordered else "ul"`. Satisfies AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2, AC-NFR-001-1.
2. Replace hardcoded `"ul"` tags with dynamic `tag` variable across nesting and closing loops in `render_toc_ul`. Satisfies AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2.
3. Add `TestTocHook.test_render_ordered_toc (new)` and `TestTocHook.test_render_unordered_toc (new)` to `tests/test_hooks.py` to verify flat, nested, and empty TOC rendering for both ordered and unordered modes. Satisfies AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2, AC-NFR-001-1.
4. Execute validation checks (`uv run pytest -q`, `uv run ruff check .`, `uv run mypy`). Satisfies AC-NFR-001-1.

## Risks
- Edge case: Nesting mismatch or mismatched closing/opening list tags when switching between list types. Mitigation: Consistently use dynamic `tag` variable throughout `render_toc_ul` for all container opens and closes.
- Type safety and Linting: Ensure type annotations (`ordered: bool = False`) are fully compatible with strict `mypy` and `ruff check .`.


---
## Stage 2 check (orchestrator)

**FAIL**

- `TestTocHook.test_render_ordered_toc (new` not found in tests/test_hooks.py (mark it `(new)` if it should be created)
- `TestTocHook.test_render_unordered_toc (new` not found in tests/test_hooks.py (mark it `(new)` if it should be created)


## Why this stage stopped

check did not pass within its retries

Run: https://github.com/QasimANaik/mistune/actions/runs/45353435408
