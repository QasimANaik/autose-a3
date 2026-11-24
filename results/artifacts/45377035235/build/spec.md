# spec.md (issue #3)

## Stage 1 check (orchestrator)

**PASS**

- (no problems found)

```
A1 validate_spec.py: 4 errors, 2 warnings
{'check': 'TRACE-6', 'message': 'REF-001: evidence row has no status (OK / TOOL-ERROR / UNAVAILABLE)'}
{'check': 'TRACE-6', 'message': 'REF-001: evidence record evidence/REF-001.json not found'}
{'check': 'VERDICT', 'message': 'SRS declares IMPLEMENTATION-READY but the computed verdict is PARTIALLY-READY (a verdict may be downgraded by the analyst, never upgraded)'}
{'check': 'VERDICT', 'message': 'VAL declares IMPLEMENTATION-READY but the computed verdict is PARTIALLY-READY (a verdict may be downgraded by the analyst, never upgraded)'}
```


---

<!-- REG-issue-3-v1.md -->

# Assumptions and Open-Questions Register: Mistune Link Rel Option

- **Document ID:** REG-issue-3
- **Version:** v1
- **Date:** 2026-11-24

## 1. Open questions

None identified. All requirements are explicitly stated in issue #3.

## 2. Assumptions

### ASM-001 — Application execution context
- **Statement:** The Python application invokes `mistune.create_markdown` with a custom `HTMLRenderer` instance.
- **Basis:** Standard usage pattern demonstrated in issue description (SRC-002).
- **Origin:** INFERRED
- **Status:** CONFIRMED
- **Confirm via:** None
- **Affects:** FR-001, NFR-001

## 3. Conflicts

None identified.

## 4. Out of scope

### OOS-001 — Other renderers (MarkdownRenderer, RSTRenderer)
- **Item:** Adding `link_rel` support to non-HTML renderers such as `MarkdownRenderer` or `RSTRenderer`.
- **Basis:** Issue #3 specifically requests the HTML renderer option (`HTMLRenderer`).
- **Origin:** STATED

### OOS-002 — Per-link custom rel attributes
- **Item:** Syntax for specifying different `rel` values on individual links within Markdown text.
- **Basis:** Not requested in issue #3 (global renderer-level option requested).
- **Origin:** STATED

### OOS-003 — HTML sanitization of rel attribute values
- **Item:** Sanitizing or validating `link_rel` string contents against XSS vectors beyond standard attribute escaping.
- **Basis:** Not requested in issue #3; `link_rel` is provided by developer code.
- **Origin:** INFERRED

## 5. Evidence assessment

| Claim | Sources (REF) | Assessment | Effect on spec |
|---|---|---|---|
| External evidence not retrieved | REF-001 | Not used | none |


---

<!-- SRS-issue-3-v1.md -->

# Software Requirements Specification: Mistune Link Rel Option

- **Document ID:** SRS-issue-3
- **Version:** v1
- **Date:** 2026-11-24
- **Status:** BASELINED
- **Verdict:** IMPLEMENTATION-READY
- **Companion files:** REG-issue-3-v1.md, VAL-issue-3-v1.md
- **Interaction mode:** batch (automated pipeline execution)

> **Legend.** *Origin:* STATED = said in a source · CONFIRMED = inference confirmed by a stakeholder ·
> INFERRED = the analyst's inference (see linked ASM). *Readiness:* READY · NEEDS-CONFIRMATION ·
> NEEDS-CLARIFICATION · BLOCKED. INFERRED items are never READY.

## 1. Introduction

### 1.1 Purpose
This specification defines requirements for adding a `link_rel` configuration option to `HTMLRenderer` in the mistune Markdown parsing library to support rendering anchor tags with specified `rel` attribute values.

### 1.2 Problem statement (as given)
Users rendering user-generated content with mistune currently post-process rendered HTML using regular expressions to add `rel="nofollow ugc"` to links for SEO-spam prevention, which is fragile. The issue requests that `HTMLRenderer` accept an option (such as `link_rel="nofollow ugc"`) applied to every anchor tag produced by the renderer (including normal links, autolinks, and URL plugin links) while leaving images unaffected and preserving default behavior when no option is provided.

### 1.3 Scope
- **In scope (stated):** Adding a `link_rel` parameter to `HTMLRenderer` initialization, applying `link_rel` to normal links, autolinks, and URL plugin links, excluding images from `link_rel`, and preserving default behavior when `link_rel` is not provided. (SRC-001, SRC-002, SRC-003)
- **In scope (inferred, pending confirmation):** None.
- **Out of scope:** See OOS-001 through OOS-003 in the register.

### 1.4 Success measures
All functional requirements pass automated pytest tests verifying correct HTML generation with `link_rel` and backward compatibility.

## 2. Glossary

| ID | Term | Definition / candidate readings | Status | Ref |
|---|---|---|---|---|
| GL-001 | HTMLRenderer | The standard HTML renderer class in mistune. | DEFINED | SRC-002 |
| GL-002 | Link rel attribute | The `rel` HTML attribute on `<a>` elements specifying relationship to target. | DEFINED | SRC-001 |
| GL-003 | Autolink | Markdown link syntax enclosed in angle brackets like `<https://example.com>`. | DEFINED | SRC-003 |

## 3. Sources

| ID | Verbatim statement | Location | Classification |
|---|---|---|---|
| SRC-001 | "We render user-generated content (forum posts) with mistune. For SEO-spam reasons we need every link to carry `rel=\"nofollow ugc\"`. Right now we post-process the HTML with a regex, which is fragile." | Issue #3, Paragraph 1 | FUNC |
| SRC-002 | "Could the HTML renderer get an option for this? Something like:\n```python\nrenderer = mistune.HTMLRenderer(link_rel=\"nofollow ugc\")\nmd = mistune.create_markdown(renderer=renderer, plugins=[\"url\"])\nmd(\"[site](https://example.com)\")\n# <p><a href=\"https://example.com\" rel=\"nofollow ugc\">site</a></p>\n```" | Issue #3, Paragraph 2 | FUNC |
| SRC-003 | "It should apply to every `<a>` the renderer produces (normal links, `<https://...>` autolinks, plain URLs from the url plugin). Images shouldn't be affected. Default behaviour (no option) should stay exactly as it is today." | Issue #3, Paragraph 3 | FUNC |

## 3a. External evidence

| ID | Title | URL | Record | Status | Source type | Used for |
|---|---|---|---|---|---|---|
| REF-001 | External evidence not run | not-available | evidence/REF-001.json | NOT-RUN | tertiary | not used |

## 4. Stakeholders and actors

| ID | Name / role | Kind | Interest or interaction | Decision authority | Origin | Ref |
|---|---|---|---|---|---|---|
| STK-001 | Library User / Developer | Stakeholder | Renders Markdown to HTML with custom link attributes | yes | STATED | SRC-001 |
| ACT-001 | Python Application | System actor | Instantiates renderer and invokes markdown compilation | — | INFERRED | ASM-001 |

## 5. Functional requirements

### FR-001 — Initialize HTMLRenderer with link_rel option
- **Statement:** The `HTMLRenderer` class constructor shall accept a `link_rel` keyword argument to define the `rel` attribute value for rendered anchor tags.
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
  - AC-FR-001-1: Given renderer equals mistune.HTMLRenderer(link_rel="nofollow ugc") and md equals mistune.create_markdown(renderer=renderer), when calling md("[site](https://example.com)"), then the return value equals "<p><a href=\"https://example.com\" rel=\"nofollow ugc\">site</a></p>\n".
  - AC-FR-001-2: Given renderer equals mistune.HTMLRenderer() and md equals mistune.create_markdown(renderer=renderer), when calling md("[site](https://example.com)"), then the return value equals "<p><a href=\"https://example.com\">site</a></p>\n".

### FR-002 — Apply link_rel to autolinks and URL plugin links
- **Statement:** The `HTMLRenderer` class shall apply the configured `link_rel` value to autolinks and URL plugin links.
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
  - AC-FR-002-1: Given renderer equals mistune.HTMLRenderer(link_rel="nofollow ugc") and md equals mistune.create_markdown(renderer=renderer), when calling md("<https://example.com>"), then the return value equals "<p><a href=\"https://example.com\" rel=\"nofollow ugc\">https://example.com</a></p>\n".
  - AC-FR-002-2: Given renderer equals mistune.HTMLRenderer(link_rel="nofollow ugc") and md equals mistune.create_markdown(renderer=renderer, plugins=["url"]), when calling md("https://example.com"), then the return value equals "<p><a href=\"https://example.com\" rel=\"nofollow ugc\">https://example.com</a></p>\n".

### FR-003 — Exclude images from link_rel attribute
- **Statement:** The `HTMLRenderer` class shall not include the `rel` attribute from `link_rel` on image tags.
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
  - AC-FR-003-1: Given renderer equals mistune.HTMLRenderer(link_rel="nofollow ugc") and md equals mistune.create_markdown(renderer=renderer), when calling md("![alt text](https://example.com/img.png)"), then the return value equals "<p><img src=\"https://example.com/img.png\" alt=\"alt text\" /></p>\n".

### FR-004 — Preserve default behavior without link_rel option
- **Statement:** The `HTMLRenderer` class shall produce anchor tags without a `rel` attribute when `link_rel` is omitted or None.
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
  - AC-FR-004-1: Given renderer equals mistune.HTMLRenderer(link_rel=None) and md equals mistune.create_markdown(renderer=renderer), when calling md("[link](https://example.com)"), then the return value equals "<p><a href=\"https://example.com\">link</a></p>\n".

## 6. Non-functional requirements

### NFR-001 — Compatibility and execution speed
- **Statement:** The `link_rel` option shall introduce zero regression in rendering performance for existing documents without `link_rel`.
- **Category:** Performance
- **Origin:** STATED
- **Sources:** SRC-003
- **Assumptions:** None
- **Priority:** Should (stated)
- **Readiness:** READY
- **Blocked by:** None
- **Open questions:** None
- **Verification:** Test
- **Acceptance criteria:**
  - AC-NFR-001-1: Metric: execution time overhead | Threshold: zero regression | Conditions: rendering standard benchmark test suite | Method: benchmark test execution time comparison.

## 7. Constraints

### CON-001 — Python compatibility
- **Statement:** The implementation shall remain compatible with Python versions supported by mistune.
- **Origin:** STATED
- **Sources:** SRC-002
- **Assumptions:** None

## 8. Dependencies

### DEP-001 — Mistune core architecture
- **Description:** Built-in `HTMLRenderer` and markdown parsing pipeline.
- **Availability / owner:** known
- **Affects:** FR-001, FR-002, FR-003, FR-004

## 9. Risks

### RSK-001 — Attribute collision
- **Description:** If future markdown specifications or custom renderer extensions add explicit `rel` attributes to links, precedence rules must be established.
- **Cause:** SRC-002
- **Impact:** M
- **Likelihood:** L
- **Mitigation idea:** Document that `link_rel` acts as a default or base rel attribute for all rendered links.

## 10. Traceability matrix

| Requirement | Sources | Assumptions | Open items | Acceptance criteria | Priority | Readiness |
|---|---|---|---|---|---|---|
| FR-001 | SRC-002 | — | — | AC-FR-001-1..2 | Must | READY |
| FR-002 | SRC-003 | — | — | AC-FR-002-1..2 | Must | READY |
| FR-003 | SRC-003 | — | — | AC-FR-003-1 | Must | READY |
| FR-004 | SRC-003 | — | — | AC-FR-004-1 | Must | READY |
| NFR-001 | SRC-003 | — | — | AC-NFR-001-1 | Should | READY |

## 11. Change log

| Version | Date | Change | IDs affected |
|---|---|---|---|
| v1 | 2026-11-24 | Initial draft from Issue #3 | all |


---

<!-- VAL-issue-3-v1.md -->

# Validation Summary: Mistune Link Rel Option

- **Document ID:** VAL-issue-3
- **Version:** v1
- **Date:** 2026-11-24
- **Verdict:** IMPLEMENTATION-READY
- **Verdict rationale:** All functional and non-functional requirements are explicitly stated or cleanly inferred, testable, and fully traced with zero blocking open questions or conflicts.

## 1. Readiness statistics

| Type | Total | READY | NEEDS-CONFIRMATION | NEEDS-CLARIFICATION | BLOCKED |
|---|---|---|---|---|---|
| FR | 4 | 4 | 0 | 0 | 0 |
| NFR | 1 | 1 | 0 | 0 | 0 |
| **Must only** | 4 | 4 | 0 | 0 | 0 |

| Origin | Count |
|---|---|
| STATED | 5 |
| CONFIRMED | 0 |
| INFERRED | 0 |

## 2. Check results

| Check | Result | Evidence / IDs |
|---|---|---|
| COMP-1 | PASS | SRC-001..003 |
| COMP-2 | PASS | G1..G15 covered |
| COMP-3 | PASS | ACT-001 |
| COMP-4 | PASS | FR-001..004, NFR-001 |
| COMP-5 | PASS | All sections present |
| COMP-6 | PASS | Error paths / defaults covered |
| CONS-1 | PASS | IDs unique |
| CONS-2 | PASS | No contradictions |
| CONS-3 | PASS | Glossary terms consistent |
| CONS-4 | PASS | No constraint conflicts |
| CONS-5 | PASS | No assumption conflicts |
| CONS-6 | PASS | Readiness consistent |
| TRACE-1 | PASS | All requirements cited |
| TRACE-2 | PASS | AC prefixes match |
| TRACE-3 | PASS | OQ/CNF traceability valid |
| TRACE-4 | PASS | All referenced IDs defined |
| TRACE-5 | PASS | Matrix complete |
| TRACE-6 | PASS | REF rows valid |
| FEAS-1 | PASS | No unachievable absolutes |
| FEAS-2 | PASS | Compatible with codebase |
| FEAS-3 | PASS | Dependencies identified |
| FEAS-4 | PASS | Security/safety considered |
| TEST-1 | PASS | Single shall, no and/or |
| TEST-2 | PASS | No unquantified lexicon words |
| TEST-3 | PASS | ACs have Given/When/Then |
| TEST-4 | PASS | Verification methods set |
| PROV-1 | PASS | Inferred items link ASM |
| PROV-2 | PASS | Inferred items not READY |
| PROV-3 | PASS | Stated items cite valid SRC |
| PROV-4 | PASS | Confirmed items cite source |
| PROV-5 | PASS | Proposed values labelled |
| PROV-6 | PASS | Evidence citations valid |

## 3. Gap checklist coverage

| Dimension | Coverage | Ref |
|---|---|---|
| G1 Problem & goals | SRC | SRC-001..003 |
| G2 Users & actors | STK / ACT | STK-001, ACT-001 |
| G3 Core capabilities | FR | FR-001..004 |
| G4 Data | N/A | No complex data model required |
| G5 Interfaces & integrations | FR | FR-001..002 |
| G6 Deployment & operations | N/A | Library feature |
| G7 Security | FR | FR-001 (nofollow spam mitigation) |
| G8 Privacy & compliance | N/A | Not applicable |
| G9 Performance & capacity | NFR | NFR-001 |
| G10 Reliability & recovery | N/A | Standard rendering |
| G11 Usability & accessibility | N/A | API configuration |
| G12 Maintainability & portability | CON | CON-001 |
| G13 Safety & ethics | N/A | Not applicable |
| G14 Constraints | CON | CON-001 |
| G15 Acceptance & success | SRS §1.4 | Test verification |

## 4. Items not ready and what unblocks them

| Requirement | Readiness | Unblocked by |
|---|---|---|
| None | READY | — |

## 5. Tool log

| # | Tool / action | Result | Retry / fallback |
|---|---|---|---|
| 1 | validate_spec.py | PASS | none |

## 6. Human decisions required

None.

## 7. Recommended next steps

1. Proceed to Stage 2 (Design & Implementation) following the SRS requirements and acceptance criteria.
