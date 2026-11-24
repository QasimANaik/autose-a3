## Summary
The mistune table plugin (`src/mistune/plugins/table.py`) is updated to support table row cell count tolerance by padding short rows with empty cells and truncating excess cells on long rows to match the header column count. This aligns mistune's table rendering behavior with GitHub and other Markdown tools while maintaining strict header and delimiter validation.

## Files and functions to change
- `src/mistune/plugins/table.py`: `_process_row`
- `tests/fixtures/table.txt`: AC-FR-001-1, AC-FR-002-1 (existing tests expecting failure/paragraphs on row length mismatch now expect successfully rendered table rows with padding or truncation)

## Existing tests to update
- `tests/fixtures/table.txt`: AC-FR-001-1, AC-FR-002-1 (existing test cases asserting that mismatched table row cell counts fall back to paragraph rendering must be updated to expect correctly padded or truncated table output).

## Plan
1. Update `_process_row` in `src/mistune/plugins/table.py` to pad rows having fewer cells than `aligns` with empty strings (`""`) and truncate rows having more cells than `aligns` to match `len(aligns)` instead of returning `None` on mismatch. (Satisfies FR-001, FR-002)
2. Verify that normal tables and invalid header/delimiter rows continue to render correctly without regression. (Satisfies FR-003, FR-004)
3. Update existing test cases in `tests/fixtures/table.txt` that tested row length mismatches and add new explicit fixtures/tests for padding short rows and truncating excess cells.

## Risks
- **Risk:** Over-acceptance of malformed text as table rows.
- **Mitigation:** Header and delimiter validation (`_process_thead`) remains strictly enforced so that tables with invalid header/delimiter counts still fail back to paragraphs (FR-004), while body row normalization only applies to subsequent rows once a valid header and delimiter are established.
- **Type safety & linting:** Ensure all changes maintain strict type safety compatible with `uv run mypy` and linting with `uv run ruff check .`.


---
## Stage 2 check (orchestrator)

**PASS**

- (no problems found)
