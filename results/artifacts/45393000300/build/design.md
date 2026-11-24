## Summary
The URL auto-linking plugin (`src/mistune/plugins/url.py`) will be updated to correctly match URLs containing balanced parentheses (such as Wikipedia article URLs) while excluding trailing question marks (`?`), exclamation marks (`!`), periods (`.`), and commas (`,`). This ensures that plain URLs in user text do not truncate at internal parentheses and do not erroneously capture sentence-ending punctuation. These updates place the fix directly within the URL parsing regex and helper function of the URL plugin, preserving full compatibility with the existing architecture and test suite.

## Files and functions to change
- `src/mistune/plugins/url.py`: `parse_url_link`, `url`
- `tests/fixtures/url.txt`: `url` (new test cases for parentheses and trailing punctuation)
- `tests/test_plugins.py`: `load_plugin`

## Existing tests to update
None

## Plan
1. Update `URL_LINK_PATTERN` in `src/mistune/plugins/url.py` to support balanced parentheses and exclude trailing punctuation including `?` and `!` alongside `.`, `,`, `;`, `:`, `"` , `'`, and `)`. (Satisfies AC-FR-001-1, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2).
2. Refine `parse_url_link` or regex matching logic to handle trailing punctuation trimming correctly (e.g., stripping trailing `?`, `!`, `.`, `,` if present, while maintaining balanced parenthesis matching). (Satisfies AC-FR-001-1, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2, AC-FR-004-1).
3. Add comprehensive test cases covering Wikipedia links with parentheses and questions/exclamations ending sentences with links in `tests/fixtures/url.txt`. (Satisfies AC-FR-001-1, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-003-2, AC-FR-004-1).
4. Run verification tests (`uv run pytest -q --tb=short`, `uv run ruff check .`, `uv run mypy`) to ensure correctness, style compliance, and strict type safety. (Satisfies AC-NFR-001-1, CON-001).

## Risks
- **Edge cases with unbalanced or trailing parentheses:** URLs inside sentences might be followed by closing parentheses in text (e.g. `(see https://example.com)`). Care must be taken so balanced parenthesis matching does not consume trailing closing parentheses belonging to the outer text.
- **Type safety & linting:** Changes must strictly adhere to Python type annotations (`mypy --strict`) and Ruff formatting rules (`ruff check .`).


---
## Stage 2 check (orchestrator)

**PASS**

- (no problems found)
