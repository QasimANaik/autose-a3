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
