# Assumptions and Open-Questions Register: Table row cell count tolerance (issue-1)

- **Document ID:** REG-issue-1
- **Version:** v1
- **Date:** 2026-11-24

## 1. Open questions

### OQ-001 — Short row padding placement
- **Question:** Should table rows with fewer cells than the header be padded with empty cells at the end of the row, or distributed across columns?
- **Why it matters:** Determines cell alignment when columns are omitted on the right vs middle.
- **Options:** (a) Pad at the end (trailing missing cells), (b) Pad at matching positions, (c) Other
- **Default if unanswered:** ASM-001 (pad at the end with empty cells)
- **Owner:** STK-001
- **Blocking:** no
- **Affects:** FR-001
- **Status:** OPEN
- **Answer:** —

## 2. Assumptions

### ASM-001 — Trailing empty cell padding
- **Statement:** Rows with fewer cells than the header are missing trailing cells and should be padded with empty `<td></td>` cells at the end.
- **Basis:** Proposal matching GitHub and standard Markdown tool behavior cited in SRC-002 ("someone forgot a trailing `|` value").
- **Origin:** INFERRED
- **Status:** OPEN
- **Confirm via:** OQ-001
- **Affects:** FR-001

### ASM-002 — Excess cell truncation
- **Statement:** Rows with more cells than the header have extra trailing cells that should be dropped.
- **Basis:** Proposal matching GitHub and standard Markdown tool behavior cited in SRC-002.
- **Origin:** INFERRED
- **Status:** OPEN
- **Confirm via:** None
- **Affects:** FR-002

## 3. Conflicts

### CNF-001 — None identified
- **Claim A:** —
- **Claim B:** —
- **Nature:** —
- **Affects:** —
- **Resolution options:** —
- **Decision owner:** —
- **Status:** RESOLVED

## 4. Out of scope

### OOS-001 — Automatic column header inference from body row cell count
- **Item:** Automatically expanding the table header if a body row has more cells than the header.
- **Basis:** Not requested in issue #1; issue explicitly states extra cell should be dropped.
- **Origin:** STATED

## 5. Evidence assessment

| Claim | Sources (REF) | Assessment | Effect on spec |
|---|---|---|---|
| N/A | REF-001 | Not used | none |
