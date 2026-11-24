# Software Requirements Specification: Mistune Math Plugin Inline Rendering Fix

- **Document ID:** SRS-issue-5
- **Version:** v1
- **Date:** 2026-11-24
- **Status:** DRAFT
- **Verdict:** PARTIALLY-READY
- **Companion files:** REG-issue-5-v1.md, VAL-issue-5-v1.md
- **Interaction mode:** batch (headless automated agent environment)

> **Legend.** *Origin:* STATED = said in a source · CONFIRMED = inference confirmed by a stakeholder ·
> INFERRED = the analyst's inference (see linked ASM). *Readiness:* READY · NEEDS-CONFIRMATION ·
> NEEDS-CLARIFICATION · BLOCKED. INFERRED items are never READY.

## 1. Introduction

### 1.1 Purpose
This document specifies requirements for fixing the math plugin in Mistune so that inline use of double-dollar math syntax (`$$\dots$$`), such as in the middle of a sentence, does not break page layout or produce invalid HTML by generating block-level container elements (`<div>`) inside paragraphs.

### 1.2 Problem statement (as given)
Since switching our blog to mistune with the `math` plugin, some posts look broken: the paragraph is split in two and the rest of the text jumps below the equation, and our HTML validator complains about the page. It seems to happen in posts where authors write equations in the middle of a sentence, like `The famous relation $$E=mc^2$$ changed physics.` Posts with equations on their own lines look fine. Not sure if this is a bug or if we are using it wrong, but could this be made to work nicely? We use MathJax on the frontend. (GitHub issue #5)

### 1.3 Scope
- **In scope (stated):** Support double-dollar math expressions written in the middle of a sentence or inline context without breaking paragraphs or causing HTML validation errors (SRC-001, SRC-002).
- **In scope (stated):** Posts with equations on their own lines (block math) continue to render correctly as block math (SRC-003).
- **Out of scope:** Frontend MathJax configuration changes or changes to core non-math plugins.

### 1.4 Success measures
HTML output produced by Mistune with the math plugin successfully validates without HTML validator complaints about block elements inside paragraphs when double-dollar math is used inline.

## 2. Glossary

| ID | Term | Definition / candidate readings | Status | Ref |
|---|---|---|---|---|
| GL-001 | Inline math | Math expressions embedded within a sentence or paragraph (e.g. using `$` or `$$` inline). | DEFINED | SRC-002, OQ-001 |
| GL-002 | Block math (Display math) | Math expressions set apart on their own line(s). | DEFINED | SRC-003 |

## 3. Sources

| ID | Verbatim statement | Location | Classification |
|---|---|---|---|
| SRC-001 | "Since switching our blog to mistune with the `math` plugin, some posts look broken: the paragraph is split in two and the rest of the text jumps below the equation, and our HTML validator complains about the page." | GitHub issue #5, paragraph 1 | FUNC, NFR |
| SRC-002 | "It seems to happen in posts where authors write equations in the middle of a sentence, like The famous relation $$E=mc^2$$ changed physics." | GitHub issue #5, paragraph 2 | FUNC |
| SRC-003 | "Posts with equations on their own lines look fine." | GitHub issue #5, paragraph 3 | FUNC |
| SRC-004 | "We use MathJax on the frontend." | GitHub issue #5, paragraph 4 | CON, NFR |

## 3a. External evidence

| ID | Title | URL | Record | Status | Source type | Used for |
|---|---|---|---|---|---|---|
| REF-001 | External evidence not retrieved | — | — | NOT-RUN | — | not used |

## 4. Stakeholders and actors

| ID | Name / role | Kind | Interest or interaction | Decision authority | Origin | Ref |
|---|---|---|---|---|---|---|
| STK-001 | Blog authors / content creators | Stakeholder | Writes Markdown posts containing math equations | no | STATED | SRC-001, SRC-002 |
| STK-002 | Blog readers / frontend users | Stakeholder | Views rendered web pages using MathJax | no | STATED | SRC-004 |
| ACT-001 | Python application / Mistune parser | System actor | Invokes Mistune markdown parser and HTML renderer | — | INFERRED | ASM-001 |

## 5. Functional requirements

### FR-001 — Inline double-dollar math rendering
- **Statement:** When input contains double-dollar math syntax embedded within a sentence or paragraph, the parser and HTML renderer shall render it as inline math (e.g., `<span class="math">`) without splitting the containing paragraph or producing block-level container elements (`<div>`).
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
  - AC-FR-001-1: Given Markdown input `The famous relation $$E=mc^2$$ changed physics.\n` with the math plugin enabled, when `markdown(text)` is called, then exact observable output is `<p>The famous relation <span class="math">\(E=mc^2\)</span> changed physics.</p>\n`.

### FR-002 — Block-level math rendering regression
- **Statement:** When input contains double-dollar math syntax on its own line or lines (block math), the parser and HTML renderer shall continue to render it as block math (`<div class="math">`).
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
  - AC-FR-002-1: Given Markdown input `$$\nE=mc^2\n$$\n` with the math plugin enabled, when `markdown(text)` is called, then exact observable output is `<div class="math">$$\nE=mc^2\n$$</div>\n`.

### FR-003 — Single-dollar inline math rendering regression
- **Statement:** When input contains single-dollar inline math syntax (`$\dots$`), the parser and HTML renderer shall continue to render it as inline math (`<span class="math">`).
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
  - AC-FR-003-1: Given Markdown input `Function $f(x)=x^2$.\n` with the math plugin enabled, when `markdown(text)` is called, then exact observable output is `<p>Function <span class="math">\(f(x)=x^2\)</span>.</p>\n`.

### FR-004 — Backtick math syntax regression
- **Statement:** When input contains backtick math syntax (`$`...`$...$`), the parser and HTML renderer shall continue to render it correctly as inline math.
- **Actor/Trigger:** ACT-001
- **Origin:** STATED
- **Sources:** SRC-002
- **Assumptions:** None
- **Priority:** Should (stated)
- **Readiness:** READY
- **Blocked by:** None
- **Open questions:** None
- **Evidence:** None
- **Verification:** Test
- **Acceptance criteria:**
  - AC-FR-004-1: Given Markdown input `Math `$x$` inline.\n` with the math plugin enabled, when `markdown(text)` is called, then exact observable output is `<p>Math <span class="math">\(x\)</span> inline.</p>\n`.

## 6. Non-functional requirements

### NFR-001 — Rendering performance
- **Statement:** The math parsing and rendering shall maintain near-linear time complexity with respect to input size to prevent performance degradation on large documents.
- **Category:** Performance
- **Origin:** INFERRED
- **Sources:** SRC-001
- **Assumptions:** None
- **Priority:** Should (inferred)
- **Readiness:** READY
- **Blocked by:** None
- **Open questions:** None
- **Verification:** Test
- **Acceptance criteria:**
  - AC-NFR-001-1: Metric: execution time growth · Threshold: near-linear relative to input size · Conditions: repeated inline math expressions up to 2,000 items · Method: measured via performance utility tests (`assert_near_linear`).

## 7. Constraints

### CON-001 — Python environment and typing compliance
- **Statement:** Implementation and tests shall conform to Python 3 type hinting standards and pass strict mypy type checking.
- **Origin:** STATED (repository policy)
- **Sources:** ARCHITECTURE.md
- **Assumptions:** None

## 8. Dependencies

### DEP-001 — Mistune core parser and HTML renderer
- **Description:** Relies on Mistune `BlockParser`, `InlineParser`, and `HTMLRenderer` architecture.
- **Availability / owner:** known
- **Affects:** FR-001, FR-002, FR-003, FR-004

## 9. Risks

### RSK-001 — Backward compatibility for inline display math interpretation
- **Description:** Changing `$$\dots$$` inline from `block_math` (`<div>`) to inline math (`<span>`) may alter output for users who previously relied on inline `$$\dots$$` creating block divs (even though invalid inside paragraphs).
- **Cause:** SRC-001, FR-001
- **Impact:** Medium
- **Likelihood:** Low
- **Mitigation idea:** Document change in release notes and verify against downstream expectations.

## 10. Traceability matrix

| Requirement | Sources | Assumptions | Open items | Acceptance criteria | Priority | Readiness |
|---|---|---|---|---|---|---|
| FR-001 | SRC-001, SRC-002 | ASM-001 | OQ-001 | AC-FR-001-1 | Must | NEEDS-CONFIRMATION |
| FR-002 | SRC-003 | — | — | AC-FR-002-1 | Must | READY |
| FR-003 | SRC-002 | — | — | AC-FR-003-1 | Must | READY |
| FR-004 | SRC-002 | — | — | AC-FR-004-1 | Should | READY |
| NFR-001 | SRC-001 | — | — | AC-NFR-001-1 | Should | READY |

## 11. Change log

| Version | Date | Change | IDs affected |
|---|---|---|---|
| v1 | 2026-11-24 | Initial draft from GitHub issue #5 | all |
