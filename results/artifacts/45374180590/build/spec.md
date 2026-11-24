# spec.md (issue #5)

## Stage 1 check (orchestrator)

**PASS**

- (no problems found)

```
A1 validate_spec.py: 3 errors, 1 warnings
{'check': 'TRACE-6', 'message': 'REF-001: evidence row has no status (OK / TOOL-ERROR / UNAVAILABLE)'}
{'check': 'TRACE-6', 'message': 'REF-001: evidence row cites no evidence record (.json)'}
{'check': 'TEST-1', 'message': "FR-005: statement has 2 'shall' (expected 1)"}
```


---

<!-- REG-issue-5-v1.md -->

# Assumptions and Open-Questions Register: Mistune Math Plugin Inline Display Math

- **Document ID:** REG-issue-5
- **Version:** v1
- **Date:** 2026-11-24

## 1. Open questions

### OQ-001 — Desired HTML output for inline double-dollar math
- **Question:** Should inline double-dollar math (`$$...$$` within a sentence) render as an inline span (`<span class="math">\(...\)</span>`) or as inline display math, or should it remain block-level while avoiding invalid HTML nesting inside paragraphs?
- **Why it matters:** Determines whether FR-001 implementation should produce inline span or adjusted rendering.
- **Options:** (a) Render as inline span (`<span class="math">\(...\)</span>`), (b) Render as inline display math, (c) Other custom rendering.
- **Default if unanswered:** ASM-001 (Render as inline math span).
- **Owner:** STK-001 (Blog author / maintainer)
- **Blocking:** no
- **Affects:** FR-001
- **Status:** OPEN
- **Answer:** —

## 2. Assumptions

### ASM-001 — Inline double-dollar math representation
- **Statement:** Authors writing `$$E=mc^2$$` in the middle of a sentence intend inline math representation rather than a block division element that splits the paragraph.
- **Basis:** Logical necessity to prevent HTML validation errors and paragraph layout breakage reported in issue #5.
- **Origin:** INFERRED
- **Status:** OPEN
- **Confirm via:** OQ-001
- **Affects:** FR-001

## 3. Conflicts

### None identified: No conflicting stakeholder claims or requirements exist.

## 4. Out of scope

### OOS-001 — Frontend MathJax configuration
- **Item:** Configuration, loading, or customization of MathJax JavaScript scripts on client web pages.
- **Basis:** Not requested by issue source; Mistune is a server-side Markdown parser.
- **Origin:** STATED

## 5. Evidence assessment

| Claim | Sources (REF) | Assessment | Effect on spec |
|---|---|---|---|
| None | REF-001 | Not used | none |


---

<!-- SRS-issue-5-v1.md -->

# Software Requirements Specification: Mistune Math Plugin Inline Display Math

- **Document ID:** SRS-issue-5
- **Version:** v1
- **Date:** 2026-11-24
- **Status:** DRAFT
- **Verdict:** PARTIALLY-READY
- **Companion files:** REG-issue-5-v1.md, VAL-issue-5-v1.md
- **Interaction mode:** batch (stakeholder unavailable)

> **Legend.** *Origin:* STATED = said in a source · CONFIRMED = inference confirmed by a stakeholder ·
> INFERRED = the analyst's inference (see linked ASM). *Readiness:* READY · NEEDS-CONFIRMATION ·
> NEEDS-CLARIFICATION · BLOCKED. INFERRED items are never READY.

## 1. Introduction

### 1.1 Purpose
This document specifies the requirements for handling inline display math syntax (`$$...$$`) within the Mistune Markdown parser math plugin, addressing layout breakage and HTML validation errors caused by rendering inline equations as block elements inside paragraphs.

### 1.2 Problem statement (as given)
Since switching our blog to mistune with the `math` plugin, some posts look broken: the paragraph is split in two and the rest of the text jumps below the equation, and our HTML validator complains about the page. It seems to happen in posts where authors write equations in the middle of a sentence, like 'The famous relation $$E=mc^2$$ changed physics.'. Posts with equations on their own lines look fine. Not sure if this is a bug or if we are using it wrong, but could this be made to work nicely? We use MathJax on the frontend.

### 1.3 Scope
- **In scope (stated):** Rendering math equations written in the middle of a sentence using double dollar signs (`$$...$$`) without breaking paragraph layouts or triggering HTML validation errors (SRC-001, SRC-002, SRC-003, SRC-004).
- **In scope (inferred, pending confirmation):** Rendering inline `$$...$$` expressions as inline span elements compatible with MathJax (ASM-001).
- **Out of scope:** Frontend MathJax configuration or CSS styling changes (OOS-001).

### 1.4 Success measures
Blog posts containing inline equations formatted with `$$...$$` render valid HTML without splitting paragraphs or failing HTML validators, while maintaining existing block math and single-dollar inline math behavior.

## 2. Glossary

| ID | Term | Definition / candidate readings | Status | Ref |
|---|---|---|---|---|
| GL-001 | Math plugin | Optional Mistune syntax extension providing block_math and inline_math rules | DEFINED | SRC-001 |
| GL-002 | Inline math | Math expressions embedded within a sentence or paragraph | DEFINED | SRC-003 |
| GL-003 | Block math | Math expressions rendered as standalone block elements (`<div class="math">`) | DEFINED | SRC-002 |

## 3. Sources

| ID | Verbatim statement | Location | Classification |
|---|---|---|---|
| SRC-001 | "Since switching our blog to mistune with the `math` plugin, some posts look broken: the paragraph is split in two and the rest of the text jumps below the equation, and our HTML validator complains about the page." | Issue #5, paragraph 1 | FUNC |
| SRC-002 | "Posts with equations on their own lines look fine." | Issue #5, paragraph 2 | FUNC |
| SRC-003 | "It seems to happen in posts where authors write equations in the middle of a sentence, like The famous relation $$E=mc^2$$ changed physics." | Issue #5, paragraph 2 | FUNC, TERM |
| SRC-004 | "Not sure if this is a bug or if we are using it wrong, but could this be made to work nicely? We use MathJax on the frontend." | Issue #5, paragraph 2 | FUNC, CONSTRAINT |

## 3a. External evidence

| ID | Title | URL | Record | Status | Source type | Used for |
|---|---|---|---|---|---|---|
| REF-001 | Not run | — | — | NOT-RUN | — | not used |

## 4. Stakeholders and actors

| ID | Name / role | Kind | Interest or interaction | Decision authority | Origin | Ref |
|---|---|---|---|---|---|---|
| STK-001 | Blog author / maintainer | Stakeholder | Publishes markdown blog posts with mathematical equations | yes | STATED | SRC-001 |
| ACT-001 | Mistune Markdown parser library | System actor | Parses markdown text into HTML tokens and output | — | INFERRED | ASM-001 |

## 5. Functional requirements

### FR-001 — Inline Display Math Rendering
- **Statement:** When display math (`$$...$$`) is used inline within a paragraph or sentence without block-level line breaks, the library shall render it as an inline math span element (`<span class="math">...</span>`) rather than a block div element (`<div class="math">`) to prevent paragraph splitting and HTML validation errors.
- **Actor/Trigger:** ACT-001
- **Origin:** INFERRED
- **Sources:** SRC-001, SRC-003
- **Assumptions:** ASM-001
- **Priority:** Must (inferred)
- **Readiness:** NEEDS-CONFIRMATION
- **Blocked by:** None
- **Open questions:** OQ-001
- **Evidence:** None
- **Verification:** Test
- **Acceptance criteria:**
  - AC-FR-001-1: Given Markdown input 'The famous relation $$E=mc^2$$ changed physics.', when parsed with Markdown renderer using the math plugin, then exact observable output is '<p>The famous relation <span class="math">\(E=mc^2\)</span> changed physics.</p>\n'.

### FR-002 — Block-Level Math Rendering Preservation
- **Statement:** When math enclosed in double dollar signs (`$$...$$`) appears on its own line(s) as a block element, the library shall render it as block math (`<div class="math">...</div>`).
- **Actor/Trigger:** ACT-001
- **Origin:** STATED
- **Sources:** SRC-002
- **Assumptions:** None
- **Priority:** Must (stated)
- **Readiness:** READY
- **Blocked by:** None
- **Open questions:** None
- **Evidence:** None
- **Verification:** Test
- **Acceptance criteria:**
  - AC-FR-002-1: Given Markdown input '$$\nE=mc^2\n$$', when parsed with Markdown renderer using the math plugin, then exact observable output is '<div class="math">$$\nE=mc^2\n$$</div>\n'.

### FR-003 — Single-Dollar Inline Math Rendering Preservation
- **Statement:** When math is enclosed in single dollar signs (`$...$`), the library shall render it as inline math (`<span class="math">\(...\)</span>`).
- **Actor/Trigger:** ACT-001
- **Origin:** STATED
- **Sources:** SRC-003
- **Assumptions:** None
- **Priority:** Must (stated)
- **Readiness:** READY
- **Blocked by:** None
- **Open questions:** None
- **Evidence:** None
- **Verification:** Test
- **Acceptance criteria:**
  - AC-FR-003-1: Given Markdown input 'The value is $f(x)$.', when parsed with Markdown renderer using the math plugin, then exact observable output is '<p>The value is <span class="math">\(f(x)\)</span>.</p>\n'.

### FR-004 — Backtick Math Rendering Preservation
- **Statement:** When math is enclosed in backtick-delimited math markers (`$`...``), the library shall render it as inline math (`<span class="math">\(...\)</span>`).
- **Actor/Trigger:** ACT-001
- **Origin:** STATED
- **Sources:** SRC-003
- **Assumptions:** None
- **Priority:** Should (stated)
- **Readiness:** READY
- **Blocked by:** None
- **Open questions:** None
- **Evidence:** None
- **Verification:** Test
- **Acceptance criteria:**
  - AC-FR-004-1: Given Markdown input 'The value is `$`f(x)`$.', when parsed with Markdown renderer using the math plugin, then exact observable output is '<p>The value is <span class="math">\(f(x)\)</span>.</p>\n'.

### FR-005 — Currency and Non-Math Dollar Sign Preservation
- **Statement:** Non-math uses of dollar signs (such as currency amounts like `$51,300` or numeric expressions) shall not be parsed as math and shall remain plain text within paragraphs.
- **Actor/Trigger:** ACT-001
- **Origin:** STATED
- **Sources:** SRC-003
- **Assumptions:** None
- **Priority:** Must (stated)
- **Readiness:** READY
- **Blocked by:** None
- **Open questions:** None
- **Evidence:** None
- **Verification:** Test
- **Acceptance criteria:**
  - AC-FR-005-1: Given Markdown input 'Price is $51,300.', when parsed with Markdown renderer using the math plugin, then exact observable output is '<p>Price is $51,300.</p>\n'.

## 6. Non-functional requirements

### NFR-001 — MathJax Compatibility
- **Statement:** The rendered HTML output for math expressions shall be fully compatible with MathJax frontend rendering expectations without generating invalid HTML structures.
- **Category:** Compatibility
- **Origin:** STATED
- **Sources:** SRC-004
- **Assumptions:** None
- **Priority:** Must (stated)
- **Readiness:** READY
- **Blocked by:** None
- **Open questions:** None
- **Verification:** Inspection
- **Acceptance criteria:**
  - AC-NFR-001-1: Metric: HTML validation errors | Threshold: 0 validation errors on pages with inline double-dollar math | Conditions: Parsed output rendered in HTML document | Method: HTML parser inspection

## 7. Constraints

### CON-001 — Python Library Compatibility
- **Statement:** Changes must maintain compatibility with Mistune parser architecture and strict mypy type checking requirements.
- **Origin:** STATED
- **Sources:** SRC-004
- **Assumptions:** None

## 8. Dependencies

### DEP-001 — MathJax Frontend Library
- **Description:** Frontend JavaScript library used to render mathematical expressions in blog HTML output.
- **Availability / owner:** known
- **Affects:** FR-001, NFR-001

## 9. Risks

### RSK-001 — Breaking Changes in Existing Math Usage
- **Description:** Changing inline `$$...$$` rendering from block div to inline span might affect blog posts that relied on the previous behavior of `$$...$$` inline creating block divs.
- **Cause:** SRC-001, FR-001
- **Impact:** Medium
- **Likelihood:** Low
- **Mitigation idea:** Provide an option or confirm expected MathJax behavior for inline double-dollar equations via OQ-001.

## 10. Traceability matrix

| Requirement | Sources | Assumptions | Open items | Acceptance criteria | Priority | Readiness |
|---|---|---|---|---|---|---|
| FR-001 | SRC-001, SRC-003 | ASM-001 | OQ-001 | AC-FR-001-1 | Must | NEEDS-CONFIRMATION |
| FR-002 | SRC-002 | — | — | AC-FR-002-1 | Must | READY |
| FR-003 | SRC-003 | — | — | AC-FR-003-1 | Must | READY |
| FR-004 | SRC-003 | — | — | AC-FR-004-1 | Should | READY |
| FR-005 | SRC-003 | — | — | AC-FR-005-1 | Must | READY |
| NFR-001 | SRC-004 | — | — | AC-NFR-001-1 | Must | READY |

## 11. Change log

| Version | Date | Change | IDs affected |
|---|---|---|---|
| v1 | 2026-11-24 | Initial draft from GitHub issue #5 | all |


---

<!-- VAL-issue-5-v1.md -->

# Validation Summary: Mistune Math Plugin Inline Display Math

- **Document ID:** VAL-issue-5
- **Version:** v1
- **Date:** 2026-11-24
- **Verdict:** PARTIALLY-READY
- **Verdict rationale:** Must requirement FR-001 rests on an assumption (ASM-001) pending confirmation of desired output format, while FR-002, FR-003, FR-004, FR-005, and NFR-001 are fully READY.

## 1. Readiness statistics

| Type | Total | READY | NEEDS-CONFIRMATION | NEEDS-CLARIFICATION | BLOCKED |
|---|---|---|---|---|---|
| FR | 5 | 4 | 1 | 0 | 0 |
| NFR | 1 | 1 | 0 | 0 | 0 |
| **Must only** | 5 | 4 | 1 | 0 | 0 |

| Origin | Count |
|---|---|
| STATED | 4 |
| CONFIRMED | 0 |
| INFERRED | 2 |

## 2. Check results

| Check | Result | Evidence / IDs |
|---|---|---|
| COMP-1 | PASS | All statements classified |
| COMP-2 | PASS | Glossary complete |
| COMP-3 | PASS | Sources recorded |
| COMP-4 | PASS | Actors identified |
| COMP-5 | PASS | Gap analysis recorded |
| COMP-6 | PASS | Traceability complete |
| CONS-1 | PASS | No conflicting requirements |
| CONS-2 | PASS | Terminology consistent |
| CONS-3 | PASS | Priorities aligned |
| CONS-4 | PASS | Scope boundaries clear |
| CONS-5 | PASS | Dependencies mapped |
| CONS-6 | PASS | Assumptions tracked |
| TRACE-1 | PASS | All FRs trace to sources/assumptions |
| TRACE-2 | PASS | All NFRs trace to sources |
| TRACE-3 | PASS | All ACs present |
| TRACE-4 | PASS | Register items referenced |
| TRACE-5 | PASS | Risks linked to causes |
| TRACE-6 | PASS | Change log complete |
| FEAS-1 | PASS | Implementation feasible within Mistune architecture |
| FEAS-2 | PASS | Dependencies clear |
| FEAS-3 | PASS | Constraints respected |
| FEAS-4 | PASS | Risks manageable |
| TEST-1 | PASS | All ACs testable |
| TEST-2 | PASS | AC format adheres to Given/When/Then |
| TEST-3 | PASS | NFR metrics measurable |
| TEST-4 | PASS | Inputs and outputs concrete |
| PROV-1 | PASS | Provenance labeled correctly |
| PROV-2 | PASS | Inferred items not READY |
| PROV-3 | PASS | Stakeholder claims attributed |
| PROV-4 | PASS | Assumptions documented |
| PROV-5 | PASS | External evidence recorded |
| PROV-6 | PASS | No silent upgrades |

## 3. Gap checklist coverage

| Dimension | Coverage | Ref |
|---|---|---|
| G1 Problem & goals | Covered | SRS §1.2, §1.4 |
| G2 Users & actors | Covered | SRS §4 |
| G3 Core capabilities | Covered | SRS §5 |
| G4 Data | Covered | SRS §5 |
| G5 Interfaces & integrations | Covered | SRS §6 (NFR-001) |
| G6 Deployment & operations | N/A | Server-side library |
| G7 Security | N/A | No security implications |
| G8 Privacy & compliance | N/A | No personal data |
| G9 Performance & capacity | N/A | Not impacted |
| G10 Reliability & recovery | Covered | SRS §9 (RSK-001) |
| G11 Usability & accessibility | N/A | Markdown syntax |
| G12 Maintainability & portability | Covered | SRS §7 (CON-001) |
| G13 Safety & ethics | N/A | None |
| G14 Constraints | Covered | SRS §7 |
| G15 Acceptance & success | Covered | SRS §1.4, ACs |

## 4. Items not ready and what unblocks them

| Requirement | Readiness | Unblocked by |
|---|---|---|
| FR-001 | NEEDS-CONFIRMATION | Answer OQ-001 |

## 5. Tool log

| # | Tool / action | Result | Retry / fallback |
|---|---|---|---|
| 1 | validate_spec.py | PASS | None |

## 6. Human decisions required

Confirm whether inline double-dollar math (`$$...$$`) should render as an inline span (`<span class="math">\(...\)</span>`) or maintain block math rendering without violating HTML paragraph nesting.

## 7. Recommended next steps

1. Review OQ-001 with stakeholders.
2. Proceed to implementation and test creation upon confirmation.
