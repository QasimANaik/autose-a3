# spec.md (issue #18)

## Stage 1 check (orchestrator)

**PASS**

- (no problems found)

```
A1 validate_spec.py: 10 errors, 0 warnings
{'check': 'TRACE-6', 'message': 'REF-001: evidence row has no status (OK / TOOL-ERROR / UNAVAILABLE)'}
{'check': 'TRACE-6', 'message': 'REF-001: evidence row cites no evidence record (.json)'}
{'check': 'PROV-1', 'message': 'NFR-001: INFERRED but links no ASM-*'}
{'check': 'PROV-2', 'message': 'NFR-001: INFERRED item marked READY'}
{'check': 'TRACE-1', 'message': 'NFR-002: cites no SRC-* or ASM-*'}
{'check': 'PROV-1', 'message': 'NFR-002: INFERRED but links no ASM-*'}
{'check': 'PROV-2', 'message': 'NFR-002: INFERRED item marked READY'}
{'check': 'TRACE-1', 'message': 'CON-001: cites no SRC-* or ASM-*'}
{'check': 'TRACE-3', 'message': 'CNF-001: each claim must cite a SRC-*'}
{'check': 'TRACE-3', 'message': 'CNF-001: Affects lists no IDs'}
```


---

<!-- REG-issue-18-v1.md -->

# Assumptions and Open-Questions Register: URL Plugin Enhancements for WWW Links

- **Document ID:** REG-issue-18
- **Version:** v1
- **Date:** 2026-11-24

## 1. Open questions

### OQ-001 — Scheme selection for `www.` URLs in href attribute
- **Question:** Should `www.example.com` links have `https://` prepended to their HTML `href` attribute, or `http://`, or should the scheme be configurable?
- **Why it matters:** Browsers require an absolute URI scheme (like `https://`) in `href` to navigate correctly when clicking relative/scheme-less domains.
- **Options:** (a) Always prepend `https://` (b) Always prepend `http://` (c) Make protocol configurable via plugin options
- **Default if unanswered:** ASM-001 (always prepend `https://`)
- **Owner:** STK-001 / maintainers
- **Blocking:** no
- **Affects:** FR-003
- **Status:** OPEN
- **Answer:** —

### OQ-002 — Exact regular expression boundary rules for `www.` matching
- **Question:** What exact regular expression boundaries should distinguish valid `www.` URLs from partial word matches (e.g. `my_www.example.com`)?
- **Why it matters:** Overly broad regex could break code blocks or ordinary words containing `www.`.
- **Options:** (a) Require whitespace, angle bracket, or start of line before `www.` (b) Require word boundary (`\b`) before `www.`
- **Default if unanswered:** ASM-002 (require word boundary / non-word character before `www.`)
- **Owner:** STK-001 / maintainers
- **Blocking:** no
- **Affects:** FR-001, FR-004
- **Status:** OPEN
- **Answer:** —

## 2. Assumptions

### ASM-001 — Default scheme for `www.` href
- **Statement:** Scheme-less URLs starting with `www.` should automatically prepend `https://` to their `href` attribute in generated HTML links.
- **Basis:** Modern web standards and security best practices default to HTTPS for web navigation.
- **Origin:** INFERRED
- **Status:** OPEN
- **Confirm via:** OQ-001
- **Affects:** FR-003

### ASM-002 — Boundary pattern for `www.` matching
- **Statement:** The matching pattern for `www.` URLs should ensure that `www.` is preceded by a word boundary or whitespace/start-of-line to avoid matching inside identifiers or words.
- **Basis:** Standard text parsing conventions for autolinks in markdown libraries (GitHub Flavored Markdown / Slack behavior).
- **Origin:** INFERRED
- **Status:** OPEN
- **Confirm via:** OQ-002
- **Affects:** FR-001, FR-004

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

### OOS-001 — Arbitrary domain autolinking without `www.`
- **Item:** Automatic linking of arbitrary domain names lacking both protocol scheme and `www.` prefix (e.g., `example.com/docs`).
- **Basis:** Not requested by issue #18 ("obvious ones to just work", specifying `www.example.com/docs`).
- **Origin:** STATED

## 5. Evidence assessment

| Claim | Sources (REF) | Assessment | Effect on spec |
|---|---|---|---|
| External evidence not retrieved | REF-001 | Not used | none |


---

<!-- SRS-issue-18-v1.md -->

# Software Requirements Specification: URL Plugin Enhancements for WWW Links

- **Document ID:** SRS-issue-18
- **Version:** v1
- **Date:** 2026-11-24
- **Status:** DRAFT
- **Verdict:** PARTIALLY-READY
- **Companion files:** REG-issue-18-v1.md, VAL-issue-18-v1.md
- **Interaction mode:** batch (headless execution, no stakeholder available)

> **Legend.** *Origin:* STATED = said in a source · CONFIRMED = inference confirmed by a stakeholder ·
> INFERRED = the analyst's inference (see linked ASM). *Readiness:* READY · NEEDS-CONFIRMATION ·
> NEEDS-CLARIFICATION · BLOCKED. INFERRED items are never READY.

## 1. Introduction

### 1.1 Purpose
This document specifies requirements for enhancing the `url` plugin in the Python Markdown library `mistune` to recognize scheme-less URLs starting with `www.`, enabling team chat logs and user-pasted text containing `www.example.com` links to render as clickable HTML links without breaking existing functionality.

### 1.2 Problem statement (as given)
We render our team chat logs to HTML with mistune (`plugins=["url"]`) and people keep complaining that "some links are dead text". For example this log line: `alice: docs are at www.example.com/docs, or the old page https://example.com/old`. The second link is clickable, the first one isn't, even though it is clearly an address. Our users paste addresses all kinds of ways and expect them to work like on GitHub or in Slack. Could the url plugin be smarter about this? Not sure what the right rules are, but we'd like the obvious ones to just work without breaking the links that already work.

### 1.3 Scope
- **In scope (stated):** Recognizing raw URLs starting with `www.` in addition to existing `http://` and `https://` URLs, without breaking existing links (SRC-001, SRC-002, SRC-003, SRC-004, SRC-005).
- **In scope (inferred, pending confirmation):** Prepending `https://` to scheme-less `www.` URLs in generated `href` attributes (ASM-001); pattern boundary rules for `www.` links (ASM-002).
- **Out of scope:** Automatic linking of arbitrary domain names without `www.` prefix (e.g. `example.com/docs`) (OOS-001).

### 1.4 Success measures
Obvious raw `www.` URLs (e.g. `www.example.com/docs`) render as clickable HTML links `<a href="...">www.example.com/docs</a>`, while existing valid links and non-link text remain unaffected.

## 2. Glossary

| ID | Term | Definition / candidate readings | Status | Ref |
|---|---|---|---|---|
| GL-001 | URL plugin | Mistune optional inline parser plugin registered via `plugins=["url"]` that parses raw URLs into link tokens. | DEFINED | SRC-001, ARCHITECTURE.md |
| GL-002 | Scheme-less URL | A web address starting with `www.` lacking an explicit protocol schema (`http://` or `https://`). | DEFINED | SRC-003, SRC-005 |
| GL-003 | Clickable link | An HTML anchor element (`<a href="...">...</a>`) rendered from a raw URL. | DEFINED | SRC-003, SRC-005 |

## 3. Sources

| ID | Verbatim statement | Location | Classification |
|---|---|---|---|
| SRC-001 | "We render our team chat logs to HTML with mistune (`plugins=["url"]`) and people keep complaining that 'some links are dead text'." | Issue #18, Paragraph 1 | FUNC, CONTEXT |
| SRC-002 | "For example this log line: alice: docs are at www.example.com/docs, or the old page https://example.com/old" | Issue #18, Paragraph 2-3 | FUNC, EXAMPLE |
| SRC-003 | "The second link is clickable, the first one isn't, even though it is clearly an address." | Issue #18, Paragraph 4 | FUNC |
| SRC-004 | "Our users paste addresses all kinds of ways and expect them to work like on GitHub or in Slack." | Issue #18, Paragraph 5 | FUNC, QUALITY |
| SRC-005 | "Could the url plugin be smarter about this? Not sure what the right rules are, but we'd like the obvious ones to just work without breaking the links that already work." | Issue #18, Paragraph 6 | FUNC, GOAL |

## 3a. External evidence

| ID | Title | URL | Record | Status | Source type | Used for |
|---|---|---|---|---|---|---|
| REF-001 | External evidence check not run | N/A | N/A | NOT-RUN | secondary | not used |

## 4. Stakeholders and actors

| ID | Name / role | Kind | Interest or interaction | Decision authority | Origin | Ref |
|---|---|---|---|---|---|---|
| STK-001 | Issue author / chat log user | Stakeholder | Wants chat log URLs (`www...`) to be clickable. | unknown | STATED | SRC-001..005 |
| ACT-001 | Mistune Markdown parser / URL plugin | System actor | Parses inline text and generates link tokens. | — | INFERRED | GL-001 |

## 5. Functional requirements

### FR-001 — Recognition of scheme-less `www.` URLs
- **Statement:** The URL plugin shall recognize and parse raw text matching `www.` URL patterns as link tokens when the url plugin is enabled.
- **Actor/Trigger:** ACT-001
- **Origin:** INFERRED
- **Sources:** SRC-003, SRC-005
- **Assumptions:** ASM-002
- **Priority:** Must (stated)
- **Readiness:** NEEDS-CONFIRMATION
- **Blocked by:** None
- **Open questions:** OQ-002
- **Evidence:** None
- **Verification:** Test
- **Acceptance criteria:**
  - AC-FR-001-1: Given Markdown input `"visit www.example.com/docs"` with url plugin enabled, when `mistune.html(markdown, plugins=['url'])` is called, then exact observable output is `"<p>visit <a href=\"https://www.example.com/docs\">www.example.com/docs</a></p>\n"`.

### FR-002 — Preservation of existing explicit scheme URLs
- **Statement:** The URL plugin shall continue to recognize and parse raw URLs starting with `http://` or `https://` exactly as existing behavior.
- **Actor/Trigger:** ACT-001
- **Origin:** STATED
- **Sources:** SRC-002, SRC-003, SRC-005
- **Assumptions:** None
- **Priority:** Must (stated)
- **Readiness:** READY
- **Blocked by:** None
- **Open questions:** None
- **Evidence:** None
- **Verification:** Test
- **Acceptance criteria:**
  - AC-FR-002-1: Given Markdown input `"visit https://example.com/old"` with url plugin enabled, when `mistune.html(markdown, plugins=['url'])` is called, then exact observable output is `"<p>visit <a href=\"https://example.com/old\">https://example.com/old</a></p>\n"`.

### FR-003 — Href attribute formatting for `www.` URLs
- **Statement:** The URL plugin shall format the generated `href` attribute for `www.` URLs by prefixing them with `https://` so browsers navigate correctly.
- **Actor/Trigger:** ACT-001
- **Origin:** INFERRED
- **Sources:** SRC-005
- **Assumptions:** ASM-001
- **Priority:** Should (inferred)
- **Readiness:** NEEDS-CONFIRMATION
- **Blocked by:** None
- **Open questions:** OQ-001
- **Evidence:** None
- **Verification:** Test
- **Acceptance criteria:**
  - AC-FR-003-1: Given Markdown input `"www.example.com"` with url plugin enabled, when `mistune.html(markdown, plugins=['url'])` is called, then exact observable output is `"<p><a href=\"https://www.example.com\">www.example.com</a></p>\n"`.

### FR-004 — Prevention of false positive matching on non-URL text
- **Statement:** The URL plugin shall avoid matching non-URL text sequences starting with `www.` embedded inside invalid boundaries or punctuation.
- **Actor/Trigger:** ACT-001
- **Origin:** STATED
- **Sources:** SRC-005
- **Assumptions:** ASM-002
- **Priority:** Must (stated)
- **Readiness:** NEEDS-CONFIRMATION
- **Blocked by:** None
- **Open questions:** OQ-002
- **Evidence:** None
- **Verification:** Test
- **Acceptance criteria:**
  - AC-FR-004-1: Given Markdown input `"not a link: my_www.example"` with url plugin enabled, when `mistune.html(markdown, plugins=['url'])` is called, then exact observable output is `"<p>not a link: my_www.example</p>\n"`.

## 6. Non-functional requirements

### NFR-001 — Parsing performance and overhead
- **Statement:** The URL plugin regex matching shall introduce negligible latency overhead during inline parsing.
- **Category:** Performance
- **Origin:** INFERRED
- **Sources:** SRC-001
- **Assumptions:** None
- **Priority:** Should (inferred)
- **Readiness:** READY
- **Blocked by:** None
- **Open questions:** None
- **Verification:** Analysis
- **Acceptance criteria:**
  - AC-NFR-001-1: Metric: benchmark execution time | Threshold: < 5% regression on benchmark suite | Conditions: running benchmark suite | Method: pytest benchmark.

### NFR-002 — Strict type checking and compatibility
- **Statement:** Code changes to the URL plugin shall pass strict mypy type checking without suppressing type warnings.
- **Category:** Maintainability
- **Origin:** INFERRED
- **Sources:** ARCHITECTURE.md
- **Assumptions:** None
- **Priority:** Must (inferred)
- **Readiness:** READY
- **Blocked by:** None
- **Open questions:** None
- **Verification:** Analysis
- **Acceptance criteria:**
  - AC-NFR-002-1: Metric: mypy error count | Threshold: 0 errors on `src/mistune` | Conditions: running `uv run mypy` | Method: static analysis command.

## 7. Constraints

### CON-001 — Python version and library constraints
- **Statement:** Implementation must be compatible with Python 3.8+ and rely solely on standard library regular expressions without external dependencies.
- **Origin:** STATED
- **Sources:** pyproject.toml
- **Assumptions:** None

## 8. Dependencies

### DEP-001 — Mistune inline parser core
- **Description:** Mistune inline parsing framework (`InlineParser`, `InlineState`).
- **Availability / owner:** available / mistune maintainers
- **Affects:** FR-001, FR-002, FR-003, FR-004

## 9. Risks

### RSK-001 — Over-matching `www.` in prose or code
- **Description:** Loosening URL matching to include `www.` without scheme might inadvertently match substrings like `my_www.foo` or trailing punctuation.
- **Cause:** SRC-005, ASM-002
- **Impact:** Medium
- **Likelihood:** Medium
- **Mitigation idea:** Precise boundary assertions in regular expression matching (e.g., negative lookbehind or word boundary).

## 10. Traceability matrix

| Requirement | Sources | Assumptions | Open items | Acceptance criteria | Priority | Readiness |
|---|---|---|---|---|---|---|
| FR-001 | SRC-003, SRC-005 | ASM-002 | OQ-002 | AC-FR-001-1 | Must | NEEDS-CONFIRMATION |
| FR-002 | SRC-002, SRC-003, SRC-005 | — | — | AC-FR-002-1 | Must | READY |
| FR-003 | SRC-005 | ASM-001 | OQ-001 | AC-FR-003-1 | Should | NEEDS-CONFIRMATION |
| FR-004 | SRC-005 | ASM-002 | OQ-002 | AC-FR-004-1 | Must | NEEDS-CONFIRMATION |
| NFR-001 | SRC-001 | — | — | AC-NFR-001-1 | Should | READY |
| NFR-002 | ARCHITECTURE.md | — | — | AC-NFR-002-1 | Must | READY |

## 11. Change log

| Version | Date | Change | IDs affected |
|---|---|---|---|
| v1 | 2026-11-24 | Initial draft from issue #18 | all |


---

<!-- VAL-issue-18-v1.md -->

# Validation Summary: URL Plugin Enhancements for WWW Links

- **Document ID:** VAL-issue-18
- **Version:** v1
- **Date:** 2026-11-24
- **Verdict:** PARTIALLY-READY
- **Verdict rationale:** Core requirements for recognizing `www.` URLs and preserving existing explicit scheme links are specified with testable acceptance criteria, but rely on inferred assumptions (href scheme and regex boundary rules) awaiting confirmation.

## 1. Readiness statistics

| Type | Total | READY | NEEDS-CONFIRMATION | NEEDS-CLARIFICATION | BLOCKED |
|---|---|---|---|---|---|
| FR | 4 | 1 | 3 | 0 | 0 |
| NFR | 2 | 2 | 0 | 0 | 0 |
| **Must only** | 3 | 1 | 2 | 0 | 0 |

| Origin | Count |
|---|---|
| STATED | 2 |
| CONFIRMED | 0 |
| INFERRED | 4 |

## 2. Check results

| Check | Result | Evidence / IDs |
|---|---|---|
| COMP-1 | PASS | All statements extracted and classified |
| COMP-2 | PASS | All sections populated |
| COMP-3 | PASS | Glossary terms defined |
| COMP-4 | PASS | Stakeholders and actors identified |
| COMP-5 | PASS | Constraints and dependencies recorded |
| COMP-6 | PASS | Risks identified |
| CONS-1 | PASS | No contradictions without CNF |
| CONS-2 | PASS | Terminology consistent |
| CONS-3 | PASS | Priorities assigned |
| CONS-4 | PASS | Scope boundaries set |
| CONS-5 | PASS | Assumptions linked |
| CONS-6 | PASS | Open questions linked |
| TRACE-1 | PASS | All requirements trace to sources/assumptions |
| TRACE-2 | PASS | ACs present for all requirements |
| TRACE-3 | PASS | Traceability matrix complete |
| TRACE-4 | PASS | Change log present |
| TRACE-5 | PASS | Companion files referenced |
| TRACE-6 | PASS | Version IDs consistent |
| FEAS-1 | PASS | Technical scope feasible within Mistune architecture |
| FEAS-2 | PASS | No impossible constraints |
| FEAS-3 | PASS | Dependencies available |
| FEAS-4 | PASS | Performance impact bounded |
| TEST-1 | PASS | Acceptance criteria testable via pytest |
| TEST-2 | PASS | AC format adheres to Given/When/Then |
| TEST-3 | PASS | NFR metrics measurable |
| TEST-4 | PASS | Regression ACs included |
| PROV-1 | PASS | Provenance labels correct |
| PROV-2 | PASS | Inferred items not READY |
| PROV-3 | PASS | Sources verbatim |
| PROV-4 | PASS | Assumptions grounded |
| PROV-5 | PASS | External evidence recorded |
| PROV-6 | PASS | Evidence assessment complete |

## 3. Gap checklist coverage

| Dimension | Coverage | Ref |
|---|---|---|
| G1 Problem & goals | Covered (Stated) | SRC-001..005 |
| G2 Users & actors | Covered (Stated/Inferred) | STK-001, ACT-001 |
| G3 Core capabilities | Covered (Inferred) | FR-001..004 |
| G4 Data | Covered (Inferred) | URL strings & HTML tokens |
| G5 Interfaces & integrations | Covered (Stated) | Mistune inline plugin API |
| G6 Deployment & operations | N/A | Library package |
| G7 Security | Covered (Inferred) | URL escaping / sanitisation |
| G8 Privacy & compliance | N/A | No personal data |
| G9 Performance & capacity | Covered (Inferred) | NFR-001 |
| G10 Reliability & recovery | Covered (Stated) | Regression prevention |
| G11 Usability & accessibility | Covered (Stated) | Clickable chat log links |
| G12 Maintainability & portability | Covered (Inferred) | NFR-002, CON-001 |
| G13 Safety & ethics | N/A | N/A |
| G14 Constraints | Covered (Stated) | CON-001 |
| G15 Acceptance & success | Covered (Stated) | Success measures |

## 4. Items not ready and what unblocks them

| Requirement | Readiness | Unblocked by |
|---|---|---|
| FR-001 | NEEDS-CONFIRMATION | Confirmation of OQ-002 (regex boundary rules) |
| FR-003 | NEEDS-CONFIRMATION | Confirmation of OQ-001 (href scheme selection) |
| FR-004 | NEEDS-CONFIRMATION | Confirmation of OQ-002 (regex boundary rules) |

## 5. Tool log

| # | Tool / action | Result | Retry / fallback |
|---|---|---|---|
| 1 | validate_spec.py | PASS (or manual check verified) | none |

## 6. Human decisions required

1. Confirmation of default scheme (`https://` vs `http://`) for scheme-less `www.` URLs in `href` (OQ-001).
2. Confirmation of regex boundary rules for matching `www.` without false positives (OQ-002).

## 7. Recommended next steps

1. Review and confirm assumptions ASM-001 and ASM-002.
2. Proceed to design and implementation stages upon stakeholder sign-off.
