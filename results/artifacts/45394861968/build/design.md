## Summary
The math plugin in Mistune currently parses inline double-dollar math expressions (`$$\dots$$`) into `block_math` tokens, causing block-level `<div>` elements to be generated inside paragraphs and splitting sentences. By updating `parse_inline_math` in `src/mistune/plugins/math.py` to produce `inline_math` tokens for inline double-dollar expressions, these expressions render cleanly as inline `<span class="math">` elements without breaking layout or HTML validation. Block-level math (`$$\dots$$` on its own lines) remains correctly handled by block parsing rules.

## Files and functions to change
- `src/mistune/plugins/math.py`: `parse_inline_math`
- `tests/fixtures/math.txt`

## Existing tests to update
- `tests/fixtures/math.txt`: AC-FR-001-1 (update the expected output for inline double-dollar expressions from `<div>` rendering inside `<p>` to inline `<span class="math">\(...\)</span>` rendering).

## Plan
1. Update `parse_inline_math` in `src/mistune/plugins/math.py` so that when `display_math_text` is matched by `INLINE_MATH_PATTERN`, it appends an `inline_math` token (`{"type": "inline_math", "raw": display_text}`) instead of a `block_math` token (Satisfies AC-FR-001-1).
2. Update existing test cases in `tests/fixtures/math.txt` that test inline double-dollar syntax (such as "No newline $$x$$") to expect inline `<span class="math">\(x\)</span>` output (Satisfies AC-FR-001-1).
3. Add a specific test case for the issue reporter's example (`The famous relation $$E=mc^2$$ changed physics.`) to `tests/fixtures/math.txt` (Satisfies AC-FR-001-1).
4. Run `uv run pytest -q --tb=short`, `uv run ruff check .`, and `uv run mypy` to verify correctness, type safety, and lint compliance.

## Risks
- **Regression in Block Math:** Block math (`$$\dots$$` on dedicated lines) uses `BLOCK_MATH_PATTERN` in the block parser (`parse_block_math`) and remains completely unaffected.
- **Single-dollar and Backtick Math:** Single-dollar math and backtick math already use `inline_math` and continue to render identically (Satisfies AC-FR-003-1, AC-FR-004-1).
- **Type Checking and Linting:** The code change is purely internal to `parse_inline_math` token emission type (string literal `"inline_math"` instead of `"block_math"`), maintaining strict adherence to Python type hints (`mypy --strict`) and Ruff lint rules.


---
## Stage 2 check (orchestrator)

**PASS**

- (no problems found)
