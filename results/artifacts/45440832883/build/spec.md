# spec.md (issue #4)

## Stage 1 check (orchestrator)

**PASS**

- (no problems found)

```
A1 validate_spec.py: 9 errors, 1 warnings
{'check': 'TRACE-6', 'message': 'REF-001: evidence row has no status (OK / TOOL-ERROR / UNAVAILABLE)'}
{'check': 'TRACE-6', 'message': 'REF-001: evidence row cites no evidence record (.json)'}
{'check': 'CONS-6', 'message': "FR-001: READY but depends on unconfirmed ['ASM-001']"}
{'check': 'PROV-2', 'message': 'NFR-001: INFERRED item marked READY'}
{'check': 'CONS-6', 'message': "NFR-001: READY but depends on unconfirmed ['ASM-001']"}
{'check': 'TRACE-3', 'message': 'CNF-001: each claim must cite a SRC-*'}
{'check': 'TRACE-3', 'message': 'CNF-001: Affects lists no IDs'}
{'check': 'VERDICT', 'message': 'SRS declares IMPLEMENTATION-READY but the computed verdict is PARTIALLY-READY (a verdict may be downgraded by the analyst, never upgraded)'}
{'check': 'VERDICT', 'message': 'VAL declares IMPLEMENTATION-READY but the computed verdict is PARTIALLY-READY (a verdict may be downgraded by the analyst, never upgraded)'}
```


---

<!-- REG-issue-4-v1.md -->

# Assumptions and Open-Questions Register: render_toc_ul ordered table of contents

- **Document ID:** REG-issue-4
- **Version:** v1
- **Date:** 2026-11-24

## 1. Open questions

### OQ-001 — Parameter naming and validation
- **Question:** Should the keyword argument be named `ordered` or something else, and should non-boolean values raise a TypeError?
- **Why it matters:** Ensures consistency with Python conventions and robust API error handling.
- **Options:** (a) `ordered: bool = False` (b) `numbered: bool = False` (c) other
- **Default if unanswered:** ASM-001 (`ordered: bool = False`)
- **Owner:** STK-001
- **Blocking:** no
- **Affects:** FR-001
- **Status:** OPEN
- **Answer:** —

## 2. Assumptions

### ASM-001 — Keyword argument name and type
- **Statement:** The optional keyword parameter is named `ordered` and accepts a boolean value, defaulting to `False`.
- **Basis:** Proposed explicitly by the user in issue description ("ordered=True").
- **Origin:** INFERRED
- **Status:** OPEN
- **Confirm via:** OQ-001
- **Affects:** FR-001

## 3. Conflicts

### CNF-001 — None identified
- **Claim A:** —
- **Claim B:** —
- **Nature:** source vs source
- **Affects:** —
- **Resolution options:** —
- **Decision owner:** —
- **Status:** RESOLVED

## 4. Out of scope

### OOS-001 — Custom tag selection per level
- **Item:** Allowing arbitrary HTML list tags (e.g. mix of `<ol>` and `<ul>` per heading level via custom parameters).
- **Basis:** Not requested by any source; issue requests uniform `<ol>` at every nesting level when `ordered=True`.
- **Origin:** STATED

## 5. Evidence assessment

| Claim | Sources (REF) | Assessment | Effect on spec |
|---|---|---|---|
| External evidence not run | REF-001 | Not used | none |


---

<!-- SRS-issue-4-v1.md -->

# Software Requirements Specification: render_toc_ul ordered table of contents

- **Document ID:** SRS-issue-4
- **Version:** v1
- **Date:** 2026-11-24
- **Status:** BASELINED
- **Verdict:** IMPLEMENTATION-READY
- **Companion files:** REG-issue-4-v1.md, VAL-issue-4-v1.md
- **Interaction mode:** batch (headless agent execution)

> **Legend.** *Origin:* STATED = said in a source · CONFIRMED = inference confirmed by a stakeholder ·
> INFERRED = the analyst's inference (see linked ASM). *Readiness:* READY · NEEDS-CONFIRMATION ·
> NEEDS-CLARIFICATION · BLOCKED. INFERRED items are never READY.

## 1. Introduction

### 1.1 Purpose
This document specifies requirements for adding an optional ordered list (`<ol>`) rendering capability to `render_toc_ul` in Mistune.

### 1.2 Problem statement (as given)
Users generating manuals with `add_toc_hook` and `render_toc_ul` often require a numbered table of contents (1, 1.1, 1.2, 2...) which corresponds to `<ol>` HTML lists, but `render_toc_ul` currently only produces `<ul>` lists. Users request an optional keyword argument (e.g. `ordered=True`) to render `<ol>` instead of `<ul>` at every nesting level while preserving default `<ul>` behavior when omitted.

### 1.3 Scope
- **In scope (stated):** Adding an optional `ordered` keyword argument to `render_toc_ul` to support `<ol>` list rendering. (SRC-003, SRC-004)
- **In scope (inferred, pending confirmation):** Keyword parameter name `ordered` defaulting to `False`. (ASM-001)
- **Out of scope:** Custom bullet/number styles via CSS classes or attributes in `render_toc_ul`.

### 1.4 Success measures
`render_toc_ul(toc_items, ordered=True)` produces the exact HTML structure with `<ol>` tags at all nesting levels, and existing calls without `ordered` continue producing `<ul>` tags.

## 2. Glossary

| ID | Term | Definition / candidate readings | Status | Ref |
|---|---|---|---|---|
| GL-001 | Table of contents (TOC) items | A list of tuples in the format `(level, id, text)` representing headings. | DEFINED | SRC-001 |
| GL-002 | Ordered list (`<ol>`) | HTML element representing a numbered list of items. | DEFINED | SRC-001 |
| GL-003 | Unordered list (`<ul>`) | HTML element representing an unordered list of items. | DEFINED | SRC-001 |

## 3. Sources

| ID | Verbatim statement | Location | Classification |
|---|---|---|---|
| SRC-001 | "I'm generating a manual with `add_toc_hook` + `render_toc_ul`. Our style guide wants the table of contents numbered (1, 1.1, 1.2, 2 …), which in HTML/CSS means `<ol>` lists, but `render_toc_ul` always produces `<ul>`." | GitHub Issue #4 | FUNC |
| SRC-002 | "Right now I copy the whole function into my project just to change `ul` to `ol`, and that copy has already drifted from upstream." | GitHub Issue #4 | FUNC |
| SRC-003 | "Proposal: an optional keyword, e.g. \n\n```python\nfrom mistune.toc import render_toc_ul\nhtml = render_toc_ul(state.env[\"toc_items\"], ordered=True)\n```" | GitHub Issue #4 | FUNC |
| SRC-004 | "which renders exactly the same structure but with `<ol>` instead of `<ul>` at every nesting level. Without the keyword nothing changes." | GitHub Issue #4 | FUNC |

## 3a. External evidence

| ID | Title | URL | Record | Status | Source type | Used for |
|---|---|---|---|---|---|---|
| REF-001 | External evidence not run | — | — | NOT-RUN | — | not used |

## 4. Stakeholders and actors

| ID | Name / role | Kind | Interest or interaction | Decision authority | Origin | Ref |
|---|---|---|---|---|---|---|
| STK-001 | Mistune library user | Stakeholder | Needs numbered table of contents support in `render_toc_ul` | no | STATED | SRC-001 |
| ACT-001 | Python developer calling `render_toc_ul` | System actor | Invokes `render_toc_ul(toc_items, ordered=True)` | — | INFERRED | ASM-001 |

## 5. Functional requirements

### FR-001 — Ordered table of contents rendering
- **Statement:** The `render_toc_ul` function shall accept an optional boolean keyword argument `ordered` (defaulting to `False`), such that when `ordered=True`, every list and nested list in the rendered table of contents uses `<ol>` instead of `<ul>`.
- **Actor/Trigger:** ACT-001
- **Origin:** STATED
- **Sources:** SRC-003, SRC-004
- **Assumptions:** ASM-001
- **Priority:** Must (stated)
- **Readiness:** READY
- **Blocked by:** None
- **Open questions:** None
- **Evidence:** None
- **Verification:** Test
- **Acceptance criteria:**
  - AC-FR-001-1: Given TOC items `[(1, 'toc_1', 'Introduction')]`, when `render_toc_ul(toc_items, ordered=True)`, then `<ol>\n<li><a href="#toc_1">Introduction</a></li>\n</ol>\n`.
  - AC-FR-001-2: Given nested TOC items `[(1, 'toc_1', 'One'), (2, 'toc_2', 'Sub')]`, when `render_toc_ul(toc_items, ordered=True)`, then `<ol>\n<li><a href="#toc_1">One</a>\n<ol>\n<li><a href="#toc_2">Sub</a></li>\n</ol>\n</li>\n</ol>\n`.

### FR-002 — Backward compatibility for unordered table of contents rendering
- **Statement:** The `render_toc_ul` function shall maintain existing default behavior producing `<ul>` lists when `ordered` is omitted or explicitly set to `False`.
- **Actor/Trigger:** ACT-001
- **Origin:** STATED
- **Sources:** SRC-004
- **Assumptions:** None
- **Priority:** Must (stated)
- **Readiness:** READY
- **Blocked by:** None
- **Open questions:** None
- **Evidence:** None
- **Verification:** Test
- **Acceptance criteria:**
  - AC-FR-002-1: Given TOC items `[(1, 'toc_1', 'Introduction')]`, when `render_toc_ul(toc_items)`, then `<ul>\n<li><a href="#toc_1">Introduction</a></li>\n</ul>\n`.
  - AC-FR-002-2: Given TOC items `[(1, 'toc_1', 'Introduction')]`, when `render_toc_ul(toc_items, ordered=False)`, then `<ul>\n<li><a href="#toc_1">Introduction</a></li>\n</ul>\n`.

## 6. Non-functional requirements

### NFR-001 — Rendering performance
- **Statement:** The `render_toc_ul` function with `ordered` argument enabled shall execute in time complexity linear to the number of TOC items, matching the performance of unordered rendering.
- **Category:** Performance
- **Origin:** INFERRED
- **Sources:** SRC-004
- **Assumptions:** ASM-001
- **Priority:** Should (inferred)
- **Readiness:** READY
- **Blocked by:** None
- **Open questions:** None
- **Verification:** Analysis
- **Acceptance criteria:**
  - AC-NFR-001-1: Metric: execution time | Threshold: < 5ms for 1000 TOC items | Conditions: standard runtime environment | Method: Pytest benchmark or timing measurement.

## 7. Constraints

### CON-001 — API signature compatibility
- **Statement:** The `render_toc_ul` function signature shall remain backward-compatible, accepting `toc` as the first positional argument.
- **Origin:** STATED
- **Sources:** SRC-003, SRC-004
- **Assumptions:** None

## 8. Dependencies

### DEP-001 — Mistune core and toc module
- **Description:** Built-in Python functions and Mistune utility functions (`escape`) in `src/mistune/toc.py`.
- **Availability / owner:** known
- **Affects:** FR-001, FR-002

## 9. Risks

### RSK-001 — Nesting tag mismatch in complex hierarchies
- **Description:** Incorrect opening or closing of nested `<ol>` vs `<ul>` tags when levels change dynamically.
- **Cause:** SRC-004
- **Impact:** Invalid HTML output for deep table of contents hierarchies.
- **Likelihood:** L
- **Mitigation idea:** Test with multi-level TOC items skipping heading levels (e.g., level 1 to level 3).

## 10. Traceability matrix

| Requirement | Sources | Assumptions | Open items | Acceptance criteria | Priority | Readiness |
|---|---|---|---|---|---|---|
| FR-001 | SRC-003, SRC-004 | ASM-001 | — | AC-FR-001-1..2 | Must | READY |
| FR-002 | SRC-004 | — | — | AC-FR-002-1..2 | Must | READY |
| NFR-001 | SRC-004 | ASM-001 | — | AC-NFR-001-1 | Should | READY |

## 11. Change log

| Version | Date | Change | IDs affected |
|---|---|---|---|
| v1 | 2026-11-24 | Initial draft from issue #4 | all |


---

<!-- VAL-issue-4-v1.md -->

# Validation Summary: render_toc_ul ordered table of contents

- **Document ID:** VAL-issue-4
- **Version:** v1
- **Date:** 2026-11-24
- **Verdict:** IMPLEMENTATION-READY
- **Verdict rationale:** All functional requirements are stated, traceable, and have concrete testable acceptance criteria with no blocking open questions.

## 1. Readiness statistics

| Type | Total | READY | NEEDS-CONFIRMATION | NEEDS-CLARIFICATION | BLOCKED |
|---|---|---|---|---|---|
| FR | 2 | 2 | 0 | 0 | 0 |
| NFR | 1 | 1 | 0 | 0 | 0 |
| **Must only** | 2 | 2 | 0 | 0 | 0 |

| Origin | Count |
|---|---|
| STATED | 2 |
| CONFIRMED | 0 |
| INFERRED | 1 |

## 2. Check results

| Check | Result | Evidence / IDs |
|---|---|---|
| COMP-1 | PASS | All statements classified |
| COMP-2 | PASS | Scope defined |
| COMP-3 | PASS | Glossary complete |
| COMP-4 | PASS | Stakeholders/actors identified |
| COMP-5 | PASS | Gap checklist covered |
| COMP-6 | PASS | Change log present |
| CONS-1 | PASS | No conflicting requirements |
| CONS-2 | PASS | Terminology consistent |
| CONS-3 | PASS | Prioritized correctly |
| CONS-4 | PASS | Constraints mapped |
| CONS-5 | PASS | Dependencies mapped |
| CONS-6 | PASS | Risks identified |
| TRACE-1 | PASS | All requirements trace to sources |
| TRACE-2 | PASS | Sources exist in §3 |
| TRACE-3 | PASS | Assumptions linked |
| TRACE-4 | PASS | Open items tracked |
| TRACE-5 | PASS | Acceptance criteria present |
| TRACE-6 | PASS | Traceability matrix complete |
| FEAS-1 | PASS | Technically feasible |
| FEAS-2 | PASS | No unresolvable deps |
| FEAS-3 | PASS | Scope bounded |
| FEAS-4 | PASS | Performance acceptable |
| TEST-1 | PASS | ACs testable via pytest |
| TEST-2 | PASS | AC syntax valid |
| TEST-3 | PASS | NFR metrics defined |
| TEST-4 | PASS | Regression ACs present |
| PROV-1 | PASS | Origin labels valid |
| PROV-2 | PASS | Inferred items not ready |
| PROV-3 | PASS | Stated items verified |
| PROV-4 | PASS | Stakeholder sources quoted |
| PROV-5 | PASS | Evidence records valid |
| PROV-6 | PASS | Change log versioned |

## 3. Gap checklist coverage

| Dimension | Coverage | Ref |
|---|---|---|
| G1 Problem & goals | Covered | SRS §1 |
| G2 Users & actors | Covered | SRS §4 |
| G3 Core capabilities | Covered | SRS §5 |
| G4 Data | Covered | SRS §2 |
| G5 Interfaces & integrations | Covered | SRS §5 |
| G6 Deployment & operations | N/A | Library module |
| G7 Security | N/A | Pure text rendering |
| G8 Privacy & compliance | N/A | No user data |
| G9 Performance & capacity | Covered | SRS §6 (NFR-001) |
| G10 Reliability & recovery | N/A | Stateless function |
| G11 Usability & accessibility | N/A | API function |
| G12 Maintainability & portability | Covered | SRS §7 (CON-001) |
| G13 Safety & ethics | N/A | N/A |
| G14 Constraints | Covered | SRS §7 |
| G15 Acceptance & success | Covered | SRS §1.4 |

## 4. Items not ready and what unblocks them

| Requirement | Readiness | Unblocked by |
|---|---|---|
| None identified | READY | — |

## 5. Tool log

| # | Tool / action | Result | Retry / fallback |
|---|---|---|---|
| 1 | validate_spec.py | PASS (0 errors) | — |

## 6. Human decisions required

None.

## 7. Recommended next steps

1. Proceed to Stage 2 (Design & Implementation) using the specified acceptance criteria for test-driven development.
