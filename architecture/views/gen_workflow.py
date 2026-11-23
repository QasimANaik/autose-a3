"""Generate architecture/views/autose-workflow.drawio in the visual style of architecture.drawio (SpecBridge).

It draws the LangGraph implementation in the fork (autose/graph.py, nodes.py, workers.py, review.py, run.py).
Usage: python3 architecture/views/gen_workflow.py
"""
from pathlib import Path
from xml.sax.saxutils import quoteattr

OUT = Path(__file__).resolve().parent / "autose-workflow.drawio"

TEXT = "text;html=1;whiteSpace=wrap;align=left;verticalAlign=top;fontSize=11;"
CONTAINER = ("rounded=1;arcSize=2;whiteSpace=wrap;html=1;dashed=1;fillColor=none;verticalAlign=top;align=left;"
             "spacingLeft=12;spacingTop=6;fontSize=12;")
NODE = "rounded=1;whiteSpace=wrap;html=1;fontSize=11;arcSize=12;"
CODE = NODE + "fillColor=#d5e8d4;strokeColor=#82b366;"
AI = NODE + "fillColor=#dae8fc;strokeColor=#6c8ebf;"
SUB = NODE + "fillColor=#e1d5e7;strokeColor=#9673a6;"
TOOL = NODE + "fillColor=#ffe6cc;strokeColor=#d79b00;"
WRITES = NODE + "fillColor=#f8cecc;strokeColor=#b85450;strokeWidth=2.5;"
HUMAN = "rounded=1;whiteSpace=wrap;html=1;fontSize=11;fillColor=#fff2cc;strokeColor=#d6b656;"
TERM = "ellipse;whiteSpace=wrap;html=1;fillColor=#1a1a1a;fontColor=#ffffff;strokeColor=#1a1a1a;fontStyle=1;fontSize=10;"
PANEL = "rounded=0;whiteSpace=wrap;html=1;fontSize=11;align=left;verticalAlign=top;spacingLeft=8;spacingTop=4;"
WHITE = PANEL + "fillColor=#ffffff;strokeColor=#666666;"
GREY = PANEL + "fillColor=#f5f5f5;strokeColor=#666666;"
E = ("edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=block;endFill=1;strokeWidth=1.5;"
     "labelBackgroundColor=#ffffff;fontSize=11;")
SOLID = E + "strokeColor=#333333;"
COND = E + "dashed=1;strokeColor=#7F00FF;fontColor=#7F00FF;"
BACK = E + "dashed=1;strokeColor=#b85450;fontColor=#b85450;"
EXPAND = E + "strokeColor=#999999;fontColor=#777777;dashed=1;dashPattern=2 3;"

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


# ------------------------------------------------------------------ header
v("<b>AutoSE agent - LangGraph orchestrator, parallel test workers and an independent review graph</b>",
  30, 15, 1200, 30, TEXT + "fontSize=18;")
v("Issue in, reviewed pull request out. The main graph writes the spec and design, implements, then the orchestrator "
  "splits the acceptance criteria and independent <b>test workers</b> (subgraphs, each in its own git worktree) write "
  "tests in parallel; merge runs the full suite; release opens the PR. A separate <b>review graph</b> in its own "
  "read-only job reviews it; changes send the main graph round again once. Only the red nodes write to GitHub; a "
  "human merges. Code: autose/graph.py, nodes.py, workers.py, review.py, run.py", 30, 48, 1290, 40,
  TEXT + "fontColor=#555555;")

# ------------------------------------------------------------------ trigger + gate (left)
trigger = v("<b>Issue #N or PR</b><br>label <i>autose</i>, comment<br><i>/autose</i>, <i>/autose review</i>",
            30, 170, 160, 70, HUMAN)
gate = v("<b>gate</b> (job, no LLM)<br>trusted author? mode<br>build | review | skip;<br>no secrets", 30, 280, 160, 80, CODE)

# ------------------------------------------------------------------ main graph
v("<b>Main graph</b> - LangGraph StateGraph (AutoSEState, SqliteSaver checkpoint after every node) - "
  "runs in job <i>build</i> and again in <i>rework-1</i>", 220, 100, 1100, 560, CONTAINER + "strokeColor=#666666;")
start = v("START", 240, 185, 60, 40, TERM)
intake = v("<b>intake</b><br>fetch issue, flag injection<br>text; branch; repo setup", 320, 170, 160, 70, CODE)
underst = v("<b>understand</b> (stage 1)<br>spec + A1 skill →<br>spec.md; AC lint", 520, 170, 160, 70, AI)
clarify = v("<b>clarify</b><br>ACs not testable:<br>questions, no code", 520, 290, 160, 60, CODE)
design = v("<b>design</b> (stage 2)<br>+ ARCHITECTURE.md →<br>design.md; refs via AST", 720, 170, 160, 70, AI)
impl = v("<b>implement</b> (stage 3)<br>edits src/ only →<br>diff.patch; ruff, mypy", 920, 170, 160, 70, AI)
orch = v("<b>orchestrator</b><br>group ACs (max 4); split<br>token budget (20% reserve);<br>Send workers", 1130, 160,
         170, 90, CODE)
v("", 1110, 290, 170, 70, SUB + "opacity=45;")
v("", 1120, 300, 170, 70, SUB + "opacity=70;")
worker = v("<b>criterion_worker x N</b><br>(subgraph, parallel,<br>own worktree) tests for<br>its ACs only",
           1130, 310, 170, 70, SUB)
e2e = v("<b>e2e_worker</b> (subgraph)<br>regression tests across<br>criteria (only if 2+ groups)", 1130, 410, 170, 60, SUB)
merge = v("<b>merge</b> (stage 4)<br>write test files, commit;<br>full pytest + AC coverage<br>→ test_report.md",
          920, 420, 170, 80, CODE)
release = v("<b>release</b> (stage 5)<br>push branch, open PR (pr.md),<br>dispatch tests.yml, wait CI",
            700, 420, 180, 80, WRITES)
stop = v("<b>stop</b><br>reason into the stage's<br>artifact; status failed", 320, 560, 160, 60, CODE)
end = v("END", 245, 440, 60, 40, TERM)
v("stop is reached from design, implement, merge or release when retries run out, and from any node when the "
  "token budget is spent.", 500, 575, 400, 40, TEXT + "fontSize=10;fontColor=#555555;")

e(trigger, gate)
e(gate, start, "mode=build", COND, [(210, 320), (210, 205)], ";exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
e(start, intake)
e(intake, underst)
e(underst, underst, "retry ≤1", BACK, [(640, 150), (560, 150)], ";exitX=0.75;exitY=0;entryX=0.25;entryY=0;")
e(underst, design, "testable", COND)
e(underst, clarify, "not testable", COND)
e(clarify, end, "", SOLID, [(450, 320), (450, 400), (275, 400)], ";exitX=0;exitY=0.5;entryX=0.5;entryY=0;")
e(design, design, "retry ≤1", BACK, [(840, 150), (760, 150)], ";exitX=0.75;exitY=0;entryX=0.25;entryY=0;")
e(design, impl, "files + functions exist", COND)
e(impl, impl, "retry ≤2", BACK, [(1040, 150), (960, 150)], ";exitX=0.75;exitY=0;entryX=0.25;entryY=0;")
e(impl, orch, "builds; tests needed", COND)
e(impl, merge, "builds; tests exist", COND, [(960, 420)], ";exitX=0.25;exitY=1;entryX=0.25;entryY=0;")
e(orch, worker, "Send x N", COND)
e(orch, e2e, "Send", COND, [(1110, 230), (1100, 230), (1100, 440)], ";exitX=0;exitY=0.75;entryX=0;entryY=0.5;")
e(worker, merge, "WorkerResult", SOLID, [(1215, 395), (1060, 395)], ";exitX=0.5;exitY=1;entryX=0.75;entryY=0;")
e(e2e, merge, "WorkerResult", SOLID, None, ";exitX=0;exitY=0.75;entryX=1;entryY=0.5;")
e(merge, orch, "AC without a test:<br>re-send weak criteria only (once)", BACK, [(1100, 490), (1312, 490), (1312, 205)],
  ";exitX=1;exitY=0.85;entryX=1;entryY=0.5;")
e(merge, impl, "tests fail (≤2)", BACK, [(1040, 300)], ";exitX=0.75;exitY=0;entryX=0.75;entryY=1;")
e(merge, design, "still failing:<br>redesign (≤1)", BACK, [(940, 380), (840, 380)], ";exitX=0.1;exitY=0;entryX=0.75;entryY=1;")
e(merge, release, "suite green,<br>every AC tested", COND)
e(release, end, "PR open, CI green", COND, [(560, 460)], ";exitX=0;exitY=0.5;entryX=1;entryY=0.5;")
e(release, impl, "CI fails (once)", BACK, [(740, 270), (940, 270)], ";exitX=0.2;exitY=0;entryX=0.15;entryY=1;")
e(stop, end, "", SOLID, [(275, 590)], ";exitX=0;exitY=0.5;entryX=0.5;entryY=1;")

# ------------------------------------------------------------------ inside one test worker
v("<b>Review graph</b> - separate job <i>review-1</i> / <i>review-2</i>: read-only token, reviewer model "
  "gemini-3-pro-preview, own prompt, own checkpointer; never downloads the build artifacts",
  220, 690, 1100, 200, CONTAINER + "strokeColor=#b85450;")
rs = v("start", 240, 777, 50, 36, TERM)
rin = v("<b>intake_pr</b><br>linked issue + gh pr diff<br>+ PR-head checkout only", 320, 760, 160, 70, CODE)
rev = v("<b>reviewer</b><br>adversarial checklist; runs<br>tests + probes; evidence<br>for every finding", 540, 755,
        170, 80, AI)
judge = v("<b>judge</b> (code)<br>drop findings without<br>evidence; fix inconsistent<br>verdicts", 770, 755, 170, 80,
          CODE)
render = v("<b>render</b><br>review.md + verdict.json<br>(verdict, route)", 1000, 760, 160, 70, CODE)
rend = v("end", 1200, 777, 50, 36, TERM)
e(rs, rin)
e(rin, rev)
e(rev, judge)
e(judge, rev, "no valid verdict / approve<br>without listing checks (once)", BACK, [(855, 730), (625, 730)],
  ";exitX=0.5;exitY=0;entryX=0.5;entryY=0;")
e(judge, render, "valid")
e(render, rend)
e(release, rs, "PR # → job review-1", SOLID, [(790, 640), (265, 640)], ";exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
e(gate, rs, "mode=review<br>(seeded PRs)", COND, [(110, 795)], ";exitX=0.5;exitY=1;entryX=0;entryY=0.5;")

# ------------------------------------------------------------------ jobs after the review
publish = v("<b>publish</b> (job, no LLM)<br>post review.md on the PR;<br>label approved /<br>changes-requested",
            320, 920, 180, 80, WRITES)
final = v("<b>finalize</b> (job, always)<br>summary comment + label<br>done | needs-human | failed", 720, 920, 180, 80,
          WRITES)
human = v("<b>Human decides</b><br>merge or close the PR<br>(the bot never merges)", 1000, 920, 180, 80, HUMAN)
e(rend, publish, "verdict.json", SOLID, [(1225, 900), (410, 900)], ";exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
e(publish, intake, "changes requested, round 1 → job rework-1:<br>main graph again, mode=rework "
  "(route code → implement,<br>approach → design); then review-2", COND, [(200, 960), (200, 228), (300, 228)],
  ";exitX=0;exitY=0.5;entryX=0;entryY=0.85;")
e(publish, final, "approved, or round 2 done")
e(final, human)

# ------------------------------------------------------------------ side panels
v("<b>State</b><br><b>AutoSEState</b> (main): issue, variant, mode, round; issue_data, injection_flags; base, branch, "
  "patch (code so far); acs; stages{status, attempts, notes}; attempts, loops, feedback; need_tests; work_items[]; "
  "results[] (WorkerResult, list reducer with reset); review (route); pr, ci; status, stopped_at; tokens (sum); "
  "events[]<br><br><b>WorkerState</b> (private, per worker): item (its ACs, test file, budget), worktree, tries, "
  "check, tokens, result<br><br><b>ReviewState</b>: pr, issue, diff, head_sha, attempt, raw, verdict, tokens",
  1380, 88, 340, 260, WHITE)
v("<b>Context per agent</b><br>understand: issue (untrusted tags) + A1 skill<br>design: SRS + ARCHITECTURE.md + repo<br>"
  "implement: design + AC list (+ failures / review findings)<br>test worker: ITS ACs + src diff, its own worktree; "
  "returns only WorkerResult<br>reviewer: issue + PR diff + PR head only<br><br><b>Checkpoints and restarts</b><br>"
  "out/checkpoints.sqlite is uploaded as the build artifact. Re-running a failed build job downloads it, restores the "
  "code from <i>patch</i>, and continues at the pending node.", 1380, 360, 340, 230, WHITE)
v("<b>Legend</b>", 1340, 610, 340, 25, TEXT)
v("code only (no AI)", 1350, 638, 160, 26, CODE)
v("calls a model (AI)", 1520, 638, 160, 26, AI)
v("subagent (subgraph)", 1350, 672, 160, 26, SUB)
v("tools (policy file)", 1520, 672, 160, 26, TOOL)
v("writes to GitHub", 1350, 706, 160, 26, WRITES)
v("trigger / human", 1520, 706, 160, 26, HUMAN)
v("solid arrow = normal edge<br><font color='#7F00FF'>dashed purple = conditional edge / Send</font><br>"
  "<font color='#b85450'>dashed red = retry / loop-back</font><br>Limits: retries per stage, 2 review rounds, "
  "60 turns per agent call, 4M tokens per job, 3 workers at a time.", 1350, 740, 330, 90, TEXT)
v("<b>Every agent call</b> (agent.py): fresh headless gemini -p; temp HOME; env = PATH, HOME, GEMINI_API_KEY "
  "(no GitHub token); admin policy file: read_file, glob, grep, write_file, replace, shell uv run pytest | ruff | "
  "mypy | python. Denied: web, git push/commit, gh, curl. Files outside the stage's folder are reverted by code.",
  1340, 840, 340, 110, TOOL.replace("rounded=1", "rounded=0") + "align=left;verticalAlign=top;spacingLeft=8;")

# ------------------------------------------------------------------ external systems
v("<b>Gemini API</b> (secret GEMINI_API_KEY)<br>builder + workers: gemini-3-flash-preview<br>reviewer: "
  "gemini-3-pro-preview<br><i>used by: understand, design, implement, workers, reviewer</i>", 220, 1040, 280, 110, GREY)
v("<b>GitHub fork</b> QasimANaik/mistune @ f7ec702<br>issues, branch, PR, reviews, labels; main protected<br>"
  "<i>used by: gate, intake, release, intake_pr, publish, finalize</i>", 520, 1040, 290, 110, GREY)
v("<b>GitHub Actions</b><br>tests.yml CI (dispatched by release); artifacts carry state and checkpoints between "
  "jobs", 830, 1040, 240, 110, GREY)
v("<b>Reused inputs</b><br>A1 skill requirements-spec + its validator<br>A2 ARCHITECTURE.md", 1090, 1040, 230, 110, GREY)
v("<b>Run records</b><br>out/: spec.md, design.md, diff.patch, test_report.md, pr.md, review.md, verdict.json, "
  "state.json, checkpoints.sqlite, transcripts/, usage/", 1340, 1040, 340, 110, GREY)

OUT.write_text(
    '<mxfile host="app.diagrams.net">\n  <diagram id="autose-workflow" name="AutoSE agent (LangGraph, orchestrator + '
    'test workers + review graph)">\n    <mxGraphModel dx="1245" dy="586" grid="1" gridSize="10" guides="1" '
    'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1720" pageHeight="1180" math="0" '
    'shadow="0">\n      <root>\n        <mxCell id="0" />\n        <mxCell id="1" parent="0" />\n        '
    + "\n        ".join(cells) + "\n      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n")
print(f"wrote {OUT} ({len(cells)} cells)")
