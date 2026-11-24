## AutoSE independent review, round 1: ❌ REQUEST CHANGES

**Route:** `code` · **Reviewer model:** `gemini-3.5-flash-lite` · **Variant:** `baseline` · PR #21

The PR adds the requested `link_rel` option to HTMLRenderer, but unfortunately bypasses URL sanitization when `link_rel` is set, creating an XSS vulnerability with `javascript:` links.

### What the reviewer checked
- uv run pytest -q --tb=short
- uv run ruff check .
- uv run mypy src
- uv run python -c "import mistune; md = mistune.create_markdown(renderer=mistune.HTMLRenderer(link_rel='nofollow'), plugins=['url']); print(md('[site](javascript:alert(1))'))"

### Findings
| Severity | Where | Problem | Evidence | Suggestion |
|---|---|---|---|---|
| blocker | `src/mistune/renderers/html.py:129` | When `link_rel` is specified, `href` is set directly to `url` without calling `self.sanitize_url(url)`, bypassing URL sanitization and allowing dangerous protocols like `javascript:`. | Command: uv run python -c "import mistune; md = mistune.create_markdown(renderer=mistune.HTMLRenderer(link_rel='nofollow'), plugins=['url']); print(md('[site](javascript:alert(1))'))" -> Output: <p><a href="javascript:alert(1)" rel="nofollow">site</a></p> | Always sanitize the URL via `self.sanitize_url(url)` when building link attributes, regardless of `link_rel`: `attrs: Dict[str, object] = {"href": self.sanitize_url(url)}; if self._link_rel: attrs["rel"] = self._link_rel`. |

_The reviewer saw only the issue, the diff and the PR-head checkout. It cannot push. A human decides whether to merge._
