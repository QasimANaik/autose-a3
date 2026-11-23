# Local simulation of the LangGraph workflow (no API key, no GitHub)

The model and GitHub are faked; everything else is the real code (LangGraph routing, checks, git worktrees,
parallel workers, merge, SQLite checkpoints, git commits). Run with a Python that has `langgraph==1.2.20` and
`langgraph-checkpoint-sqlite==3.1.3`, against a clone of the fork whose `origin` is a local bare repo.

| Script | Path exercised | Result (2026-11-23) |
|---|---|---|
| `simulate.py <autose> <work> <out>` | intake → understand → design → implement (fails strict mypy, retried) → orchestrator → 3 parallel workers (2 criterion + e2e) → merge (1334 passed) → release | `pr_open`, 7 agent calls, injection phrases flagged |
| `simulate.py … crash` then `simulate.py …` on a fresh clone | crash inside merge, then a new runner resumes from `checkpoints.sqlite` | resumed at `merge`, code restored from `patch`, no extra agent calls; found and fixed a bug (repo excludes not re-applied on resume → `.venv` deleted) |
| `simulate_review.py <autose> <pr-checkout> <out> <review>` | review graph: reviewer approves without listing checks → judge rejects → retry → request_changes with one evidenced + one evidence-less finding; then rework (route=code) on the PR branch | evidence-less finding discarded; rework → implement → workers → merge → release (no force push) |
| `simulate_vague.py …` | spec ACs stay vague after the retry | `clarify` → `needs_clarification`, no code written |
