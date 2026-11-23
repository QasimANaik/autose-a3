# workflow/

Exact copy of the agent workflow from the fork (`QasimANaik/mistune`, PR #6, branch `autose-infra`):

- `.github/workflows/autose.yml`: the GitHub Actions workflow
- `.github/CODEOWNERS`: makes a human code-owner review necessary for merging
- `autose/`: orchestrator, checks, agent runner (Gemini CLI), role policies, prompts, the A1 skill, config
