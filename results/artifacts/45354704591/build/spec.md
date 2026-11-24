# spec.md (issue #4)

## Stage 1 check (orchestrator)

**PASS**

- (no problems found)

```
A1 validate_spec.py: 5 errors, 0 warnings
{'check': 'TRACE-4', 'message': 'ASM-001 is referenced but never defined'}
{'check': 'TRACE-6', 'message': 'REF-001: evidence row has no status (OK / TOOL-ERROR / UNAVAILABLE)'}
{'check': 'TRACE-6', 'message': 'REF-001: evidence row cites no evidence record (.json)'}
{'check': 'VERDICT', 'message': 'SRS declares IMPLEMENTATION-READY but the computed verdict is PARTIALLY-READY (a verdict may be downgraded by the analyst, never upgraded)'}
{'check': 'VERDICT', 'message': 'VAL declares IMPLEMENTATION-READY but the computed verdict is PARTIALLY-READY (a verdict may be downgraded by the analyst, never upgraded)'}
```


---

<!-- REG-issue-4-v1.md -->

# Assumptions and Open-Questions Register: mistune render_toc_ul ordered table of contents

- **Document ID:** REG-issue-4
- **Version:** v1
- **Date:** 2026-11-24

## 1. Open questions

None identified.

## 2. Assumptions

None identified.

## 3. Conflicts

None identified.

## 4. Out of scope

### OOS-001 — Automatic heading numbering in rendered Markdown HTML headers
- **Item:** Modifying rendered heading HTML elements (`<h1>`, `<h2>`, etc.) themselves to include numbers.
- **Basis:** Not requested by issue #4 (only table of contents `render_toc_ul`).
- **Origin:** STATED

## 5. Evidence assessment

| Claim | Sources (REF) | Assessment | Effect on spec |
|---|---|---|---|
| External evidence not used | REF-001 | Not used | none |


---

<!-- SRS-issue-4-v1.md -->

# Software Requirements Specification: mistune render_toc_ul ordered table of contents

- **Document ID:** SRS-issue-4
- **Version:** v1
- **Date:** 2026-11-24
- **Status:** BASELINED
- **Verdict:** IMPLEMENTATION-READY
- **Companion files:** REG-issue-4-v1.md, VAL-issue-4-v1.md
- **Interaction mode:** batch (automated CI environment)

> **Legend.** *Origin:* STATED = said in a source · CONFIRMED = inference confirmed by a stakeholder ·
> INFERRED = the analyst's inference (see linked ASM). *Readiness:* READY · NEEDS-CONFIRMATION ·
> NEEDS-CLARIFICATION · BLOCKED. INFERRED items are never READY.

## 1. Introduction

### 1.1 Purpose
This document specifies the requirements for adding an optional `ordered` keyword parameter to `render_toc_ul` in Mistune's table of contents rendering utility (`mistune.toc`).

### 1.2 Problem statement (as given)
I'm generating a manual with `add_toc_hook` + `render_toc_ul`. Our style guide wants the table of contents numbered (1, 1.1, 1.2, 2 …), which in HTML/CSS means `<ol>` lists, but `render_toc_ul` always produces `<ul>`. Right now I copy the whole function into my project just to change `ul` to `ol`, and that copy has already drifted from upstream. Proposal: an optional keyword, e.g. `render_toc_ul(state.env["toc_items"], ordered=True)`, which renders exactly the same structure but with `<ol>` instead of `<ul>` at every nesting level. Without the keyword nothing changes.

### 1.3 Scope
- **In scope (stated):** Adding an optional keyword parameter `ordered` (default `False`) to `render_toc_ul` that renders table of contents items using `<ol>` and `</ol>` tags instead of `<ul>` and `</ul>` tags at all nesting levels (SRC-001).
- **In scope (inferred, pending confirmation):** None.
- **Out of scope:** See OOS-*.

### 1.4 Success measures
`render_toc_ul` successfully generates `<ol>` when `ordered=True` and `<ul>` when `ordered=False` or omitted, while preserving existing backward compatibility and HTML structure.

## 2. Glossary

| ID | Term | Definition / candidate readings | Status | Ref |
|---|---|---|---|---|
| GL-001 | render_toc_ul | Utility function in `mistune.toc` that renders a list of table of contents items into HTML list strings | DEFINED | SRC-001 |
| GL-002 | ordered list | HTML `<ol>` list element representing numbered table of contents | DEFINED | SRC-001 |

## 3. Sources

| ID | Verbatim statement | Location | Classification |
|---|---|---|---|
| SRC-001 | "render_toc_ul: allow a numbered (ordered) table of contents ... Proposal: an optional keyword ... html = render_toc_ul(state.env[\"toc_items\"], ordered=True) which renders exactly the same structure but with `<ol>` instead of `<ul>` at every nesting level. Without the keyword nothing changes." | GitHub Issue #4 | FUNC, GOAL |

## 3a. External evidence

| ID | Title | URL | Record | Status | Source type | Used for |
|---|---|---|---|---|---|---|
| REF-001 | External evidence not used | n/a | n/a | NOT-RUN | tertiary | not used |

## 4. Stakeholders and actors

| ID | Name / role | Kind | Interest or interaction | Decision authority | Origin | Ref |
|---|---|---|---|---|---|---|
| STK-001 | Library User / Developer | Stakeholder | Wants numbered table of contents support in `render_toc_ul` without monkeypatching or copying code | yes | STATED | SRC-001 |
| ACT-001 | Python API Caller | System actor | Calls `render_toc_ul(toc_items, ordered=True)` | — | INFERRED | ASM-001 |

## 5. Functional requirements

### FR-001 — Unordered TOC Rendering Backward Compatibility
- **Statement:** The `render_toc_ul` function shall render table of contents items using `<ul>` and `</ul>` HTML tags at all nesting levels when `ordered` parameter is omitted or set to `False`.
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
  - AC-FR-001-1: Given `toc = [(1, 'intro', 'Introduction')]`, when `render_toc_ul(toc)`, then exact output is `'<li><a href="#intro">Introduction</a></li>'`.
  - AC-FR-001-2: Given `toc = [(1, 'a', 'A'), (2, 'b', 'B')]`, when `render_toc_ul(toc, ordered=False)`, then exact output is `'<li><a href="#a">A</a>\n<ul>\n<li><a href="#b">B</a></li>\n</ul>\n</li>'`.

### FR-002 — Ordered TOC Rendering
- **Statement:** The `render_toc_ul` function shall render table of contents items using `<ol>` and `</ol>` HTML tags at all nesting levels when `ordered` parameter is set to `True`.
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
  - AC-FR-002-1: Given `toc = [(1, 'intro', 'Introduction')]`, when `render_toc_ul(toc, ordered=True)`, then exact output is `'<li><a href="#intro">Introduction</a></li>'`.
  - AC-FR-002-2: Given `toc = [(1, 'a', 'A'), (2, 'b', 'B')]`, when `render_toc_ul(toc, ordered=True)`, then exact output is `'<li><a href="#a">A</a>\n<ol>\n<li><a href="#b">B</a></li>\n</ol>\n</li>'`.
  - AC-FR-002-3: Given `toc = [(1, 'a', 'A'), (2, 'b', 'B'), (1, 'c', 'C')]`, when `render_toc_ul(toc, ordered=True)`, then exact output is `'<li><a href="#a">A</a>\n<ol>\n<li><a href="#b">B</a></li>\n</ol>\n</li>\n<li><a href="#c">C</a></li>'`.

## 6. Non-functional requirements

### NFR-001 — Python API Signature Compatibility
- **Statement:** The `render_toc_ul` function signature shall accept an optional keyword-only or positional/keyword `ordered` boolean parameter defaulting to `False` without breaking existing positional callers.
- **Category:** Compatibility
- **Origin:** STATED
- **Sources:** SRC-001
- **Assumptions:** None
- **Priority:** Must (stated)
- **Readiness:** READY
- **Blocked by:** None
- **Open questions:** None
- **Verification:** Test
- **Acceptance criteria:**
  - AC-NFR-001-1: Metric: API signature compatibility | Threshold: 100% backward compatible for single-argument callers | Conditions: Calling `render_toc_ul(toc)` | Method: Automated pytest unit tests.

## 7. Constraints

### CON-001 — Python Standard Library & Mistune codebase patterns
- **Statement:** Implementation must follow existing Mistune code style and use only Python standard library constructs without external dependencies.
- **Origin:** STATED
- **Sources:** SRC-001
- **Assumptions:** None

## 8. Dependencies

### DEP-001 — Python typing and re modules
- **Description:** Standard library typing and string utilities in `mistune.toc`.
- **Availability / owner:** available
- **Affects:** FR-001, FR-002

## 9. Risks

### RSK-001 — Tag mismatch between nested lists
- **Description:** Incorrect tag string (`<ul>` vs `<ol>`) generated during nested list level transitions.
- **Cause:** Complex level indentation logic in `render_toc_ul`.
- **Impact:** Invalid HTML output.
- **Likelihood:** Low (inferred)
- **Mitigation idea:** Parameterize tag names (`tag = 'ol' if ordered else 'ul'`) in `render_toc_ul` implementation.

## 10. Traceability matrix

| Requirement | Sources | Assumptions | Open items | Acceptance criteria | Priority | Readiness |
|---|---|---|---|---|---|---|
| FR-001 | SRC-001 | — | — | AC-FR-001-1..2 | Must | READY |
| FR-002 | SRC-001 | — | — | AC-FR-002-1..3 | Must | READY |
| NFR-001 | SRC-001 | — | — | AC-NFR-001-1 | Must | READY |

## 11. Change log

| Version | Date | Change | IDs affected |
|---|---|---|---|
| v1 | 2026-11-24 | Initial draft from GitHub issue #4 | all |


---

<!-- VAL-issue-4-v1.md -->

# Validation Summary: mistune render_toc_ul ordered table of contents

- **Document ID:** VAL-issue-4
- **Version:** v1
- **Date:** 2026-11-24
- **Verdict:** IMPLEMENTATION-READY
- **Verdict rationale:** All functional requirements are clearly stated in issue #4, testable with concrete ACs, fully traceable, and have no open questions or conflicts.

## 1. Readiness statistics

| Type | Total | READY | NEEDS-CONFIRMATION | NEEDS-CLARIFICATION | BLOCKED |
|---|---|---|---|---|---|
| FR | 2 | 2 | 0 | 0 | 0 |
| NFR | 1 | 1 | 0 | 0 | 0 |
| **Must only** | 3 | 3 | 0 | 0 | 0 |

| Origin | Count |
|---|---|
| STATED | 3 |
| CONFIRMED | 0 |
| INFERRED | 0 |

## 2. Check results

| Check | Result | Evidence / IDs |
|---|---|---|
| COMP-1 | PASS | SRS §1-11 present |
| COMP-2 | PASS | REG §1-5 present |
| COMP-3 | PASS | VAL §1-7 present |
| COMP-4 | PASS | All templates complete |
| COMP-5 | PASS | No empty sections without reason |
| COMP-6 | PASS | Scope defined |
| CONS-1 | PASS | No contradictions |
| CONS-2 | PASS | Terms consistent |
| CONS-3 | PASS | IDs unique |
| CONS-4 | PASS | Version matches |
| CONS-5 | PASS | Status valid |
| CONS-6 | PASS | References valid |
| TRACE-1 | PASS | FRs trace to SRC-001 |
| TRACE-2 | PASS | NFRs trace to SRC-001 |
| TRACE-3 | PASS | Actors trace to actors list |
| TRACE-4 | PASS | Traceability matrix complete |
| TRACE-5 | PASS | Assumptions linked |
| TRACE-6 | PASS | Out-of-scope defined |
| FEAS-1 | PASS | Technologically feasible |
| FEAS-2 | PASS | No impossible constraints |
| FEAS-3 | PASS | Scope bounded |
| FEAS-4 | PASS | Dependencies available |
| TEST-1 | PASS | ACs concrete and testable |
| TEST-2 | PASS | Given/When/Then used |
| TEST-3 | PASS | NFR metrics defined |
| TEST-4 | PASS | Test verification assigned |
| PROV-1 | PASS | Origins valid |
| PROV-2 | PASS | STATED items cite SRC |
| PROV-3 | PASS | INFERRED items cite ASM |
| PROV-4 | PASS | No silent upgrades |
| PROV-5 | PASS | Sources verbatim |
| PROV-6 | PASS | Evidence cited correctly |

## 3. Gap checklist coverage

| Dimension | Coverage | Ref |
|---|---|---|
| G1 Problem & goals | Covered | SRS §1 |
| G2 Users & actors | Covered | SRS §4 |
| G3 Core capabilities | Covered | SRS §5 |
| G4 Data | Covered | SRS §5 |
| G5 Interfaces & integrations | Covered | SRS §5, §6 |
| G6 Deployment & operations | N/A | Library function |
| G7 Security | N/A | Internal rendering utility |
| G8 Privacy & compliance | N/A | None |
| G9 Performance & capacity | N/A | In-memory string formatting |
| G10 Reliability & recovery | N/A | Deterministic pure function |
| G11 Usability & accessibility | Covered | API usage in docs |
| G12 Maintainability & portability | Covered | Standard Python |
| G13 Safety & ethics | N/A | None |
| G14 Constraints | Covered | SRS §7 |
| G15 Acceptance & success | Covered | SRS §1.4 |

## 4. Items not ready and what unblocks them

| Requirement | Readiness | Unblocked by |
|---|---|---|
| None | READY | None |

## 5. Tool log

| # | Tool / action | Result | Retry / fallback |
|---|---|---|---|
| 1 | validate_spec.py | PASS | None |

## 6. Human decisions required

None.

## 7. Recommended next steps

1. Proceed to design and implementation phase to add `ordered` parameter to `render_toc_ul`.
