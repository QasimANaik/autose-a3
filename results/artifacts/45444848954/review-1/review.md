## AutoSE independent review, round 1: ❌ REQUEST CHANGES

**Route:** `approach` · **Reviewer model:** `gemini-3.5-flash-lite` · **Variant:** `baseline` · PR #23

The PR fails to implement half of the issue (Wikipedia links with parentheses) and places URL parsing/punctuation logic in the generic HTML renderer instead of the URL plugin.

### What the reviewer checked
- uv run pytest -q --tb=short
- uv run python -c 'import mistune; md = mistune.create_markdown(plugins=["url"]); print(repr(md("see https://en.wikipedia.org/wiki/Python_(programming_language) for details")))'
- uv run python -c 'import mistune; md = mistune.create_markdown(plugins=["url"]); print(repr(md("did you try https://example.com/docs?")))'
- uv run ruff check .
- uv run mypy src/mistune

### Findings
| Severity | Where | Problem | Evidence | Suggestion |
|---|---|---|---|---|
| blocker | `src/mistune/renderers/html.py:126` | Pull request completely fails to address part 1 of the issue: Wikipedia links with parentheses get cut off. | uv run python -c 'import mistune; md = mistune.create_markdown(plugins=["url"]); print(repr(md("see https://en.wikipedia.org/wiki/Python_(programming_language) for details")))' -> '<p>see <a href="https://en.wikipedia.org/wiki/Python_(programming_language">https://en.wikipedia.org/wiki/Python_(programming_language</a>) for details</p>\n' | Update the URL plugin pattern and parser to properly handle balanced parentheses in URLs (such as Wikipedia links) as well as trailing punctuation. |
| major | `src/mistune/renderers/html.py:126` | Trailing punctuation trimming is placed in `HtmlRenderer.link` rather than the `url` plugin, causing it to apply globally to all standard Markdown links (`[text](url)`) rather than just raw auto-linked URLs. | src/mistune/renderers/html.py:126-130 | Move URL cleaning and punctuation/parentheses adjustment logic into `src/mistune/plugins/url.py` (`URL_LINK_PATTERN` and `parse_url_link`). |

_The reviewer saw only the issue, the diff and the PR-head checkout. It cannot push. A human decides whether to merge._
