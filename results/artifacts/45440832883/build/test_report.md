# test_report.md (issue #4)

**Full suite:** PASS: `1337 passed, 158 subtests passed in 5.36s`

## Workers (this round)
| Worker | Criteria | Status | File | Tests | Alone | Tokens |
|---|---|---|---|---|---|---|
| c1r1 | AC-FR-002-1, AC-FR-002-2 | complete | `tests/test_autose_issue_4_fr002.py` | 3 | 3 passed in 0.02s | 351,792 |
| c2r1 | AC-NFR-001-1, AC-FR-001-1, AC-FR-001-2 | complete | `tests/test_autose_issue_4_fr001.py` | 3 | 3 passed in 0.03s | 164,803 |
| e2er1 | e2e (regression) | complete | `tests/test_autose_issue_4_e2e.py` | 4 | 4 passed in 0.03s | 523,857 |

## Acceptance criteria → tests
| AC | Tests |
|---|---|
| AC-FR-001-1 | tests/test_autose_issue_4_e2e.py::test_render_toc_ul_ordered_and_unordered<br>tests/test_autose_issue_4_fr001.py::test_render_toc_ul_ordered_single |
| AC-FR-001-2 | tests/test_autose_issue_4_e2e.py::test_render_toc_ul_ordered_and_unordered<br>tests/test_autose_issue_4_fr001.py::test_render_toc_ul_ordered_nested |
| AC-FR-002-1 | tests/test_autose_issue_4_e2e.py::test_render_toc_ul_ordered_and_unordered<br>tests/test_autose_issue_4_fr002.py::test_render_toc_ul_default |
| AC-FR-002-2 | tests/test_autose_issue_4_e2e.py::test_render_toc_ul_ordered_and_unordered<br>tests/test_autose_issue_4_fr002.py::test_render_toc_ul_ordered_false<br>tests/test_autose_issue_4_fr002.py::test_render_toc_ol_ordered_true |
| AC-NFR-001-1 | tests/test_autose_issue_4_e2e.py::test_toc_performance<br>tests/test_autose_issue_4_fr001.py::test_render_toc_ul_performance_threshold |

## Stage 4 check (orchestrator)

**PASS**

- (no problems found)

