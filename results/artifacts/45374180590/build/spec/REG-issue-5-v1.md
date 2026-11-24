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
