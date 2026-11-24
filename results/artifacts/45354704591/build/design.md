## Summary
Add an optional `ordered` keyword parameter (defaulting to `False`) to `render_toc_ul` in `src/mistune/toc.py`. When `ordered=True`, table of contents lists are rendered using `<ol>` and `</ol>` tags at all nesting levels instead of `<ul>` and `</ul>`. This provides native ordered TOC support while maintaining 100% backward compatibility for existing callers.

## Files and functions to change
- `src/mistune/toc.py`: `render_toc_ul`
- `tests/test_hooks.py`: `TestTocHook.test_render_ordered_toc`

## Plan
1. Update `render_toc_ul` function signature in `src/mistune/toc.py` to accept `ordered: bool = False` (satisfies FR-001, FR-002, NFR-001).
2. Parameterize list tags (`ul` / `ol`) in `render_toc_ul` based on the `ordered` flag across all nesting levels (satisfies FR-002).
3. Add unit tests in `tests/test_hooks.py` covering ordered and unordered TOC rendering with single and nested items (satisfies AC-FR-001-1..2, AC-FR-002-1..3, AC-NFR-001-1).
4. Verify changes using `uv run pytest`, `uv run ruff check .`, and `uv run mypy`.

## Risks
- Edge cases in nested list indentation and tag closure when switching between `<ul>` and `<ol>`. Mitigation: parameterize the tag string (`tag = 'ol' if ordered else 'ul'`) in all opening and closing tags in `render_toc_ul`.
- Type safety and strict mypy compliance. Mitigation: type hint `ordered: bool = False` and `tag: str` explicitly.


---
## Stage 2 check (orchestrator)

**PASS**

- (no problems found)
