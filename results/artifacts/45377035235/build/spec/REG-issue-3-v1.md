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
