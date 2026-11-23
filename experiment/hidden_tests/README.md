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

Interpretation chosen for the vague issue 5 is written in the test module docstring.
