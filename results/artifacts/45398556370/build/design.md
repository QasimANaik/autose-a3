## Summary
Enhance the `url` plugin in `src/mistune/plugins/url.py` to recognize scheme-less raw URLs starting with `www.` in addition to existing `http://` and `https://` links. The URL pattern uses word boundaries to prevent false positives (such as `my_www.example`), and `parse_url_link` automatically prefixes `www.` URLs with `https://` in generated `href` attributes. This provides seamless auto-linking for chat logs and user-pasted text matching standard expectations without breaking existing behavior.

## Files and functions to change
- `src/mistune/plugins/url.py`: `parse_url_link`, `url`
- `tests/fixtures/url.txt`

## Existing tests to update
None

## Plan
1. Update `URL_LINK_PATTERN` in `src/mistune/plugins/url.py` to match `\b(?:https?:\/\/|www\.)[^\s<]+[^<.,:;"')\]\s]` (satisfies FR-001, FR-002, FR-004).
2. Update `parse_url_link` in `src/mistune/plugins/url.py` to prepend `https://` to `www.` links when generating the `href` attribute (satisfies FR-003).
3. Add test cases for `www.` URLs, explicit scheme URLs, and non-link false positives (`my_www.example`) to `tests/fixtures/url.txt` (satisfies AC-FR-001-1, AC-FR-002-1, AC-FR-003-1, AC-FR-004-1).
4. Validate changes using `uv run pytest`, `uv run mypy`, and `uv run ruff check .` (satisfies NFR-001, NFR-002).

## Risks
- **Over-matching / false positives:** Substrings containing `www.` preceded by word characters (e.g., `my_www.example`) must not be matched as URLs. This is mitigated by using the `\b` word boundary assertion in the regular expression.
- **Malformed or incomplete URLs:** Edge cases with trailing punctuation or brackets are handled by existing negative character classes and bracket handling logic in `parse_url_link`.
- **Type safety and linting:** All modifications must maintain strict typing compatible with `uv run mypy` and pass `uv run ruff check .`.


---
## Stage 2 check (orchestrator)

**PASS**

- (no problems found)
