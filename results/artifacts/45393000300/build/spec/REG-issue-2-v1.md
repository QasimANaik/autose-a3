# Assumptions and Open-Questions Register: Mistune URL Plugin Link Parsing Fix

- **Document ID:** REG-issue-2
- **Version:** v1
- **Date:** 2026-11-24

## 1. Open questions

### OQ-001 — Unbalanced or nested parentheses inside URLs
- **Question:** Should URLs containing unbalanced or complex nested parentheses (e.g. `https://example.com/a(b)c)`) terminate at the outer closing parenthesis or treat them as part of the URL?
- **Why it matters:** Affects regex pattern matching for edge-case URLs.
- **Options:** (a) Match balanced parentheses using standard rules (b) Allow any trailing parenthesis if opened (c) Stick to standard GitHub-compatible balanced parenthesis rules.
- **Default if unanswered:** ASM-001 (GitHub-compatible balanced parentheses)
- **Owner:** STK-001
- **Blocking:** no
- **Affects:** FR-001
- **Status:** ANSWERED
- **Answer:** Follow GitHub-compatible balanced parentheses rules. (SRC-001)

## 2. Assumptions

### ASM-001 — GitHub-compatible URL parsing behavior
- **Statement:** The URL plugin should adopt GitHub's rule where balanced parentheses are included in URLs and trailing punctuation such as `?`, `!`, `.`, and `,` are stripped from the end of URLs.
- **Basis:** Explicitly requested in issue description ("GitHub keeps balanced parentheses in the URL and drops trailing punctuation like `?` and `!`").
- **Origin:** STATED
- **Status:** CONFIRMED
- **Confirm via:** SRC-001
- **Affects:** FR-001, FR-002, FR-003

## 3. Conflicts

### None identified
- **Description:** No conflicts between sources or constraints.

## 4. Out of scope

### OOS-001 — Custom URL Schemes and Whitelisting
- **Item:** Custom non-HTTP/HTTPS URL schemes or domain-specific URL filtering.
- **Basis:** Not requested by any source.
- **Origin:** STATED

## 5. Evidence assessment
- **Claim:** External evidence not used in batch offline mode. (REF-001: NOT-RUN)
