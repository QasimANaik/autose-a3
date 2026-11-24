# Hidden acceptance tests

Kept **outside** the fork so no agent can see them. Run against any ref of the fork with
`experiment/scripts/eval_hidden.sh <ref> <issue>`; output goes to `results/hidden/`.

Baseline at `f7ec702` (main), verified 2026-11-23:

| Issue | GitHub | Type | Hidden tests | Fail on base | Pass on base (regression guards) |
|---|---|---|---|---|---|
| 1 | [#1](https://github.com/QasimANaik/mistune/issues/1) | bug: table rows with missing/extra cells | 4 | 4 | 0 |
| 2 | [#2](https://github.com/QasimANaik/mistune/issues/2) | bug: url plugin parens / trailing `?` `!` | 4 | 3 | 1 (`unbalanced_closing_paren_still_excluded`) |
| 3 | [#3](https://github.com/QasimANaik/mistune/issues/3) | feature: `HTMLRenderer(link_rel=...)` | 4 | 3 | 1 (`default_output_unchanged`) |
| 4 | [#4](https://github.com/QasimANaik/mistune/issues/4) | feature: `render_toc_ul(..., ordered=True)` | 4 | 3 | 1 (`default_unchanged`) |
| 5 | [#5](https://github.com/QasimANaik/mistune/issues/5) | vague: "math breaks my page layout" (inline `$$..$$` → `<div>` inside `<p>`) | 4 | 1 | 3 (one-paragraph + 2 regression guards) |
| 18 | [#18](https://github.com/QasimANaik/mistune/issues/18) | **vague (replaces #5):** "some links in our chat logs are not clickable" (`www.` addresses not autolinked by the url plugin) | 4 | 2 | 2 (existing https links, code/non-addresses unchanged) |

Interpretation chosen for the vague issue 5 is written in the test module docstring.

**Issue #5 was closed (not planned) on 2026-11-24 and replaced by #18** as the vague issue. Its underlying change (inline `$$` math) proved hard for the cheap model (runs 3 and 4 in results/runs.md, plus run 45374180590). #18 was checked before use: no existing upstream test pins the behaviour (no `www.` cases in tests/fixtures/url.txt), and a throwaway reference fix of 3 lines in 2 files (`plugins/url.py` pattern + scheme, `inline_parser.py` url_link trigger chars) passes 4/4 hidden tests and the full suite (1327 passed). The reference fix was discarded and never pushed.
