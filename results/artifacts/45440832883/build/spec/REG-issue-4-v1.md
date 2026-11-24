# Assumptions and Open-Questions Register: render_toc_ul ordered table of contents

- **Document ID:** REG-issue-4
- **Version:** v1
- **Date:** 2026-11-24

## 1. Open questions

### OQ-001 — Parameter naming and validation
- **Question:** Should the keyword argument be named `ordered` or something else, and should non-boolean values raise a TypeError?
- **Why it matters:** Ensures consistency with Python conventions and robust API error handling.
- **Options:** (a) `ordered: bool = False` (b) `numbered: bool = False` (c) other
- **Default if unanswered:** ASM-001 (`ordered: bool = False`)
- **Owner:** STK-001
- **Blocking:** no
- **Affects:** FR-001
- **Status:** OPEN
- **Answer:** —

## 2. Assumptions

### ASM-001 — Keyword argument name and type
- **Statement:** The optional keyword parameter is named `ordered` and accepts a boolean value, defaulting to `False`.
- **Basis:** Proposed explicitly by the user in issue description ("ordered=True").
- **Origin:** INFERRED
- **Status:** OPEN
- **Confirm via:** OQ-001
- **Affects:** FR-001

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

### OOS-001 — Custom tag selection per level
- **Item:** Allowing arbitrary HTML list tags (e.g. mix of `<ol>` and `<ul>` per heading level via custom parameters).
- **Basis:** Not requested by any source; issue requests uniform `<ol>` at every nesting level when `ordered=True`.
- **Origin:** STATED

## 5. Evidence assessment

| Claim | Sources (REF) | Assessment | Effect on spec |
|---|---|---|---|
| External evidence not run | REF-001 | Not used | none |
