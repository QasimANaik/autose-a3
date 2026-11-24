# Seeded PRs (reviewer check, experiment E1)

Five human-authored PRs in the fork, each targeting one experiment issue. Four contain a planted defect, and one is
clean. The ground truth (`labels.csv`) and the diffs (`*.patch`) live here, outside the fork. PR descriptions only
say that the PR is a seeded calibration PR that must never be merged. The reviewer never receives the PR body, title or labels: it gets the linked issue,
the diff and the PR-head checkout only.

| Seeded | PR | Issue | Planted defect | Expected |
|---|---|---|---|---|
| sp-1 | [#20](https://github.com/QasimANaik/mistune/pull/20) | #4 | incomplete fix: nested TOC levels stay `<ul>` | request changes (code) |
| sp-2 | [#21](https://github.com/QasimANaik/mistune/pull/21) | #3 | XSS: `javascript:` URLs bypass `sanitize_url()` when `link_rel` is set | request changes (code) |
| sp-3 | [#22](https://github.com/QasimANaik/mistune/pull/22) | #1 | correct fix, but its new tests assert nothing | request changes (code) |
| sp-4 | [#23](https://github.com/QasimANaik/mistune/pull/23) | #2 | wrong layer: hack in `HTMLRenderer.link()` breaks `<https://…?>` autolinks | request changes (approach) |
| sp-5 | [#24](https://github.com/QasimANaik/mistune/pull/24) | #18 | none (clean, correct) | approve |

Every branch was verified before review: the full suite passes, ruff and strict mypy are clean, and the hidden tests
give the results in `labels.csv`. Each defect was demonstrated with a probe (see `how_to_see_it`), so none of them is
visible just from a failing test run.

Reviews: `/autose review` (baseline) and `/autose review variant=weak_reviewer` (E1) on each PR. Results are in
`results/results.csv` (kind = `seeded`).
