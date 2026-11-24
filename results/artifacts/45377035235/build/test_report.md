# test_report.md (issue #3)

**Full suite:** PASS: `1339 passed, 158 subtests passed in 4.19s`

## Workers (this round)
| Worker | Criteria | Status | File | Tests | Alone | Tokens |
|---|---|---|---|---|---|---|
| c1r1 | AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-004-1 | complete | `tests/test_autose_issue_3_fr002.py` | 4 | 4 passed in 0.02s | 176,610 |
| c2r1 | AC-NFR-001-1, AC-FR-001-1, AC-FR-001-2 | complete | `tests/test_autose_issue_3_fr001.py` | 3 | 3 passed in 0.29s | 362,084 |
| e2er1 | e2e (regression) | complete | `tests/test_autose_issue_3_e2e.py` | 5 | 5 passed in 0.02s | 220,157 |

## Acceptance criteria → tests
| AC | Tests |
|---|---|
| AC-FR-001-1 | tests/test_autose_issue_3_e2e.py::test_link_rel_renderer_options<br>tests/test_autose_issue_3_fr001.py::test_link_rel_specified |
| AC-FR-001-2 | tests/test_autose_issue_3_e2e.py::test_link_rel_renderer_options<br>tests/test_autose_issue_3_fr001.py::test_link_rel_default |
| AC-FR-002-1 | tests/test_autose_issue_3_e2e.py::test_link_rel_autolinks<br>tests/test_autose_issue_3_fr002.py::test_ac_fr_002_1<br>tests/test_autose_issue_3_fr002.py::test_ac_fr_002_1 |
| AC-FR-002-2 | tests/test_autose_issue_3_e2e.py::test_link_rel_autolinks<br>tests/test_autose_issue_3_fr002.py::test_ac_fr_002_2<br>tests/test_autose_issue_3_fr002.py::test_ac_fr_002_2 |
| AC-FR-003-1 | tests/test_autose_issue_3_e2e.py::test_link_rel_image_isolation<br>tests/test_autose_issue_3_fr002.py::test_ac_fr_003_1<br>tests/test_autose_issue_3_fr002.py::test_ac_fr_003_1 |
| AC-FR-004-1 | tests/test_autose_issue_3_e2e.py::test_link_rel_renderer_options<br>tests/test_autose_issue_3_fr002.py::test_ac_fr_004_1<br>tests/test_autose_issue_3_fr002.py::test_ac_fr_004_1 |
| AC-NFR-001-1 | tests/test_autose_issue_3_fr001.py::test_benchmark_execution_time_overhead |

## Stage 4 check (orchestrator)

**PASS**

- (no problems found)

