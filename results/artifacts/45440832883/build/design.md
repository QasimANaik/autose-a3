## Summary
This change adds an optional `ordered: bool = False` keyword argument to `render_toc_ul` in `src/mistune/toc.py`. When `ordered=True`, the function renders table of contents items using `<ol>` tags instead of `<ul>` tags at all nesting levels, while preserving default unordered behavior when omitted or set to `False`. This addresses GitHub Issue #4 by enabling numbered table of contents output required by various documentation style guides.

## Files and functions to change
- `src/mistune/toc.py`: `render_toc_ul`
- `tests/test_hooks.py`: `TestTocHook.test_render_toc_ordered`, `TestTocHook.test_render_toc_unordered`

## Existing tests to update
None

## Plan
1. Update `render_toc_ul` signature in `src/mistune/toc.py` to accept `ordered: bool = False`.
2. Refactor HTML generation logic in `render_toc_ul` to use `<ol>` or `<ul>` dynamically based on the `ordered` parameter value. (FR-001, FR-002)
3. Add unit tests in `tests/test_hooks.py` (`TestTocHook`) covering both ordered (`ordered=True`) and unordered (`ordered=False` / default) TOC rendering with flat and nested TOC structures. (AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2)
4. Verify changes using `uv run pytest -q --tb=short`, `uv run ruff check .`, and `uv run mypy`.

## Risks
- Nesting tag mismatch or invalid closing tags for complex hierarchies (mitigated by existing test suite and new test cases covering multi-level TOC items).
- Type safety and strict mypy compliance (mitigated by adding explicit type annotations: `ordered: bool = False` and `list_tag: str`).


---
## Stage 2 check (orchestrator)

**PASS**

- (no problems found)
