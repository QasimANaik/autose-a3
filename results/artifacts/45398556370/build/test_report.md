# test_report.md (issue #18)

**Full suite:** PASS: `1339 passed, 158 subtests passed in 8.57s`

## Workers (this round)
| Worker | Criteria | Status | File | Tests | Alone | Tokens |
|---|---|---|---|---|---|---|
| c1r1 | AC-FR-001-1, AC-FR-002-1, AC-FR-003-1, AC-FR-004-1 | complete | `tests/test_autose_issue_18_fr001.py` | 4 | 4 passed in 0.03s | 496,807 |
| c2r1 | AC-NFR-001-1, AC-NFR-002-1 | complete | `tests/test_autose_issue_18_nfr001.py` | 3 | 3 passed in 3.80s | 408,329 |
| e2er1 | e2e (regression) | complete | `tests/test_autose_issue_18_e2e.py` | 5 | 5 passed in 0.03s | 567,176 |

## Acceptance criteria → tests
| AC | Tests |
|---|---|
| AC-FR-001-1 | tests/test_autose_issue_18_e2e.py::test_url_plugin_acceptance_criteria<br>tests/test_autose_issue_18_fr001.py::test_ac_fr_001_1<br>tests/test_autose_issue_18_fr001.py::test_ac_fr_001_1 |
| AC-FR-002-1 | tests/test_autose_issue_18_e2e.py::test_url_plugin_acceptance_criteria<br>tests/test_autose_issue_18_fr001.py::test_ac_fr_002_1<br>tests/test_autose_issue_18_fr001.py::test_ac_fr_002_1 |
| AC-FR-003-1 | tests/test_autose_issue_18_e2e.py::test_url_plugin_acceptance_criteria<br>tests/test_autose_issue_18_fr001.py::test_ac_fr_003_1<br>tests/test_autose_issue_18_fr001.py::test_ac_fr_003_1 |
| AC-FR-004-1 | tests/test_autose_issue_18_e2e.py::test_url_plugin_acceptance_criteria<br>tests/test_autose_issue_18_fr001.py::test_ac_fr_004_1<br>tests/test_autose_issue_18_fr001.py::test_ac_fr_004_1 |
| AC-NFR-001-1 | tests/test_autose_issue_18_nfr001.py::test_ac_nfr_001_1<br>tests/test_autose_issue_18_nfr001.py::test_ac_nfr_001_1<br>tests/test_autose_issue_18_nfr001.py::test_url_plugin_www |
| AC-NFR-002-1 | tests/test_autose_issue_18_nfr001.py::test_ac_nfr_002_1<br>tests/test_autose_issue_18_nfr001.py::test_ac_nfr_002_1<br>tests/test_autose_issue_18_nfr001.py::test_url_plugin_www |

## Stage 4 check (orchestrator)

**PASS**

- (no problems found)

