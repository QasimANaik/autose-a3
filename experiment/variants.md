# Decision-experiment variants

Variants are entries in `autose/config.toml` (`[variants.<name>]`) and are selected with the workflow input
`variant` (or `/autose review variant=<name>` on a PR). The code is identical between arms; a variant only
overrides the keys it lists. Results go to `results/results.csv` (`variant` column).

| Experiment | ADR tested | Variant | What it changes | How to run |
|---|---|---|---|---|
| E1 reviewer independence | ADR-008 | `baseline` | reviewer runs code (`reviewer.toml` policy), adversarial checklist prompt with the evidence rule (`reviewer.md`) | `/autose review` on each seeded PR |
| | | `weak_reviewer` | read-only policy, cannot run anything (`reviewer_readonly.toml`); plain prompt (`reviewer_plain.md`). Same model as baseline (ADR-014) | `/autose review variant=weak_reviewer` on each seeded PR |
| E2 hand-offs | ADR-003 | `baseline` | design stage is told to read `ARCHITECTURE.md` | `gh workflow run autose.yml -f issue=N -f variant=baseline -f stop_after=design` |
| | | `no_arch` | `ARCHITECTURE.md` hidden from every agent (`git update-index --skip-worktree` + delete in the job's checkout; not committed) and not mentioned in the prompt | `gh workflow run autose.yml -f issue=N -f variant=no_arch -f stop_after=design` |

**Metrics.** E1: planted defects caught (of 4), false rejection of the clean seeded PR, findings dropped by the
judge, reviewer tokens. E2: design check passes on the first attempt; files named vs the files the reference
fix changes; design-stage tokens.
