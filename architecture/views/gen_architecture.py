"""Generate architecture/views/architecture.drawio: the AutoSE workflow (LangGraph) with every node, what it does,
and an estimated cost per node / per run. Visual style follows the SpecBridge architecture.drawio.

Prices: Gemini API Standard paid tier, USD per 1M tokens, read from https://aistudio.google.com/docs/pricing
on 2026-11-24 (gemini-3.8-flash: $0.75 in / $0.075 cached / $3.75 out through 2026-12-31;
gemini-3.1-pro-preview: $2.00 in / $0.20 cached / $12.00 out for prompts <= 200k tokens).
Token counts are ESTIMATES (see the assumptions panel); replace them with out/usage/*.json after real runs.

Usage: python3 architecture/views/gen_architecture.py
"""
from pathlib import Path
from xml.sax.saxutils import quoteattr

OUT = Path(__file__).resolve().parent / "architecture.drawio"

# ---------------------------------------------------------------- cost model (estimates)
PRICE = {  # USD per 1M tokens: input, cached input, output (incl. thinking)
    "flash": (0.75, 0.075, 3.75),
    "pro": (2.00, 0.20, 12.00),
}
CACHE_HIT = 0.70  # share of input tokens served from Gemini's implicit cache (repeated prefix every turn)

# agent node -> (model, turns, average context tokens per turn, output tokens per turn)
CALLS = {
    "understand": ("flash", 15, 30_000, 1_500),
    "design": ("flash", 20, 40_000, 1_200),
    "implement": ("flash", 25, 50_000, 1_500),
    "worker": ("flash", 12, 30_000, 1_000),     # per test worker (criterion or e2e)
    "reviewer": ("pro", 20, 45_000, 1_500),
}


def cost(node: str) -> tuple[float, int, int]:
    model, turns, ctx, out = CALLS[node]
    tin, tout = turns * ctx, turns * out
    p_in, p_cache, p_out = PRICE[model]
    usd = (tin * (1 - CACHE_HIT) * p_in + tin * CACHE_HIT * p_cache + tout * p_out) / 1e6
    return usd, tin, tout


def tag(node: str, times: int = 1) -> str:
    usd, tin, tout = cost(node)
    extra = f" x{times} = ${usd * times:.2f}" if times > 1 else ""
    return (f"<br><font color='#0b6e4f'><b>≈ ${usd:.2f}</b>{extra} · ~{tin // 1000}k in / "
            f"{tout // 1000}k out</font>")


FREE = "<br><font color='#0b6e4f'><b>$0</b> LLM · Actions minutes free (public repo)</font>"

C = {k: cost(k)[0] for k in CALLS}
WORKERS = 3  # 2 criterion workers + 1 e2e for a typical issue
BUILD = C["understand"] + C["design"] + C["implement"] + WORKERS * C["worker"]
HAPPY = BUILD + C["reviewer"]
REWORK = C["implement"] + WORKERS * C["worker"] + C["reviewer"]
WORST = (2 * C["understand"] + 4 * C["design"] + 3 * 3 * C["implement"] + 2 * WORKERS * C["worker"]
         + 2 * C["reviewer"] + REWORK)
BUILD_TOKENS = sum(cost(k)[1] + cost(k)[2] for k in ("understand", "design", "implement")) + WORKERS * sum(cost("worker")[1:])

# ---------------------------------------------------------------- styles
TEXT = "text;html=1;whiteSpace=wrap;align=left;verticalAlign=top;fontSize=11;"
CONTAINER = ("rounded=1;arcSize=2;whiteSpace=wrap;html=1;dashed=1;fillColor=none;verticalAlign=top;align=left;"
             "spacingLeft=12;spacingTop=6;fontSize=12;")
NODE = "rounded=1;whiteSpace=wrap;html=1;fontSize=11;arcSize=10;verticalAlign=top;spacingTop=4;"
CODE = NODE + "fillColor=#d5e8d4;strokeColor=#82b366;"
AI = NODE + "fillColor=#dae8fc;strokeColor=#6c8ebf;"
SUB = NODE + "fillColor=#e1d5e7;strokeColor=#9673a6;"
TOOL = NODE + "fillColor=#ffe6cc;strokeColor=#d79b00;"
WRITES = NODE + "fillColor=#f8cecc;strokeColor=#b85450;strokeWidth=2.5;"
HUMAN = NODE + "fillColor=#fff2cc;strokeColor=#d6b656;"
TERM = "ellipse;whiteSpace=wrap;html=1;fillColor=#1a1a1a;fontColor=#ffffff;strokeColor=#1a1a1a;fontStyle=1;fontSize=10;"
PANEL = "rounded=0;whiteSpace=wrap;html=1;fontSize=11;align=left;verticalAlign=top;spacingLeft=8;spacingTop=4;"
WHITE = PANEL + "fillColor=#ffffff;strokeColor=#666666;"
GREY = PANEL + "fillColor=#f5f5f5;strokeColor=#666666;"
COSTP = PANEL + "fillColor=#f0f8f4;strokeColor=#0b6e4f;"
E = ("edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=block;endFill=1;strokeWidth=1.5;"
     "labelBackgroundColor=#ffffff;fontSize=11;")
SOLID = E + "strokeColor=#333333;"
COND = E + "dashed=1;strokeColor=#7F00FF;fontColor=#7F00FF;"
BACK = E + "dashed=1;strokeColor=#b85450;fontColor=#b85450;"

cells: list[str] = []
_n = [1]


def v(value: str, x: int, y: int, w: int, h: int, style: str) -> str:
    _n[0] += 1
    cid = f"c{_n[0]}"
    cells.append(f'<mxCell id="{cid}" parent="1" style={quoteattr(style)} value={quoteattr(value)} vertex="1">'
                 f'<mxGeometry height="{h}" width="{w}" x="{x}" y="{y}" as="geometry"/></mxCell>')
    return cid


def e(src: str, dst: str, label: str = "", style: str = SOLID, pts: list[tuple[int, int]] | None = None,
      extra: str = "") -> None:
    _n[0] += 1
    arr = ('<Array as="points">' + "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in pts) + "</Array>") if pts else ""
    cells.append(f'<mxCell id="c{_n[0]}" edge="1" parent="1" source="{src}" target="{dst}" '
                 f'style={quoteattr(style + extra)} value={quoteattr(label)}>'
                 f'<mxGeometry relative="1" as="geometry">{arr}</mxGeometry></mxCell>')


def ex(x: float, y: float) -> str:
    return f";exitX={x};exitY={y};"


def en(x: float, y: float) -> str:
    return f"entryX={x};entryY={y};"


# ---------------------------------------------------------------- header
v("<b>AutoSE - architecture of the issue-to-PR workflow (LangGraph agents + GitHub Actions jobs), with estimated "
  "cost per node</b>", 30, 15, 1500, 30, TEXT + "fontSize=18;")
v("A trusted maintainer labels an issue <b>autose</b>. The <b>main graph</b> (job build) writes the spec and the "
  "design, implements the change, sends <b>parallel test workers</b> (one per acceptance-criterion group, each in its "
  "own git worktree), merges and runs the full suite, then opens the PR and waits for CI. The <b>review graph</b> runs "
  "in its own read-only job with a different model. Changes requested send the main graph round once more "
  "(job rework-1). Every route is decided by code; only red nodes write to GitHub; a human merges. "
  "<font color='#0b6e4f'>Green figures = estimated Gemini cost per node (paid tier, see the cost panel).</font>",
  30, 48, 1480, 50, TEXT + "fontColor=#555555;")

# ---------------------------------------------------------------- trigger + gate
trigger = v("<b>Issue #N or PR</b> (fork)<br>label <i>autose</i>, comment <i>/autose</i>, or <i>/autose review</i> "
            "on a PR", 30, 160, 170, 80, HUMAN)
gate = v("<b>gate</b> (job, no LLM)<br>reads the event file; accepts only OWNER / MEMBER / COLLABORATOR, ignores bots; "
         "mode = build | review | skip; label autose:running + 'run started' comment" + FREE, 30, 270, 170, 175, CODE)

# ---------------------------------------------------------------- main graph
v("<b>Main graph</b> - LangGraph StateGraph (AutoSEState, SQLite checkpoint after every node); job <i>build</i>, "
  "and again in job <i>rework-1</i>. Each agent node = one fresh headless <i>gemini -p</i> call (builder model "
  "gemini-3.8-flash)", 230, 100, 1270, 660, CONTAINER + "strokeColor=#666666;")
start = v("START", 250, 210, 60, 40, TERM)
intake = v("<b>intake</b> (code)<br>fetch issue via gh; flag injection-like phrases (kept as data); create branch "
           "autose/issue-N; repo setup" + FREE, 330, 170, 185, 130, CODE)
underst = v("<b>understand</b> - stage 1<br>A1 <i>requirements-spec</i> skill, batch mode → SRS / REG / VAL → "
            "<b>spec.md</b>. Check (code): every AC has an id + Given/When/Then, no vague words" + tag("understand"),
            540, 170, 190, 150, AI)
clarify = v("<b>clarify</b> (code)<br>ACs still not testable after 1 retry: write open questions, no code; status "
            "needs_clarification" + FREE, 540, 350, 190, 110, CODE)
design = v("<b>design</b> - stage 2<br>reads ARCHITECTURE.md + code → <b>design.md</b> (files and functions to "
           "change, plan, risks). Check (code): every named file / function exists (AST)" + tag("design"),
           755, 170, 190, 150, AI)
impl = v("<b>implement</b> - stage 3<br>edits <b>src/</b> only (other edits reverted) → <b>diff.patch</b>. Check "
         "(code): import, ruff, strict mypy; commit" + tag("implement"), 970, 170, 190, 150, AI)
orch = v("<b>orchestrator</b> (code) - stage 4<br>group ACs per requirement (max 4 groups); token budget split with "
         "20% reserve; <i>Send</i> one worker per group (+ e2e if 2+ groups)" + FREE, 1290, 160, 190, 150, CODE)
v("", 1270, 335, 190, 135, SUB + "opacity=45;")
v("", 1280, 345, 190, 135, SUB + "opacity=70;")
worker = v("<b>criterion_worker x N</b> (subgraph)<br>own git worktree; writes ONE test file for ITS ACs; runs it; "
           "1 retry if an AC is uncovered; returns WorkerResult" + tag("worker", 2), 1290, 355, 190, 135, SUB)
e2e = v("<b>e2e_worker</b> (subgraph)<br>regression + cross-criteria tests in one file (only with 2+ groups)"
        + tag("worker"), 1290, 515, 190, 115, SUB)
merge = v("<b>merge</b> (code) - stage 4<br>write the workers' files, commit; full pytest + AC→test coverage → "
          "<b>test_report.md</b>; stops on a model outage" + FREE, 1050, 500, 190, 140, CODE)
release = v("<b>release</b> (code) - stage 5<br>push branch, open PR (<b>pr.md</b>), dispatch tests.yml, wait; "
            "re-run failed CI jobs once (flaky timing tests)" + FREE, 820, 500, 195, 140, WRITES)
stop = v("<b>stop</b> (code)<br>append 'why this stage stopped' to the stage's artifact; status failed" + FREE,
         330, 610, 185, 110, CODE)
end = v("END", 255, 545, 60, 40, TERM)
v("<i>stop</i> is reached from design, implement, merge or release when their retries run out, from any agent node "
  "when the model is unavailable (quota / retired model), and when the 8M-token job budget is spent.",
  540, 660, 460, 60, TEXT + "fontSize=10;fontColor=#555555;")

e(trigger, gate)
e(gate, start, "mode=build", COND, [(215, 357), (215, 230)], ex(1, 0.5) + en(0, 0.5))
e(start, intake)
e(intake, underst)
e(underst, underst, "retry ≤1", BACK, [(690, 140), (580, 140)], ex(0.75, 0) + en(0.25, 0))
e(underst, design, "testable", COND)
e(underst, clarify, "not testable", COND)
e(clarify, end, "", SOLID, [(285, 405)], ex(0, 0.5) + en(0.5, 0))
e(design, design, "retry ≤1", BACK, [(905, 140), (795, 140)], ex(0.75, 0) + en(0.25, 0))
e(design, impl, "refs exist", COND)
e(impl, impl, "retry ≤2", BACK, [(1120, 140), (1010, 140)], ex(0.75, 0) + en(0.25, 0))
e(impl, orch, "builds; tests needed", COND)
e(impl, merge, "builds; tests exist", COND, [(1015, 470), (1100, 470)], ex(0.25, 1) + en(0.25, 0))
e(orch, worker, "Send x N", COND)
e(orch, e2e, "Send", COND, [(1255, 280), (1255, 572)], ex(0, 0.8) + en(0, 0.5))
e(worker, merge, "WorkerResult", SOLID, [(1385, 495), (1200, 495)], ex(0.5, 1) + en(0.8, 0))
e(e2e, merge, "WorkerResult", SOLID, None, ex(0, 0.8) + en(1, 0.5))
e(merge, orch, "AC without a test:<br>re-send weak criteria only (once)", BACK,
  [(1145, 700), (1492, 700), (1492, 235)], ex(0.5, 1) + en(1, 0.5))
e(merge, impl, "tests fail (≤2)", BACK, [(1190, 335)], ex(0.75, 0) + en(0.85, 1))
e(merge, design, "still failing:<br>redesign (≤1)", BACK, [(1070, 450), (900, 450)], ex(0.1, 0) + en(0.75, 1))
e(merge, release, "suite green,<br>every AC tested", COND)
e(release, end, "PR open, CI green", COND, [(720, 565)], ex(0, 0.45) + en(1, 0.5))
e(release, impl, "CI fails (once)", BACK, [(850, 345), (1000, 345)], ex(0.15, 0) + en(0.15, 1))
e(stop, end, "", SOLID, [(285, 665)], ex(0, 0.5) + en(0.5, 1))

# ---------------------------------------------------------------- review graph
v("<b>Review graph</b> - separate jobs <i>review-1</i> / <i>review-2</i>: read-only token, reviewer model "
  "<b>gemini-3.1-pro-preview</b>, own prompt and checkpointer; sees ONLY the issue, the PR diff and the PR-head "
  "checkout; never downloads the build artifacts", 230, 790, 1270, 230, CONTAINER + "strokeColor=#b85450;")
rs = v("start", 250, 890, 50, 36, TERM)
rin = v("<b>intake_pr</b> (code)<br>linked issue (Fixes #N) + gh pr diff; PR body and builder artifacts are NOT "
        "passed" + FREE, 330, 860, 190, 120, CODE)
rev = v("<b>reviewer</b> - stage 6<br>adversarial checklist: reproduce the issue's examples, run pytest, look for "
        "regressions, XSS, empty tests; every finding needs evidence; verdict JSON" + tag("reviewer"),
        555, 845, 220, 150, AI)
judge = v("<b>judge</b> (code)<br>drop findings without evidence; approve + blocker → request changes; approve "
          "without listing checks → ask again once" + FREE, 810, 855, 200, 130, CODE)
render = v("<b>render</b> (code)<br>review.md + verdict.json (verdict, route code | approach)" + FREE,
           1045, 865, 190, 110, CODE)
rend = v("end", 1290, 890, 50, 36, TERM)
e(rs, rin)
e(rin, rev)
e(rev, judge)
e(judge, rev, "no valid verdict (once)", BACK, [(910, 830), (665, 830)], ex(0.5, 0) + en(0.5, 0))
e(judge, render, "valid")
e(render, rend)
e(release, rs, "PR # → job review-1", SOLID, [(917, 770), (275, 770)], ex(0.5, 1) + en(0.5, 0))
e(gate, rs, "mode=review<br>(seeded PRs)", COND, [(115, 908)], ex(0.5, 1) + en(0, 0.5))

# ---------------------------------------------------------------- jobs after the review
publish = v("<b>publish</b> (job, no LLM)<br>post review.md on the PR; label approved / changes-requested; outputs "
            "verdict + route" + FREE, 330, 1060, 210, 120, WRITES)
final = v("<b>finalize</b> (job, always)<br>summary comment with stage table, stop reason and tokens; label done | "
          "needs-human | failed" + FREE, 760, 1060, 210, 120, WRITES)
human = v("<b>Human decides</b><br>merge or close the PR. The bot never merges; CODEOWNERS makes a bot approval "
          "useless for merging", 1040, 1060, 210, 120, HUMAN)
e(rend, publish, "verdict.json", SOLID, [(1315, 1040), (435, 1040)], ex(0.5, 1) + en(0.5, 0))
e(publish, intake, "changes requested, round 1 → job rework-1: main graph again (route code → implement, "
  "approach → design), then review-2" + f"<br><font color='#0b6e4f'>≈ ${REWORK:.2f} per rework round</font>",
  COND, [(215, 1120), (215, 285), (320, 285)], ex(0, 0.5) + en(0, 0.9))
e(publish, final, "approved, or round 2 done")
e(final, human)

# ---------------------------------------------------------------- cost panel
rows = "".join(
    f"<tr><td>{name}</td><td>{CALLS[k][0]}</td><td align='right'>{CALLS[k][1]}</td>"
    f"<td align='right'>{cost(k)[1] // 1000}k / {cost(k)[2] // 1000}k</td><td align='right'><b>${cost(k)[0]:.2f}</b></td></tr>"
    for name, k in (("understand", "understand"), ("design", "design"), ("implement", "implement"),
                    ("test worker (each)", "worker"), ("reviewer (per round)", "reviewer")))
v("<b>Estimated cost</b> (Gemini API, Standard paid tier)<br>"
  "<table border='1' cellpadding='2' style='border-collapse:collapse;font-size:10px'>"
  "<tr><th>agent node</th><th>model</th><th>turns</th><th>tokens in / out</th><th>USD</th></tr>" + rows + "</table>"
  f"<br><b>Per issue run</b><br>"
  f"• build job (spec + design + implement + {WORKERS} workers): <b>${BUILD:.2f}</b>, ~{BUILD_TOKENS / 1e6:.1f}M tokens<br>"
  f"• happy path (+ 1 review round): <b>${HAPPY:.2f}</b><br>"
  f"• with one rework round (+ implement, workers, review-2): <b>${HAPPY + REWORK:.2f}</b><br>"
  f"• worst case (every retry used): <b>≈ ${WORST:.0f}</b>, but the 8M-token cap per job stops it earlier<br>"
  f"• seeded-PR review only: <b>${C['reviewer']:.2f}</b>; weak-reviewer variant (Flash, read-only): "
  f"<b>≈ ${C['reviewer'] * (0.75 / 2.0) * 0.6:.2f}</b><br><br>"
  f"<b>Whole assignment</b> (5 issues, ~1 rework each; 5 seeded PRs x 2 reviewer variants; E2: 5 issues x 2 variants "
  f"up to design): <b>≈ ${5 * (HAPPY + REWORK) + 5 * C['reviewer'] * 1.25 + 10 * (C['understand'] + C['design']):.0f}</b>"
  f" (range about half to double).<br><br>"
  "<b>Assumptions</b>: each turn re-sends the whole context (Gemini CLI system prompt + tools ≈ 12k tokens, plus "
  f"files read so far); {int(CACHE_HIT * 100)}% of input is served from Gemini's implicit cache; output includes "
  "thinking tokens. Prices per 1M tokens (in / cached / out): gemini-3.8-flash $0.75 / $0.075 / $3.75 (until "
  "2026-12-31, then double); gemini-3.1-pro-preview $2.00 / $0.20 / $12.00 (prompts ≤ 200k). Source: "
  "aistudio.google.com/docs/pricing, 2026-11-24. GitHub Actions minutes are free for a public repo. "
  "<b>Replace these estimates with out/usage/*.json after the real runs.</b><br><br>"
  "<b>Free tier</b>: one agent call = one API request per turn, so one issue run is roughly 100-150 requests; "
  "the Flash free tier's daily request limit is far below that, and Pro has no free tier, so the runs need billing "
  "with a budget cap.",
  1540, 88, 380, 700, COSTP)

# ---------------------------------------------------------------- state / context / legend
v("<b>State</b> (checkpointed; carried between jobs as workflow artifacts)<br><b>AutoSEState</b>: issue, variant, "
  "mode; issue_data, injection_flags; base, branch, patch (code so far); acs; stages{status, attempts, notes}; "
  "attempts, loops, feedback; need_tests; work_items; results[] (reducer); review route; pr, ci; status, stopped_at, "
  "stop_reason; tokens; events<br><b>WorkerState</b> (private): its ACs, test file, worktree, tries, result<br>"
  "<b>ReviewState</b>: pr, issue, diff, head_sha, verdict, tokens<br>A re-run build job resumes at the pending node "
  "and restores the code from <i>patch</i>.", 1540, 805, 380, 215, WHITE)
v("<b>Legend</b>", 1540, 1035, 380, 22, TEXT)
v("code only (no AI)", 1540, 1060, 185, 26, CODE.replace("verticalAlign=top;spacingTop=4;", ""))
v("calls a model (AI)", 1735, 1060, 185, 26, AI.replace("verticalAlign=top;spacingTop=4;", ""))
v("subagent (subgraph)", 1540, 1092, 185, 26, SUB.replace("verticalAlign=top;spacingTop=4;", ""))
v("tools (policy file)", 1735, 1092, 185, 26, TOOL.replace("verticalAlign=top;spacingTop=4;", ""))
v("writes to GitHub", 1540, 1124, 185, 26, WRITES.replace("verticalAlign=top;spacingTop=4;", ""))
v("trigger / human", 1735, 1124, 185, 26, HUMAN.replace("verticalAlign=top;spacingTop=4;", ""))
v("solid = normal edge · <font color='#7F00FF'>dashed purple = conditional / Send</font> · "
  "<font color='#b85450'>dashed red = retry / loop-back</font>", 1540, 1156, 380, 30, TEXT)

# ---------------------------------------------------------------- agent call + external systems
v("<b>Every agent call</b> (agent.py): fresh headless <i>gemini -p</i> with an empty context; temp HOME; env = PATH, "
  "HOME, GEMINI_API_KEY only (no GitHub token); admin policy file allows read_file, glob, grep, write_file, replace, "
  "shell uv run pytest | ruff | mypy | python; denies web, git push / commit, gh, curl; 60 turns, 1200 s. A failure "
  "before any work (quota, retired model) is retried once on the fallback model, then stops the run with the reason.",
  230, 1200, 1270, 60, TOOL.replace("rounded=1", "rounded=0") + "align=left;spacingLeft=8;")
v("<b>Gemini API</b> (secret GEMINI_API_KEY)<br>builder + workers: gemini-3.8-flash<br>reviewer: "
  "gemini-3.1-pro-preview", 230, 1280, 290, 75, GREY)
v("<b>GitHub fork</b> QasimANaik/mistune @ f7ec702<br>issues, branch, PR, reviews, labels; main protected",
  540, 1280, 300, 75, GREY)
v("<b>GitHub Actions</b><br>8 jobs; tests.yml CI dispatched by release; artifacts carry checkpoints",
  860, 1280, 300, 75, GREY)
v("<b>Reused inputs</b><br>A1 skill requirements-spec + validator; A2 ARCHITECTURE.md", 1180, 1280, 320, 75, GREY)
v("<b>Run records</b> (artifacts)<br>spec.md, design.md, diff.patch, test_report.md, pr.md, review.md, "
  "verdict.json, state.json, checkpoints.sqlite, transcripts/, usage/ (tokens)", 1540, 1200, 380, 155, GREY)

OUT.write_text(
    '<mxfile host="app.diagrams.net">\n  <diagram id="autose-architecture" name="AutoSE architecture + costs">\n'
    '    <mxGraphModel dx="1245" dy="586" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
    'fold="1" page="1" pageScale="1" pageWidth="1950" pageHeight="1380" math="0" shadow="0">\n      <root>\n'
    '        <mxCell id="0" />\n        <mxCell id="1" parent="0" />\n        '
    + "\n        ".join(cells) + "\n      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n")
print(f"wrote {OUT} ({len(cells)} cells)")
for k in CALLS:
    usd, tin, tout = cost(k)
    print(f"  {k:11s} ${usd:.2f}  in {tin:,}  out {tout:,}")
print(f"  build ${BUILD:.2f} (~{BUILD_TOKENS / 1e6:.2f}M tokens) | happy ${HAPPY:.2f} | +rework ${HAPPY + REWORK:.2f} "
      f"| worst ${WORST:.2f}")
