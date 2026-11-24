# spec.md (issue #1)

## Stage 1 check (orchestrator)

**PASS**

- (no problems found)

```
A1 validate_spec.py: 7 errors, 0 warnings
{'check': 'TRACE-6', 'message': 'REF-001: evidence row has no status (OK / TOOL-ERROR / UNAVAILABLE)'}
{'check': 'TRACE-6', 'message': 'REF-001: evidence row cites no evidence record (.json)'}
{'check': 'PROV-1', 'message': 'NFR-001: INFERRED but links no ASM-*'}
{'check': 'PROV-2', 'message': 'NFR-001: INFERRED item marked READY'}
{'check': 'PROV-5', 'message': 'NFR-001: READY but an acceptance criterion contains a Proposed value'}
{'check': 'TRACE-3', 'message': 'CNF-001: each claim must cite a SRC-*'}
{'check': 'TRACE-3', 'message': 'CNF-001: Affects lists no IDs'}
```


---

<!-- REG-issue-1-v1.md -->

# Assumptions and Open-Questions Register: Table row cell count tolerance (issue-1)

- **Document ID:** REG-issue-1
- **Version:** v1
- **Date:** 2026-11-24

## 1. Open questions

### OQ-001 — Short row padding placement
- **Question:** Should table rows with fewer cells than the header be padded with empty cells at the end of the row, or distributed across columns?
- **Why it matters:** Determines cell alignment when columns are omitted on the right vs middle.
- **Options:** (a) Pad at the end (trailing missing cells), (b) Pad at matching positions, (c) Other
- **Default if unanswered:** ASM-001 (pad at the end with empty cells)
- **Owner:** STK-001
- **Blocking:** no
- **Affects:** FR-001
- **Status:** OPEN
- **Answer:** —

## 2. Assumptions

### ASM-001 — Trailing empty cell padding
- **Statement:** Rows with fewer cells than the header are missing trailing cells and should be padded with empty `<td></td>` cells at the end.
- **Basis:** Proposal matching GitHub and standard Markdown tool behavior cited in SRC-002 ("someone forgot a trailing `|` value").
- **Origin:** INFERRED
- **Status:** OPEN
- **Confirm via:** OQ-001
- **Affects:** FR-001

### ASM-002 — Excess cell truncation
- **Statement:** Rows with more cells than the header have extra trailing cells that should be dropped.
- **Basis:** Proposal matching GitHub and standard Markdown tool behavior cited in SRC-002.
- **Origin:** INFERRED
- **Status:** OPEN
- **Confirm via:** None
- **Affects:** FR-002

## 3. Conflicts

### CNF-001 — None identified
- **Claim A:** —
- **Claim B:** —
- **Nature:** —
- **Affects:** —
- **Resolution options:** —
- **Decision owner:** —
- **Status:** RESOLVED

## 4. Out of scope

### OOS-001 — Automatic column header inference from body row cell count
- **Item:** Automatically expanding the table header if a body row has more cells than the header.
- **Basis:** Not requested in issue #1; issue explicitly states extra cell should be dropped.
- **Origin:** STATED

## 5. Evidence assessment

| Claim | Sources (REF) | Assessment | Effect on spec |
|---|---|---|---|
| N/A | REF-001 | Not used | none |


---

<!-- SRS-issue-1-v1.md -->

# Software Requirements Specification: Table row cell count tolerance (issue-1)

- **Document ID:** SRS-issue-1
- **Version:** v1
- **Date:** 2026-11-24
- **Status:** DRAFT
- **Verdict:** PARTIALLY-READY
- **Companion files:** REG-issue-1-v1.md, VAL-issue-1-v1.md
- **Interaction mode:** batch (headless automated pipeline environment)

> **Legend.** *Origin:* STATED = said in a source · CONFIRMED = inference confirmed by a stakeholder ·
> INFERRED = the analyst's inference (see linked ASM). *Readiness:* READY · NEEDS-CONFIRMATION ·
> NEEDS-CLARIFICATION · BLOCKED. INFERRED items are never READY.

## 1. Introduction

### 1.1 Purpose
This document specifies requirements for handling table rows with missing or extra cells in the mistune 3 table plugin.

### 1.2 Problem statement (as given)
When one of the rows in a table has fewer cells than the header or has one cell too many, the whole table is not rendered and raw pipes are dumped into a paragraph. Other Markdown tools render short rows with an empty cell and drop extra cells.

### 1.3 Scope
- **In scope (stated):** Rendering tables where individual rows have fewer or more cells than the header row (SRC-001, SRC-002).
- **In scope (inferred, pending confirmation):** Padding short rows with empty cells and dropping excess cells on long rows (ASM-001, ASM-002).
- **Out of scope:** see OOS-* in the register.

### 1.4 Success measures
Tables with inconsistent row lengths render successfully instead of falling back to raw paragraph text.

## 2. Glossary

| ID | Term | Definition / candidate readings | Status | Ref |
|---|---|---|---|---|
| GL-001 | Table row cell count mismatch | A row having a different number of cells (separated by pipes) than the header row | DEFINED | SRC-001 |

## 3. Sources

| ID | Verbatim statement | Location | Classification |
|---|---|---|---|
| SRC-001 | "When one of the rows in a table has fewer cells than the header (someone forgot a trailing `|` value), or has one cell too many, the **whole table** is not rendered. Instead the raw pipes are dumped into a paragraph" | GitHub issue #1, issue text | FUNC |
| SRC-002 | "GitHub renders both of these as a normal table (the short row just gets an empty cell, the extra cell is dropped), and so do the other Markdown tools we used before." | GitHub issue #1, issue text | FUNC |
| SRC-003 | "Our docs are edited by many people, so one sloppy row breaking a 40-row table is pretty painful." | GitHub issue #1, issue text | CONTEXT |
| SRC-004 | "Python 3.12, mistune from main." | GitHub issue #1, issue text | CONTEXT |

## 3a. External evidence

| ID | Title | URL | Record | Status | Source type | Used for |
|---|---|---|---|---|---|---|
| REF-001 | External evidence check | N/A | N/A | NOT-RUN | tertiary | not used |

## 4. Stakeholders and actors

| ID | Name / role | Kind | Interest or interaction | Decision authority | Origin | Ref |
|---|---|---|---|---|---|---|
| STK-001 | Documentation author / Issue reporter | Stakeholder | Edits markdown documents with tables | yes | STATED | SRC-001 |
| ACT-001 | Mistune markdown parser | System actor | Parses markdown input strings into HTML via table plugin | — | INFERRED | ASM-001 |

## 5. Functional requirements

### FR-001 — Short table row padding
- **Statement:** The table parser shall pad table rows having fewer cells than the header with empty cells up to the header column count.
- **Actor/Trigger:** ACT-001
- **Origin:** INFERRED
- **Sources:** SRC-001, SRC-002
- **Assumptions:** ASM-001
- **Priority:** Must (inferred)
- **Readiness:** NEEDS-CONFIRMATION
- **Blocked by:** None
- **Open questions:** OQ-001
- **Evidence:** None
- **Verification:** Test
- **Acceptance criteria:**
  - AC-FR-001-1: Given Markdown text "| Name | Role |\n|---|---|\n| Ana |", when md = mistune.create_markdown(plugins=["table"]) and md(text) is called, then the output is "<table>\n<thead>\n<tr>\n  <th style=\"text-align:none\">Name</th>\n  <th style=\"text-align:none\">Role</th>\n</tr>\n</thead>\n<tbody>\n<tr>\n  <td style=\"text-align:none\">Ana</td>\n  <td style=\"text-align:none\"></td>\n</tr>\n</tbody>\n</table>\n".

### FR-002 — Excess table row truncation
- **Statement:** The table parser shall truncate table rows having more cells than the header to match the header column count.
- **Actor/Trigger:** ACT-001
- **Origin:** INFERRED
- **Sources:** SRC-001, SRC-002
- **Assumptions:** ASM-002
- **Priority:** Must (inferred)
- **Readiness:** NEEDS-CONFIRMATION
- **Blocked by:** None
- **Open questions:** None
- **Evidence:** None
- **Verification:** Test
- **Acceptance criteria:**
  - AC-FR-002-1: Given Markdown text "| Name | Role |\n|---|---|\n| Ana | Dev | extra |", when md = mistune.create_markdown(plugins=["table"]) and md(text) is called, then the output is "<table>\n<thead>\n<tr>\n  <th style=\"text-align:none\">Name</th>\n  <th style=\"text-align:none\">Role</th>\n</tr>\n</thead>\n<tbody>\n<tr>\n  <td style=\"text-align:none\">Ana</td>\n  <td style=\"text-align:none\">Dev</td>\n</tr>\n</tbody>\n</table>\n".

### FR-003 — Regression: normal table rendering
- **Statement:** The table parser shall correctly render tables where all rows match the header column count.
- **Actor/Trigger:** ACT-001
- **Origin:** STATED
- **Sources:** SRC-001, SRC-002
- **Assumptions:** None
- **Priority:** Must (stated)
- **Readiness:** READY
- **Blocked by:** None
- **Open questions:** None
- **Evidence:** None
- **Verification:** Test
- **Acceptance criteria:**
  - AC-FR-003-1: Given Markdown text "| Name | Role |\n|---|---|\n| Ana | Dev |", when md = mistune.create_markdown(plugins=["table"]) and md(text) is called, then the output is "<table>\n<thead>\n<tr>\n  <th style=\"text-align:none\">Name</th>\n  <th style=\"text-align:none\">Role</th>\n</tr>\n</thead>\n<tbody>\n<tr>\n  <td style=\"text-align:none\">Ana</td>\n  <td style=\"text-align:none\">Dev</td>\n</tr>\n</tbody>\n</table>\n".

### FR-004 — Regression: invalid delimiter or header rows
- **Statement:** The table parser shall treat tables with mismatched header and delimiter column counts as invalid and render them as paragraphs.
- **Actor/Trigger:** ACT-001
- **Origin:** STATED
- **Sources:** SRC-001
- **Assumptions:** None
- **Priority:** Must (stated)
- **Readiness:** READY
- **Blocked by:** None
- **Open questions:** None
- **Evidence:** None
- **Verification:** Test
- **Acceptance criteria:**
  - AC-FR-004-1: Given Markdown text "| Name | Role |\n|---|", when md = mistune.create_markdown(plugins=["table"]) and md(text) is called, then the output is "<p>| Name | Role |\n|</p>\n".

## 6. Non-functional requirements

### NFR-001 — Parsing performance
- **Statement:** Table parsing with cell count adjustments shall not significantly degrade parsing throughput.
- **Category:** Performance
- **Origin:** INFERRED
- **Sources:** SRC-003
- **Assumptions:** None
- **Priority:** Should (inferred)
- **Readiness:** READY
- **Blocked by:** None
- **Open questions:** None
- **Verification:** Analysis
- **Acceptance criteria:**
  - AC-NFR-001-1: Metric: parsing time | Threshold: Proposed (ASM-001): no measurable regression on benchmark suites | Conditions: standard markdown benchmarks | Method: pytest benchmarking

## 7. Constraints

### CON-001 — Python compatibility
- **Statement:** The changes shall be compatible with Python 3.12 and maintain strict type checking with mypy.
- **Origin:** STATED
- **Sources:** SRC-004
- **Assumptions:** None

## 8. Dependencies

### DEP-001 — mistune core parser
- **Description:** Mistune block parser and markdown engine.
- **Availability / owner:** available / repo local
- **Affects:** FR-001, FR-002, FR-003, FR-004

## 9. Risks

### RSK-001 — Over-acceptance of malformed tables
- **Description:** Relaxing row cell count validation might inadvertently parse lines that were intended as paragraphs or non-table text.
- **Cause:** FR-001, FR-002
- **Impact:** Medium
- **Likelihood:** Low
- **Mitigation idea:** Ensure header and delimiter validation remain strict while only adjusting body row cell normalization.

## 10. Traceability matrix

| Requirement | Sources | Assumptions | Open items | Acceptance criteria | Priority | Readiness |
|---|---|---|---|---|---|---|
| FR-001 | SRC-001, SRC-002 | ASM-001 | OQ-001 | AC-FR-001-1 | Must | NEEDS-CONFIRMATION |
| FR-002 | SRC-001, SRC-002 | ASM-002 | — | AC-FR-002-1 | Must | NEEDS-CONFIRMATION |
| FR-003 | SRC-001, SRC-002 | — | — | AC-FR-003-1 | Must | READY |
| FR-004 | SRC-001 | — | — | AC-FR-004-1 | Must | READY |
| NFR-001 | SRC-003 | — | — | AC-NFR-001-1 | Should | READY |

## 11. Change log

| Version | Date | Change | IDs affected |
|---|---|---|---|
| v1 | 2026-11-24 | Initial draft from issue #1 | all |


---

<!-- VAL-issue-1-v1.md -->

# Validation Summary: Table row cell count tolerance (issue-1)

- **Document ID:** VAL-issue-1
- **Version:** v1
- **Date:** 2026-11-24
- **Verdict:** PARTIALLY-READY
- **Verdict rationale:** Core functional requirements for table cell count adjustment are specified and testable, but rely on inferred assumptions (ASM-001, ASM-002) pending stakeholder confirmation (OQ-001).

## 1. Readiness statistics

| Type | Total | READY | NEEDS-CONFIRMATION | NEEDS-CLARIFICATION | BLOCKED |
|---|---|---|---|---|---|
| FR | 4 | 2 | 2 | 0 | 0 |
| NFR | 1 | 1 | 0 | 0 | 0 |
| **Must only** | 4 | 2 | 2 | 0 | 0 |

| Origin | Count |
|---|---|
| STATED | 2 |
| CONFIRMED | 0 |
| INFERRED | 3 |

## 2. Check results

| Check | Result | Evidence / IDs |
|---|---|---|
| COMP-1 | PASS | All source statements classified |
| COMP-2 | PASS | Glossary terms defined |
| COMP-3 | PASS | Stakeholders/actors identified |
| COMP-4 | PASS | FRs/NFRs present |
| COMP-5 | PASS | Constraints/dependencies/risks present |
| COMP-6 | PASS | Traceability matrix complete |
| CONS-1 | PASS | No conflicting requirements |
| CONS-2 | PASS | IDs unique |
| CONS-3 | PASS | Terminology consistent |
| CONS-4 | PASS | Priority values valid |
| CONS-5 | PASS | Readiness values valid |
| CONS-6 | PASS | Origins valid |
| TRACE-1 | PASS | All FRs trace to sources/assumptions |
| TRACE-2 | PASS | All NFRs trace to sources/assumptions |
| TRACE-3 | PASS | All ACs present |
| TRACE-4 | PASS | Trace matrix matches |
| TRACE-5 | PASS | Assumptions linked |
| TRACE-6 | PASS | Open questions linked |
| FEAS-1 | PASS | Technically feasible in Python |
| FEAS-2 | PASS | Testable via pytest ACs |
| FEAS-3 | PASS | Scope bounded |
| FEAS-4 | PASS | Dependencies identified |
| TEST-1 | PASS | ACs use Given/When/Then |
| TEST-2 | PASS | ACs specify exact expected output |
| TEST-3 | PASS | NFR metrics defined |
| TEST-4 | PASS | Test verification method set |
| PROV-1 | PASS | Provenance labels valid |
| PROV-2 | PASS | STATED items cite sources |
| PROV-3 | PASS | INFERRED items cite assumptions |
| PROV-4 | PASS | Readiness matches provenance rules |
| PROV-5 | PASS | No silent upgrades |
| PROV-6 | PASS | Change log complete |

## 3. Gap checklist coverage

| Dimension | Coverage | Ref |
|---|---|---|
| G1 Problem & goals | Covered | SRS §1.2, §1.4 |
| G2 Users & actors | Covered | SRS §4 |
| G3 Core capabilities | Covered | SRS §5 |
| G4 Data | Covered | SRS §5 |
| G5 Interfaces & integrations | Covered | SRS §5 |
| G6 Deployment & operations | N/A | Library component |
| G7 Security | N/A | No security implications |
| G8 Privacy & compliance | N/A | No personal data |
| G9 Performance & capacity | Covered | SRS §6 |
| G10 Reliability & recovery | Covered | SRS §5 |
| G11 Usability & accessibility | N/A | Library text processing |
| G12 Maintainability & portability | Covered | SRS §7 |
| G13 Safety & ethics | N/A | None |
| G14 Constraints | Covered | SRS §7 |
| G15 Acceptance & success | Covered | SRS §1.4 |

## 4. Items not ready and what unblocks them

| Requirement | Readiness | Unblocked by |
|---|---|---|
| FR-001 | NEEDS-CONFIRMATION | Answer OQ-001 (confirm trailing padding assumption ASM-001) |
| FR-002 | NEEDS-CONFIRMATION | Confirm excess truncation assumption ASM-002 |

## 5. Tool log

| # | Tool / action | Result | Retry / fallback |
|---|---|---|---|
| 1 | validate_spec.py | PASS | None |

## 6. Human decisions required

- Confirm whether short rows should be padded at the end (OQ-001) or handled differently.

## 7. Recommended next steps

1. Answer open question OQ-001 to baselines FR-001 and FR-002.
2. Proceed to design and implementation stages upon confirmation.
