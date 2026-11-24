# AutoSE: issue in, reviewed pull request out

Assignment 3, Automated Software Engineering. Roll no. 2025201064.

A GitHub Actions workflow in which LangGraph-orchestrated agents turn a labelled issue into a tested pull request,
which an independent reviewer agent then reviews. A human always makes the merge decision.

| | |
|---|---|
| **Fork (target repository)** | <https://github.com/QasimANaik/mistune> (public) |
| **Pinned upstream commit** | `lepture/mistune` @ `f7ec702edfc1ad5579a76f881238841af266d93c` |
| **Workflow on the fork** | [`.github/workflows/autose.yml`](https://github.com/QasimANaik/mistune/blob/main/.github/workflows/autose.yml) + [`autose/`](https://github.com/QasimANaik/mistune/tree/main/autose) (copy in [`workflow/`](workflow/)) |
| **Report** | [`report.pdf`](report.pdf) (source: [`report/report.html`](report/report.html)) |
| **Demo video** | TODO: add the link to the demo video (YouTube unlisted / Google Drive) |
| **All runs, PRs and reviews** | [`results/runs.md`](results/runs.md), [`results/results.csv`](results/results.csv) |

## Models and runtime

| Role | Model |
|---|---|
| Every agent node: spec (`understand`), `design`, `implement`, test workers, e2e worker, `reviewer` | **`gemini-3.5-flash-lite`** |
| Fallback (used once if a call fails before doing any work) | `gemini-3.1-flash-lite` |

- Agents run as headless **Gemini CLI 0.70.0** calls (`gemini -p`), each with a fresh context, a per-role tool policy file
  and no GitHub token.
- Orchestration is a **LangGraph 1.2.20** `StateGraph` with SQLite checkpoints.
- Model history: Flash builder + Pro reviewer (ADR-006) was superseded by one Lite model for every node (ADR-014),
  after a 429, a retired model and the price list.
- The API key is the repository secret `GEMINI_API_KEY`. It is never in code, logs or prompts.

## How to trigger the workflow

Only users with `author_association` OWNER, MEMBER or COLLABORATOR can start a run. Comments from bots and comments
that are not commands are ignored.

| What | How |
|---|---|
| Issue → spec → design → code → tests → PR → review | add the label **`autose`** to an issue, or comment **`/autose`** on it |
| Review an existing PR (seeded PRs) | comment **`/autose review`** on the PR |
| Decision-experiment variant | `/autose review variant=weak_reviewer` on a PR (E1), or `gh workflow run autose.yml -R QasimANaik/mistune -f issue=N -f variant=no_arch -f stop_after=design` (E2) |
| Re-run after a crash | "Re-run failed jobs" on the Actions run. It resumes from the last LangGraph checkpoint |

A run posts "run started" on the issue. The jobs are gate → build → review-1 → publish-1 → (rework-1 → review-2 →
publish-2) → finalize. Finalize posts a summary (stage table, stop reason, tokens) and labels the issue `autose:done`,
`autose:needs-human` or `autose:failed`. The bot never merges. The `protect-main` ruleset and CODEOWNERS require a human
code-owner approval.

## Results so far (details in the report and `results/`)

- **Issues:** bot PRs for all five issues (#1, #2, #3, #4, #18). **Hidden acceptance tests: 20/20 pass** on those branches
  (5/20 on the original code). Four PRs were approved by the reviewer. #18 stopped at release on a PyPy-only CI failure
  of a generated timing/tooling test.
- **Seeded PRs (reviewer check):** the baseline reviewer gave the expected verdict on **5/5**. It found the incomplete fix,
  the `javascript:` sanitisation bypass, the tests that assert nothing, and the wrong-layer fix (route = approach), and it
  approved the clean PR. The weak-reviewer arm of E1 could not run: Gemini prepayment credits were depleted.
- **Tokens and cost:** 27 workflow runs, 114 agent calls, **44.0M input tokens (79% cached) and 264k output tokens**, about
  **$4.73** in total. A successful issue costs $0.21–$0.39 and takes 8–10 minutes.

## Spending limit

The Gemini API key uses **prepaid credits**, which act as a hard spending cap. When the credits ran out, the review
jobs stopped with the provider's error ("prepayment credits are depleted", runs 45445763935–45445790671) instead of
spending more. The workflow also caps each job at 8M tokens and each agent call at 30 turns and 1200 s.
TODO (author): note the prepaid amount and add a screenshot of the billing page to the report appendix.

## Repository layout

```
README.md            this file
report.pdf           the report (≤ 8 pages + appendices); source in report/ (with the original PLAN.md)
architecture/
  views/             component view, sequence view (real run), stage map: .drawio + .svg/.md; generators in views/src/
  decisions/         ADR-001.md … ADR-016.md (Nygard format); superseded ADRs kept and marked
workflow/            copy of the fork's .github/workflows/ and autose/ (agent code, prompts, policies, A1 skill)
experiment/
  issues/            the 5 issue texts (issue-1, -2, -3, -4, -18); replaced/issue-5 (closed, replaced by #18)
  hidden_tests/      2-4 hidden acceptance tests per issue (never pushed to the fork)
  seeded_prs/        the 5 reviewer-check PRs: diffs (*.patch) + ground truth (labels.csv)
  variants.md        what each decision-experiment variant changes
  scripts/           eval_hidden.sh (hidden tests on any branch), sim/ (local replays of the graph with a faked model)
results/
  results.csv        one row per workflow run
  runs.md            links to every Actions run, PR and review
  hidden/            hidden-test outputs per issue and branch
  artifacts/         downloaded run artifacts (state, checkpoints, prompts, transcripts, usage)
```

## Reproduce

```bash
# hidden tests of issue N against the bot's branch (needs a clone of the fork in ./fork with `uv sync --group test`)
experiment/scripts/eval_hidden.sh autose/issue-4 4
# regenerate the draw.io views
python3 architecture/views/src/gen_architecture.py && python3 architecture/views/src/gen_views.py
# rebuild the report PDF
google-chrome --headless=new --no-pdf-header-footer --print-to-pdf=report.pdf "file://$PWD/report/report.html"
```

## Use of AI

This project was built with substantial help from an AI coding assistant (**Claude Code**, Anthropic). It wrote most of
the workflow code (`autose/`, `autose.yml`), the prompts and policies, the draw.io generators, the local simulations,
the seeded-PR changes and the first drafts of the ADRs and the report. All generated material was reviewed by the
author. As the course policy requires, the **reasoning in the ADRs** ("Rationale" sections) and the report sections marked
"✎ draft reasoning" are written by the author in their own words.
