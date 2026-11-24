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
