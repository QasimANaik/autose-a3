# Assumptions and Open-Questions Register: Mistune Math Plugin Inline Rendering Fix

- **Document ID:** REG-issue-5
- **Version:** v1
- **Date:** 2026-11-24

## 1. Open questions

### OQ-001 — Inline double-dollar math rendering behavior
- **Question:** Should double-dollar math syntax (`$$\dots$$`) in the middle of a sentence be treated as inline math (`<span class="math">`) instead of block math (`<div class="math">`)?
- **Why it matters:** Resolves paragraph splitting and HTML validation errors reported in issue #5.
- **Options:** (a) Yes, render as inline math (`<span class="math">`). (b) No, keep rendering as block math (`<div class="math">`). (c) Other custom rendering.
- **Default if unanswered:** (a) Render as inline math (`<span class="math">`).
- **Owner:** Maintainer / Project Author
- **Blocking:** no
- **Affects:** FR-001
- **Status:** OPEN
- **Answer:** —

## 2. Assumptions

### ASM-001 — Inline equation intent
- **Statement:** Users writing `$$\dots$$` in the middle of a sentence intend inline math that formats correctly without breaking containing paragraphs.
- **Basis:** Issue #5 description ("equations in the middle of a sentence... paragraph is split in two... HTML validator complains").
- **Origin:** INFERRED
- **Status:** OPEN
- **Confirm via:** OQ-001
- **Affects:** FR-001

## 3. Conflicts

### None identified
- **Basis:** No conflicting statements or constraints found in the problem statement.

## 4. Out of scope

### OOS-001 — Frontend MathJax configuration
- **Item:** Changes to frontend MathJax script configuration or styling sheets.
- **Basis:** Not requested by any source (issue mentions using MathJax on the frontend, but expects Mistune library output to be valid).
- **Origin:** STATED

## 5. Evidence assessment

| Claim | Sources (REF) | Assessment | Effect on spec |
|---|---|---|---|
| External evidence not retrieved | REF-001 | Not used | none |
