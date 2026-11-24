# test_report.md (issue #1)

**Full suite:** PASS: `1338 passed, 158 subtests passed in 5.25s`

## Workers (this round)
| Worker | Criteria | Status | File | Tests | Alone | Tokens |
|---|---|---|---|---|---|---|
| c1r1 | AC-FR-003-1, AC-FR-004-1 | complete | `tests/test_autose_issue_1_fr003.py` | 3 | 3 passed in 0.03s | 420,117 |
| c2r1 | AC-NFR-001-1, AC-FR-001-1, AC-FR-002-1 | complete | `tests/test_autose_issue_1_fr001.py` | 3 | 3 passed in 0.12s | 476,398 |
| e2er1 | e2e (regression) | complete | `tests/test_autose_issue_1_e2e.py` | 5 | 5 passed in 0.02s | 580,660 |

## Acceptance criteria → tests
| AC | Tests |
|---|---|
| AC-FR-001-1 | tests/test_autose_issue_1_e2e.py::test_e2e_table_ac_missing_and_extra_cells<br>tests/test_autose_issue_1_fr001.py::test_ac_fr_001_1_missing_cell<br>tests/test_autose_issue_1_fr001.py::test_ac_fr_001_1_missing_cell |
| AC-FR-002-1 | tests/test_autose_issue_1_e2e.py::test_e2e_table_ac_missing_and_extra_cells<br>tests/test_autose_issue_1_fr001.py::test_ac_fr_002_1_extra_cell<br>tests/test_autose_issue_1_fr001.py::test_ac_fr_002_1_extra_cell |
| AC-FR-003-1 | tests/test_autose_issue_1_e2e.py::test_e2e_table_ac_missing_and_extra_cells<br>tests/test_autose_issue_1_fr003.py::test_ac_fr_003_1<br>tests/test_autose_issue_1_fr003.py::test_ac_fr_003_1<br>tests/test_autose_issue_1_fr003.py::test_table_row_padding_and_truncation |
| AC-FR-004-1 | tests/test_autose_issue_1_e2e.py::test_e2e_table_ac_invalid_delimiter<br>tests/test_autose_issue_1_fr003.py::test_ac_fr_004_1<br>tests/test_autose_issue_1_fr003.py::test_ac_fr_004_1 |
| AC-NFR-001-1 | tests/test_autose_issue_1_fr001.py::test_ac_nfr_001_1_table_benchmark_performance<br>tests/test_autose_issue_1_fr001.py::test_ac_nfr_001_1_table_benchmark_performance |

## Stage 4 check (orchestrator)

**PASS**

- (no problems found)


## Acceptance-criteria conflicts reported by test workers
- AC-CONFLICT: AC-FR-001-1, AC-FR-002-1: AC expected output specified `style="text-align:none"` on table cells/headers, but mistune's HTML table renderer outputs standard `<th>` and `<td>` elements without inline style attributes, matching the library's existing fixtures (`tests/fixtures/table.txt`).
- AC-CONFLICT: AC-FR-003-1: Expected output specifies `style="text-align:none"`, but mistune omits style attributes when table cell alignment is None.
- AC-CONFLICT: AC-FR-004-1: Expected output omits `---|` in paragraph fallback, whereas mistune preserves the delimiter line text when falling back to paragraph.
