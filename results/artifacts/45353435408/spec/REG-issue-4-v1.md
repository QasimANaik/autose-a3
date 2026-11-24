# Assumptions and Open-Questions Register: Mistune Table of Contents Ordered Rendering

- **Document ID:** REG-issue-4
- **Version:** v1
- **Date:** 2026-11-24

## 1. Open questions

- **None identified:** All requirements and parameters requested in the issue are fully specified.

## 2. Assumptions

### ASM-001 — Parameter Default Value
- **Statement:** The `ordered` parameter defaults to `False` to maintain 100% backward compatibility with existing calls to `render_toc_ul`.
- **Basis:** Stated requirement "Without the keyword nothing changes."
- **Origin:** STATED
- **Status:** CONFIRMED
- **Confirm via:** None (stated in source)
- **Affects:** FR-002

## 3. Conflicts

- **None identified:** No conflicting claims or requirements found.

## 4. Out of scope

### OOS-001 — Built-in Markdown directive syntax for ordered TOC
- **Item:** Adding a fenced directive syntax (e.g. ````{toc} :ordered: true````) is not explicitly requested by the issue author, who specifically requested keyword parameterization on `render_toc_ul`.
- **Basis:** Not requested by source (SRC-001).
- **Origin:** STATED

## 5. Evidence assessment

| Claim | Sources (REF) | Assessment | Effect on spec |
|---|---|---|---|
| N/A | N/A | Not used | none |
