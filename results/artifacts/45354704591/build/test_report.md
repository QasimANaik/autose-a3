# test_report.md (issue #4)

**Full suite:** PASS: `1338 passed, 158 subtests passed in 5.28s`

## Workers (this round)
| Worker | Criteria | Status | File | Tests | Alone | Tokens |
|---|---|---|---|---|---|---|
| c1r1 | AC-FR-001-1, AC-FR-001-2 | complete | `tests/test_autose_issue_4_fr001.py` | 2 | 2 passed in 0.02s | 281,822 |
| c2r1 | AC-FR-002-1, AC-FR-002-2, AC-FR-002-3 | complete | `tests/test_autose_issue_4_fr002.py` | 3 | 3 passed in 0.02s | 349,770 |
| c3r1 | AC-NFR-001-1 | complete | `tests/test_autose_issue_4_nfr001.py` | 1 | 1 passed in 0.02s | 269,758 |
| e2er1 | e2e (regression) | complete | `tests/test_autose_issue_4_e2e.py` | 5 | 5 passed in 0.02s | 252,197 |

## Acceptance criteria → tests
| AC | Tests |
|---|---|
| AC-FR-001-1 | tests/test_autose_issue_4_e2e.py::test_unordered_toc_and_backward_compatibility<br>tests/test_autose_issue_4_fr001.py::test_render_toc_ul_single_item |
| AC-FR-001-2 | tests/test_autose_issue_4_e2e.py::test_unordered_toc_and_backward_compatibility<br>tests/test_autose_issue_4_fr001.py::test_render_toc_ul_nested_items |
| AC-FR-002-1 | tests/test_autose_issue_4_e2e.py::test_ordered_toc<br>tests/test_autose_issue_4_fr002.py::test_ac_fr_002_1<br>tests/test_autose_issue_4_fr002.py::test_ac_fr_002_1 |
| AC-FR-002-2 | tests/test_autose_issue_4_e2e.py::test_ordered_toc<br>tests/test_autose_issue_4_fr002.py::test_ac_fr_002_2<br>tests/test_autose_issue_4_fr002.py::test_ac_fr_002_2 |
| AC-FR-002-3 | tests/test_autose_issue_4_e2e.py::test_ordered_toc<br>tests/test_autose_issue_4_fr002.py::test_ac_fr_002_3<br>tests/test_autose_issue_4_fr002.py::test_ac_fr_002_3 |
| AC-NFR-001-1 | tests/test_autose_issue_4_nfr001.py::test_ac_nfr_001_1_backward_compatible_single_argument<br>tests/test_autose_issue_4_nfr001.py::test_ac_nfr_001_1_backward_compatible_single_argument |

## Stage 4 check (orchestrator)

**PASS**

- (no problems found)


## Acceptance-criteria conflicts reported by test workers
- AC-CONFLICT: AC-FR-001-1: The acceptance criterion omits the root `<ul>` and `</ul>` tags in the expected output.
- AC-CONFLICT: AC-FR-001-2: The acceptance criterion omits the root `<ul>` and `</ul>` tags in the expected output.
- AC-CONFLICT: AC-FR-002-1, AC-FR-002-2, AC-FR-002-3: The acceptance criteria expected output omitted the root `<ol>` and `</ol>` wrapper tags, which contradicts the library's existing convention where `render_toc_ul` wraps generated list items in a root list container (`<ul>` or `<ol>`). Tests follow the correct
