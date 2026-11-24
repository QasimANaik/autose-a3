# test_report.md (issue #2)

**Full suite:** PASS: `1339 passed, 158 subtests passed in 4.65s`

## Workers (this round)
| Worker | Criteria | Status | File | Tests | Alone | Tokens |
|---|---|---|---|---|---|---|
| c1r1 | AC-FR-003-1, AC-FR-003-2, AC-FR-001-1, AC-FR-004-1 | complete | `tests/test_autose_issue_2_fr001.py` | 4 | 4 passed in 0.03s | 399,436 |
| c2r1 | AC-NFR-001-1, AC-FR-002-1, AC-FR-002-2 | complete | `tests/test_autose_issue_2_fr002.py` | 3 | 3 passed in 0.13s | 462,625 |
| e2er1 | e2e (regression) | complete | `tests/test_autose_issue_2_e2e.py` | 5 | 5 passed in 0.04s | 445,263 |

## Acceptance criteria → tests
| AC | Tests |
|---|---|
| AC-FR-001-1 | tests/test_autose_issue_2_e2e.py::test_url_plugin_acceptance_criteria_parentheses_and_punctuation<br>tests/test_autose_issue_2_e2e.py::test_url_plugin_acceptance_criteria_parentheses_and_punctuation<br>tests/test_autose_issue_2_fr001.py::test_ac_fr_001_1<br>tests/test_autose_issue_2_fr001.py::test_ac_fr_001_1 |
| AC-FR-002-1 | tests/test_autose_issue_2_e2e.py::test_url_plugin_acceptance_criteria_parentheses_and_punctuation<br>tests/test_autose_issue_2_e2e.py::test_url_plugin_acceptance_criteria_parentheses_and_punctuation<br>tests/test_autose_issue_2_fr002.py::test_url_plugin_trailing_question_mark |
| AC-FR-002-2 | tests/test_autose_issue_2_e2e.py::test_url_plugin_acceptance_criteria_parentheses_and_punctuation<br>tests/test_autose_issue_2_e2e.py::test_url_plugin_acceptance_criteria_parentheses_and_punctuation<br>tests/test_autose_issue_2_fr002.py::test_url_plugin_trailing_exclamation_mark |
| AC-FR-003-1 | tests/test_autose_issue_2_e2e.py::test_url_plugin_acceptance_criteria_parentheses_and_punctuation<br>tests/test_autose_issue_2_e2e.py::test_url_plugin_acceptance_criteria_parentheses_and_punctuation<br>tests/test_autose_issue_2_fr001.py::test_ac_fr_003_1<br>tests/test_autose_issue_2_fr001.py::test_ac_fr_003_1 |
| AC-FR-003-2 | tests/test_autose_issue_2_e2e.py::test_url_plugin_acceptance_criteria_parentheses_and_punctuation<br>tests/test_autose_issue_2_e2e.py::test_url_plugin_acceptance_criteria_parentheses_and_punctuation<br>tests/test_autose_issue_2_fr001.py::test_ac_fr_003_2<br>tests/test_autose_issue_2_fr001.py::test_ac_fr_003_2 |
| AC-FR-004-1 | tests/test_autose_issue_2_e2e.py::test_url_plugin_combined_with_other_plugins_and_brackets<br>tests/test_autose_issue_2_fr001.py::test_ac_fr_004_1<br>tests/test_autose_issue_2_fr001.py::test_ac_fr_004_1 |
| AC-NFR-001-1 | tests/test_autose_issue_2_e2e.py::test_url_plugin_performance_scaling_nfr<br>tests/test_autose_issue_2_fr002.py::test_url_plugin_performance_linear |

## Stage 4 check (orchestrator)

**PASS**

- (no problems found)

