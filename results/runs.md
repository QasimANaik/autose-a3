# Runs

Every AutoSE workflow run on the fork, in order. Costs use Gemini Standard paid-tier prices
(per 1M tokens, in / cached / out): gemini-3-flash-preview $0.50 / $0.05 / $3.00,
gemini-3.5-flash-lite $0.30 / $0.03 / $2.50 (aistudio.google.com/docs/pricing, 2026-11-24).
Token counts come from each agent call's `usage/*.json` (Gemini CLI stream-json stats).

| # | Run | Issue | Builder model | Outcome | Stopped at | Agent calls | Tokens in (cached) / out | Cost | What it showed → change |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [45234284925](https://github.com/QasimANaik/mistune/actions/runs/45234284925) | #5 | – | skipped | – | 0 | – | $0 | a normal comment, not `/autose`: gate correctly did nothing |
| 2 | [45234300084](https://github.com/QasimANaik/mistune/actions/runs/45234300084) | #5 | gemini-3-flash-preview | cancelled | build | – | – | – | cancelled by hand |
| 3 | [45236521564](https://github.com/QasimANaik/mistune/actions/runs/45236521564) | #5 | gemini-3-flash-preview | needs_clarification (wrong) | spec | 4 (all failed) | 0 | $0 | 429 free-tier limit + retired fallback; outage was scored as a spec failure → **PR #7**: model outage = stop with the provider's reason |
| 4 | [45347324270](https://github.com/QasimANaik/mistune/actions/runs/45347324270) | #5 | gemini-3-flash-preview | failed | implement | 10 | 4.16M (81%) / 31k | $0.66 | over-broad change broke 12 existing tests; implementer's test edits reverted; stage-3 ruff covered worker test files; 4M token cap → **PR #7**: ruff scope, existing-test feedback, 8M cap |
| 5 | [45350365755](https://github.com/QasimANaik/mistune/actions/runs/45350365755) | #4 | gemini-3.5-flash-lite | cancelled | spec | – | – | – | cancelled by hand |
| 6 | [45351202045](https://github.com/QasimANaik/mistune/actions/runs/45351202045) | #4 | gemini-3.5-flash-lite | failed | test | 11 | 3.63M (77%) / 19k | $0.38 | correct code (4/4 hidden), wrong AC tested literally, loops could only blame the code → **PR #9**: `loop_dispute` |
| 7 | [45353435408](https://github.com/QasimANaik/mistune/actions/runs/45353435408) | #4 | gemini-3.5-flash-lite | failed | design | 3 | 0.80M (82%) / 7k | $0.08 | design-check parser rejected `(new)` inside backticks → **PR #10** |
| 8 | [45354704591](https://github.com/QasimANaik/mistune/actions/runs/45354704591) | #4 | gemini-3.5-flash-lite | **PR opened, approved** | – | 8 | 2.00M (79%) / 15k | $0.21 | all stages first time; [PR #11](https://github.com/QasimANaik/mistune/pull/11), [CI](https://github.com/QasimANaik/mistune/actions/runs/45355186100) green; reviewer approved; hidden tests 4/4 |
| 9 | [45379575388](https://github.com/QasimANaik/mistune/actions/runs/45379575388) | #1 | gemini-3.5-flash-lite | failed | test | 10 | 5.51M (82%) / 50k | $0.55 | correct code (agent diff passes 4/4 hidden tests) but issue #1 changes behaviour pinned by 8 EXISTING upstream fixture tests (`tests/fixtures/table.txt`, "Invalid Table"); the implementer may not edit tests → loops until stop → **PR #14**: declared existing-test updates |

**Totals so far:** 46 agent calls, 16.09M input tokens (12.91M cached) and 121k output tokens, about **$1.88**.

Workflow fixes merged between runs: [PR #7](https://github.com/QasimANaik/mistune/pull/7), [#8](https://github.com/QasimANaik/mistune/pull/8), [#9](https://github.com/QasimANaik/mistune/pull/9), [#10](https://github.com/QasimANaik/mistune/pull/10), [#12](https://github.com/QasimANaik/mistune/pull/12) (token savings, before run 9); [#14](https://github.com/QasimANaik/mistune/pull/14) (declared existing-test updates, after run 9).
Artifacts of runs 7 and 8 are copied to `results/artifacts/` (GitHub keeps them 90 days).

## Still to run
- Issue #1 again after PRs #14/#15; issue #2; **issue #18** (vague, replaces #5 which was closed as not planned).
- 5 seeded PRs for the reviewer (`/autose review`), baseline and `weak_reviewer` (experiment E1).
- Experiment E2: design stage with vs without ARCHITECTURE.md (`variant=no_arch`, `stop_after=design`).
