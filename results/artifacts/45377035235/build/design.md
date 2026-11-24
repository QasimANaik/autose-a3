## Summary
We will add a `link_rel` configuration option to `HTMLRenderer.__init__` in `src/mistune/renderers/html.py` and apply it in `HTMLRenderer.link()` when rendering anchor tags. Because normal links, autolinks, and URL plugin links all use the `link()` method in `HTMLRenderer`, this automatically covers all required link types while leaving images unaffected. This is the cleanest and most direct architectural placement, adhering to ADR-1 and existing renderer design patterns.

## Files and functions to change
- `src/mistune/renderers/html.py`: `HTMLRenderer.__init__`, `HTMLRenderer.link`
- `tests/test_renderers.py`: `TestHTMLRendererLinkRel` (new)

## Plan
1. Update `HTMLRenderer.__init__` to accept an optional `link_rel: Optional[str] = None` parameter and store it as `self._link_rel`. Satisfies FR-001, FR-004.
2. Update `HTMLRenderer.link` to conditionally include a `rel` attribute with the configured `link_rel` value when `self._link_rel` is truthy. Satisfies FR-001, FR-002, FR-003, FR-004.
3. Add unit test suite `TestHTMLRendererLinkRel` in `tests/test_renderers.py` covering normal links, autolinks, URL plugin links, exclusion of images, and default behavior without `link_rel`. Satisfies AC-FR-001-1..2, AC-FR-002-1..2, AC-FR-003-1, AC-FR-004-1, NFR-001.

## Risks
- **Edge cases and existing behavior:** Images must not receive the `rel` attribute; since `image()` uses the `<img>` tag and does not call `link()`, images remain unaffected. Default behavior when `link_rel` is omitted or None must produce identical HTML to previous versions.
- **Type checking and linting:** Ensure all new parameters and type hints conform to mypy strict mode (`uv run mypy`) and ruff lint rules (`uv run ruff check .`).


---
## Stage 2 check (orchestrator)

**PASS**

- (no problems found)
