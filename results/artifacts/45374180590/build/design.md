## Summary
The math plugin's inline parser is updated to parse inline double-dollar expressions (`$$...$$`) as inline math tokens (`inline_math`) rather than block math tokens, ensuring they render as `<span class="math">\(...\)</span>` instead of block divs within paragraphs. Additionally, test fixtures are updated to align with the new inline rendering behavior for inline double-dollar syntax. This is the correct architectural place as syntax parsing rules and token generation belong in the math plugin module (`src/mistune/plugins/math.py`).

## Files and functions to change
- `src/mistune/plugins/math.py`: `parse_inline_math`
- `tests/fixtures/math.txt`: `test_inline_math_007`
- `tests/test_autose_issue_5_e2e.py`: `TestAutoseIssue5E2E.test_inline_double_dollar_math_and_nfr`

## Plan
1. Update `src/mistune/plugins/math.py` to ensure `parse_inline_math` correctly maps `display_math_text` to `inline_math` tokens. (Satisfies AC-FR-001-1, AC-NFR-001-1)
2. Update `tests/fixtures/math.txt` fixture `test_inline_math_007` (`No newline $$x$$`) to expect inline span rendering (`<span class="math">\(x\)</span>`). (Satisfies AC-FR-001-1)
3. Validate and extend tests across `tests/test_autose_issue_5_e2e.py`, `tests/test_autose_issue_5_fr001.py`, and other test suites. (Satisfies AC-FR-001-1, AC-FR-002-1, AC-FR-003-1, AC-FR-004-1, AC-FR-005-1, AC-NFR-001-1)

## Risks
- Edge case: Block-level math (`$$\n...\n$$` or `$$...$$` on its own line) must continue to render as `<div class="math">` blocks (FR-002). This is protected by separate block math rules and patterns.
- Edge case: Single-dollar math (`$...$`) and backtick math (`$`...``) must remain unaffected (FR-003, FR-004).
- Edge case: Currency and non-math dollar signs (`$51,300`) must not be parsed as math (FR-005).
- Compatibility with `uv run mypy` (strict) and `uv run ruff check .`: Code changes maintain strict type annotations and conform to ruff linting rules.


---
## Stage 2 check (orchestrator)

**PASS**

- (no problems found)
