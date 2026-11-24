# Runs

Every AutoSE workflow run on the fork, with links to its Actions run, pull request and posted review. Generated from
`results/results.csv`. Costs use Gemini Standard paid-tier list prices per 1M tokens (in / cached / out):
gemini-3-flash-preview $0.50 / $0.05 / $3.00, gemini-3.5-flash-lite $0.30 / $0.03 / $2.50 (aistudio.google.com/docs/pricing,
2026-11-24). Token counts come from each agent call's `usage/*.json`. Artifacts of the runs since run 7 are in `results/artifacts/<run id>/`.

## Issue runs (stages 1-6)

| # | Run | Issue | Model | Outcome | Stopped at | Calls | Tokens in (cached) / out | Cost | Min | PR | Review | What it showed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [45234284925](https://github.com/QasimANaik/mistune/actions/runs/45234284925) | #5 | – | skipped | – | 0 | – | $0.00 | 0.0 | – | – | comment was not an /autose command (gate job skipped) |
| 2 | [45234300084](https://github.com/QasimANaik/mistune/actions/runs/45234300084) | #5 | 3-flash-preview | cancelled | build | – | – | – | – | – | – | run cancelled during the build job |
| 3 | [45236521564](https://github.com/QasimANaik/mistune/actions/runs/45236521564) | #5 | 3-flash-preview | needs_clarification (wrong) | spec | 4 | – | $0.00 | – | – | – | model unavailable: 429 free-tier daily limit; fallback gemini-2.5-flash retired -> graph routed to clarify (fixed in PR #7) |
| 4 | [45347324270](https://github.com/QasimANaik/mistune/actions/runs/45347324270) | #5 | 3-flash-preview | failed | implement | 10 | 4.16M (81%) / 31k | $0.66 | – | – | – | 12 existing math tests broken (over-broad change); implement edits to tests reverted; ruff failed on worker test files the implementer may not edit; token cap 4M hit (fixed in PR #7) |
| 5 | [45350365755](https://github.com/QasimANaik/mistune/actions/runs/45350365755) | #4 | 3.5-flash-lite | cancelled | spec | – | – | – | – | – | – | run cancelled during the spec agent call |
| 6 | [45351202045](https://github.com/QasimANaik/mistune/actions/runs/45351202045) | #4 | 3.5-flash-lite | failed | test | 11 | 3.63M (77%) / 19k | $0.38 | – | – | – | code correct (diff passes 4/4 hidden tests + full suite) but AC-FR-001-2 expected a flat list; worker tested it literally; no route for 'the test is wrong' (fixed in PR #9) |
| 7 | [45353435408](https://github.com/QasimANaik/mistune/actions/runs/45353435408) | #4 | 3.5-flash-lite | failed | design | 3 | 0.80M (82%) / 7k | $0.08 | – | – | – | design check parser rejected `name (new)` written inside backticks (fixed in PR #10) |
| 8 | [45354704591](https://github.com/QasimANaik/mistune/actions/runs/45354704591) | #4 | 3.5-flash-lite | **pr_open (autose:done)** | – | 8 | 2.00M (79%) / 15k | $0.21 | 8.3 | [#11](https://github.com/QasimANaik/mistune/pull/11) | [review](https://github.com/QasimANaik/mistune/pull/11#pullrequestreview-6035868107) | all stages first time; 4 parallel test workers; CI green; reviewer approved; hidden tests 4/4 |
| 9 | [45374180590](https://github.com/QasimANaik/mistune/actions/runs/45374180590) | #5 | 3.5-flash-lite | failed | test | 12 | 8.28M (86%) / 30k | $0.64 | 9.8 | – | – | math change kept breaking 2-5 tests through 2 implement loops and a redesign (vague issue #5; later closed and replaced by #18) |
| 10 | [45377035235](https://github.com/QasimANaik/mistune/actions/runs/45377035235) | #3 | 3.5-flash-lite | **pr_open (autose:done)** | – | 7 | 2.94M (66%) / 14k | $0.39 | 8.8 | [#13](https://github.com/QasimANaik/mistune/pull/13) | [review](https://github.com/QasimANaik/mistune/pull/13#pullrequestreview-6037843036) | all stages first time; CI green; reviewer approved after running pytest, ruff, mypy and the issue example |
| 11 | [45379575388](https://github.com/QasimANaik/mistune/actions/runs/45379575388) | #1 | 3.5-flash-lite | failed | test | 10 | 5.51M (82%) / 50k | $0.55 | 12.6 | – | – | correct code (diff passes 4/4 hidden tests) but issue #1 changes behaviour pinned by 8 existing fixture tests (tests/fixtures/table.txt); implementer may not edit tests (fixed in PR #14) |
| 12 | [45393000300](https://github.com/QasimANaik/mistune/actions/runs/45393000300) | #2 | 3.5-flash-lite | **pr_open (autose:done)** | – | 8 | 3.60M (83%) / 18k | $0.31 | 10.2 | [#16](https://github.com/QasimANaik/mistune/pull/16) | [review](https://github.com/QasimANaik/mistune/pull/16#pullrequestreview-6039245574) | design check rejected a backticked `None` in 'Existing tests to update' once; implementer edit to tests/fixtures/url.txt reverted (undeclared) |
| 13 | [45394861968](https://github.com/QasimANaik/mistune/actions/runs/45394861968) | #5 | 3.5-flash-lite | cancelled | build | 5 | 2.76M (85%) / 16k | $0.23 | 18.7 | – | – | cancelled by hand (issue #5 being replaced) |
| 14 | [45394898264](https://github.com/QasimANaik/mistune/actions/runs/45394898264) | #1 | 3.5-flash-lite | **pr_open (autose:done)** | – | 7 | 2.92M (83%) / 22k | $0.28 | 9.9 | [#17](https://github.com/QasimANaik/mistune/pull/17) | [review](https://github.com/QasimANaik/mistune/pull/17#pullrequestreview-6039398765) | re-run after PR #14: design declared tests/fixtures/table.txt (AC-linked), implement updated the 'Invalid Table' expectations; all stages first time |
| 15 | [45398325310](https://github.com/QasimANaik/mistune/actions/runs/45398325310) | #5 | – | skipped | – | 0 | – | $0.00 | – | – | – | comment on the closed issue #5 was not an /autose command; gate job skipped |
| 16 | [45398556370](https://github.com/QasimANaik/mistune/actions/runs/45398556370) | #18 | 3.5-flash-lite | failed | release | 7 | 3.38M (82%) / 20k | $0.31 | 19.3 | [#19](https://github.com/QasimANaik/mistune/pull/19) | – | CI failed only on PyPy 3.11: a generated NFR test runs mypy (and a benchmark) in a subprocess; plus one flaky upstream timing test; CI loop went to implement, which cannot fix a test |
| 17 | [45440832883](https://github.com/QasimANaik/mistune/actions/runs/45440832883) | #4 | 3.5-flash-lite | failed | release | 7 | 2.01M (73%) / 18k | $0.25 | 14.8 | [#11](https://github.com/QasimANaik/mistune/pull/11) | – | re-run of #4: CI failed only on PyPy 3.11 because generated tests assert wall-clock time (<5 ms per 1000 TOC items); flake re-run cannot help |

## Seeded-PR reviews (reviewer check, experiment E1)

Ground truth: `experiment/seeded_prs/labels.csv`.

| Run | Seeded PR | Variant | Verdict (route) | Correct? | Tokens in | Cost | Review |
|---|---|---|---|---|---|---|---|
| [45444827070](https://github.com/QasimANaik/mistune/actions/runs/45444827070) | [#20](https://github.com/QasimANaik/mistune/pull/20) | baseline | request_changes (route code) | yes | 100,897 | $0.017 | [review](https://github.com/QasimANaik/mistune/pull/20#pullrequestreview-6043867261) |
| [45444833603](https://github.com/QasimANaik/mistune/actions/runs/45444833603) | [#21](https://github.com/QasimANaik/mistune/pull/21) | baseline | request_changes (route code) | yes | 98,390 | $0.014 | [review](https://github.com/QasimANaik/mistune/pull/21#pullrequestreview-6043867549) |
| [45444838962](https://github.com/QasimANaik/mistune/actions/runs/45444838962) | [#22](https://github.com/QasimANaik/mistune/pull/22) | baseline | request_changes (route code) | yes | 1,313,841 | $0.346 | [review](https://github.com/QasimANaik/mistune/pull/22#pullrequestreview-6043882603) |
| [45444848954](https://github.com/QasimANaik/mistune/actions/runs/45444848954) | [#23](https://github.com/QasimANaik/mistune/pull/23) | baseline | request_changes (route approach) | yes | 107,903 | $0.015 | [review](https://github.com/QasimANaik/mistune/pull/23#pullrequestreview-6043866791) |
| [45444860902](https://github.com/QasimANaik/mistune/actions/runs/45444860902) | [#24](https://github.com/QasimANaik/mistune/pull/24) | baseline | approve (route none) | yes | 412,637 | $0.044 | [review](https://github.com/QasimANaik/mistune/pull/24#pullrequestreview-6043875408) |
| [45445763935](https://github.com/QasimANaik/mistune/actions/runs/45445763935) | [#20](https://github.com/QasimANaik/mistune/pull/20) | weak_reviewer | error (model unavailable) | – | 0 | $0.000 | [review](https://github.com/QasimANaik/mistune/pull/20#pullrequestreview-6043944624) |
| [45445772635](https://github.com/QasimANaik/mistune/actions/runs/45445772635) | [#21](https://github.com/QasimANaik/mistune/pull/21) | weak_reviewer | error (model unavailable) | – | 0 | $0.000 | [review](https://github.com/QasimANaik/mistune/pull/21#pullrequestreview-6043939555) |
| [45445776522](https://github.com/QasimANaik/mistune/actions/runs/45445776522) | [#22](https://github.com/QasimANaik/mistune/pull/22) | weak_reviewer | error (model unavailable) | – | 0 | $0.000 | [review](https://github.com/QasimANaik/mistune/pull/22#pullrequestreview-6043944141) |
| [45445782304](https://github.com/QasimANaik/mistune/actions/runs/45445782304) | [#23](https://github.com/QasimANaik/mistune/pull/23) | weak_reviewer | error (model unavailable) | – | 0 | $0.000 | [review](https://github.com/QasimANaik/mistune/pull/23#pullrequestreview-6043937962) |
| [45445790671](https://github.com/QasimANaik/mistune/actions/runs/45445790671) | [#24](https://github.com/QasimANaik/mistune/pull/24) | weak_reviewer | error (model unavailable) | – | 0 | $0.000 | [review](https://github.com/QasimANaik/mistune/pull/24#pullrequestreview-6043939611) |

**Totals (27 runs):** 114 agent calls, 44.01M input tokens (34.70M cached, 79%) and 264k output tokens, about **$4.73**.
Hidden acceptance tests: **20/20** on the five bot PR branches (#1, #2, #3, #4, #18); results in `results/hidden/`.

Workflow fixes merged between runs (fork PRs): [#7](https://github.com/QasimANaik/mistune/pull/7), [#8](https://github.com/QasimANaik/mistune/pull/8), [#9](https://github.com/QasimANaik/mistune/pull/9), [#10](https://github.com/QasimANaik/mistune/pull/10), [#12](https://github.com/QasimANaik/mistune/pull/12), [#14](https://github.com/QasimANaik/mistune/pull/14), [#15](https://github.com/QasimANaik/mistune/pull/15).

## Still to run
- E1 weak-reviewer arm: the 5 runs failed because the Gemini prepayment credits were depleted. Re-run with `/autose review variant=weak_reviewer` after topping up.
- E2: design stage with vs without ARCHITECTURE.md (`variant=no_arch`, `stop_after=design`).
