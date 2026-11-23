"""Generate architecture/views/autose-workflow.drawio in the same visual style as architecture.drawio
(SpecBridge): dashed main-graph container, START/END, colour = kind of node, dashed purple = conditional edge.

Usage: python3 architecture/views/gen_workflow.py
"""
from pathlib import Path
from xml.sax.saxutils import quoteattr

OUT = Path(__file__).resolve().parent / "autose-workflow.drawio"

TEXT = "text;html=1;whiteSpace=wrap;align=left;verticalAlign=top;fontSize=11;"
CONTAINER = ("rounded=1;arcSize=2;whiteSpace=wrap;html=1;dashed=1;fillColor=none;verticalAlign=top;align=left;"
             "spacingLeft=12;spacingTop=6;fontSize=12;")
NODE = "rounded=1;whiteSpace=wrap;html=1;fontSize=11;arcSize=12;"
CODE = NODE + "fillColor=#d5e8d4;strokeColor=#82b366;"          # code only (no AI)
AI = NODE + "fillColor=#dae8fc;strokeColor=#6c8ebf;"            # calls a model
AGENT = NODE + "fillColor=#e1d5e7;strokeColor=#9673a6;"         # agent call (fresh gemini -p)
TOOL = NODE + "fillColor=#ffe6cc;strokeColor=#d79b00;"          # tool runner
WRITES = NODE + "fillColor=#f8cecc;strokeColor=#b85450;strokeWidth=2.5;"  # writes to GitHub
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
    arr = ""
    if pts:
        arr = '<Array as="points">' + "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in pts) + "</Array>"
    cells.append(f'<mxCell id="c{_n[0]}" edge="1" parent="1" source="{src}" target="{dst}" '
                 f'style={quoteattr(style + extra)} value={quoteattr(label)}>'
                 f'<mxGeometry relative="1" as="geometry">{arr}</mxGeometry></mxCell>')


# ------------------------------------------------------------------ header
v("<b>AutoSE workflow - GitHub Actions jobs, orchestrator and agents</b>", 30, 15, 1000, 30, TEXT + "fontSize=18;")
v("Issue in, reviewed pull request out. A trusted maintainer labels an issue <b>autose</b>; the orchestrator runs the "
  "builder agent once per stage (fresh context) and checks every stage in code; release opens the PR and waits for CI; "
  "an independent reviewer job (read-only, different model) reviews it; changes go back once. Only the red nodes write "
  "to GitHub, and a human merges. Details: architecture/decisions/ADR-001..010",
  30, 48, 1290, 40, TEXT + "fontColor=#555555;")

# ------------------------------------------------------------------ main graph
v("<b>Main graph</b> - .github/workflows/autose.yml (one job per box group; <font face='Courier New'>permissions: {}</font> "
  "by default, each job opts in; one run per issue at a time)", 220, 100, 1100, 560, CONTAINER + "strokeColor=#666666;")
trigger = v("<b>Issue #N or PR</b><br>label <i>autose</i>, comment<br><i>/autose</i> or <i>/autose review</i>",
            30, 170, 160, 70, HUMAN)
start = v("START", 240, 185, 60, 40, TERM)
gate = v("<b>gate</b> (job)<br>trusted author? which mode?<br>event read from file;<br>no secrets, no LLM",
         320, 165, 160, 80, CODE)
orch = v("<b>orchestrator.py</b> (build job)<br>state machine for stages 1-5;<br>retry caps, token budget;<br>"
         "reverts edits outside the<br>stage's folder; holds GH_TOKEN", 520, 160, 160, 100, CODE)
v("", 760, 140, 160, 70, AGENT + "opacity=45;")
v("", 750, 150, 160, 70, AGENT + "opacity=70;")
builder = v("<b>builder agent x 4 stages</b><br>gemini -p (Flash), fresh each<br>1 spec  2 design<br>3 implement  4 test",
            740, 160, 160, 70, AGENT)
checks = v("<b>stage checks</b> (code)<br>AC lint + A1 validator | design<br>refs (AST) | ruff, strict mypy |<br>"
           "AC→test coverage | pytest", 740, 285, 160, 80, CODE)
release = v("<b>release</b> (stage 5)<br>push autose/issue-N, open PR<br>(pr.md), dispatch tests.yml,<br>wait for CI",
            960, 165, 160, 80, WRITES)
reviewer = v("<b>reviewer</b> (job review-1 / review-2)<br>gemini -p (Pro), own prompt;<br>sees issue + diff + PR head;<br>"
             "runs tests; read-only token", 1150, 165, 160, 90, AI)
publish = v("<b>publish</b> (job)<br>post review.md on the PR,<br>label approved /<br>changes-requested; no LLM",
            1150, 420, 160, 80, WRITES)
final = v("<b>finalize</b> (job, always)<br>summary comment + label<br>done | needs-human | failed", 720, 425, 160, 70,
          WRITES)
human = v("<b>Human decides</b><br>merge or close the PR<br>(the bot never merges)", 520, 420, 160, 80, HUMAN)
end = v("END", 245, 440, 60, 40, TERM)

e(trigger, start)
e(start, gate)
e(gate, orch, "mode = build", COND)
e(gate, reviewer, "mode = review (seeded PRs)", COND, [(400, 128), (1230, 128)], ";exitX=0.5;exitY=0;entryX=0.5;entryY=0;")
e(gate, end, "skip: untrusted /<br>not a command", COND, [(400, 300), (275, 300)], ";exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
e(orch, builder, "prompt + only the<br>artifacts it needs", SOLID)
e(builder, checks, "artifact", SOLID)
e(checks, orch, "fail: retry / loop back<br>(4→3 ≤2, 4→2 ≤1)", BACK, [(600, 325)], ";exitX=0;exitY=0.5;entryX=0.5;entryY=1;")
e(checks, release, "stage 4 passed", COND, [(1040, 325)], ";exitX=1;exitY=0.5;entryX=0.5;entryY=1;")
e(release, reviewer, "PR #", SOLID)
e(reviewer, publish, "review.md +<br>verdict.json", SOLID)
e(publish, orch, "changes requested, round 1:<br>rework-1 (code → 3, approach → 2)", COND,
  [(930, 440), (930, 395), (640, 395)], ";exitX=0;exitY=0.25;entryX=0.75;entryY=1;")
e(publish, final, "approved, or round 2 done", COND, None, ";exitX=0;exitY=0.75;entryX=1;entryY=0.5;")
e(orch, final, "STOP: check still fails<br>after retries", BACK, [(560, 405), (800, 405)],
  ";exitX=0.25;exitY=1;entryX=0.5;entryY=0;")
e(final, human, "", SOLID)
e(human, end, "", SOLID)

# ------------------------------------------------------------------ inside one agent call
v("<b>Inside one agent call</b> - agent.py: headless Gemini CLI with a fresh context (the reviewer uses the same runner "
  "with its own policy, prompt and model)", 220, 690, 1100, 210, CONTAINER + "strokeColor=#9673a6;")
s2 = v("start", 240, 785, 50, 36, TERM)
prep = v("<b>prepare</b><br>temp HOME + turn limit; A1 skill<br>only for spec; env = PATH, HOME,<br>GEMINI_API_KEY (no GH_TOKEN)",
         320, 760, 180, 80, CODE)
model = v("<b>model</b><br>choose next tool or finish<br>(stream-json events logged)", 540, 768, 160, 70, AI)
tools = v("<b>tools</b> (admin policy file)<br>read_file, glob, grep, write_file,<br>replace, shell: uv run pytest |<br>"
          "ruff | mypy | python. Denied: web,<br>git push/commit, gh, curl", 760, 720, 200, 90, TOOL)
art = v("<b>write output</b><br>.autose-work/spec/, design.md,<br>or edits in src/ (stage 3) /<br>tests/ (stage 4)",
        760, 825, 200, 70, AI)
ret = v("<b>return to orchestrator</b><br>final text, transcript .jsonl,<br>token stats; then code reverts<br>"
        "files outside the stage folder", 1000, 790, 190, 80, AGENT)
e(s2, prep)
e(prep, model)
e(model, tools, "tool call", COND, None, ";exitX=1;exitY=0.25;entryX=0;entryY=0.5;")
e(tools, model, "result /<br>denied", SOLID, [(810, 705), (620, 705)], ";exitX=0.25;exitY=0;entryX=0.5;entryY=0;")
e(model, art, "write", COND, None, ";exitX=1;exitY=0.75;entryX=0;entryY=0.5;")
e(art, ret)
e(builder, prep, "expanded below", EXPAND, [(930, 219), (930, 268), (1130, 268), (1130, 675), (410, 675)],
  ";exitX=1;exitY=0.85;entryX=0.5;entryY=0;")
v("Limits per call: 60 turns, 1200 s, then the attempt fails (exit 53 = turn limit). Per job: 4M tokens. "
  "A call that fails before any tool use is retried once on the fallback model.",
  1000, 712, 300, 60, TEXT + "fontSize=10;fontColor=#555555;")

# ------------------------------------------------------------------ side panels
v("<b>State</b><br><b>out/state.json</b> (written by the orchestrator after every step): issue, variant, models; "
  "stages{status, attempts, notes} for spec, design, implement, test, release; acs (AC id → text); base commit; "
  "branch; pr; ci; tokens; events[]<br><br><b>Between jobs</b>: workflow artifacts <i>build</i>, <i>review-1</i>, "
  "<i>rework-1</i>, <i>review-2</i> (the reviewer job never downloads <i>build</i>)<br><br><b>Between runs</b>: "
  "a new trigger starts fresh from main; the PR branch is force-pushed. The issue gets a summary comment "
  "with an &lt;!-- autose-state --&gt; marker.", 1380, 88, 340, 250, WHITE)
v("<b>Context per agent</b><br>1 spec: issue (in untrusted tags) + A1 skill<br>2 design: SRS + ARCHITECTURE.md + repo<br>"
  "3 implement: design + AC list (+ failing test output / review findings on loop-back)<br>"
  "4 test: AC list + src diff (no design rationale)<br>review: issue + PR diff + PR-head checkout only; never spec, "
  "design, test report or transcripts<br><br><b>Agents per issue</b><br>4 builder calls per pass (+ retries), "
  "1 reviewer call per round, max 2 review rounds. Stages run one after another; each call starts with an empty "
  "context.", 1380, 350, 340, 230, WHITE)
v("<b>Legend</b>", 1340, 600, 340, 25, TEXT)
v("code only (no AI)", 1350, 628, 160, 26, CODE)
v("calls a model (AI)", 1520, 628, 160, 26, AI)
v("agent call (fresh gemini -p)", 1350, 662, 160, 26, AGENT)
v("tool runner (policy-gated)", 1520, 662, 160, 26, TOOL)
v("writes to GitHub", 1350, 696, 160, 26, WRITES)
v("trigger / human", 1520, 696, 160, 26, HUMAN)
v("solid arrow = normal edge<br><font color='#7F00FF'>dashed purple = conditional edge</font><br>"
  "<font color='#b85450'>dashed red = loop-back / stop</font><br>"
  "<font color='#777777'>dotted grey = 'expanded below'</font><br>Limits: retries per stage, 2 review rounds, "
  "60 turns per call, 4M tokens per job; hitting one stops the run with the reason in the stage's artifact.",
  1350, 730, 330, 110, TEXT)

# ------------------------------------------------------------------ external systems
v("<b>Gemini API</b> (secret GEMINI_API_KEY)<br>builder: gemini-3-flash-preview<br>reviewer: gemini-3-pro-preview<br>"
  "fallbacks: 2.5-flash / 2.5-pro<br><i>used by: builder agents, reviewer</i>", 220, 930, 280, 120, GREY)
v("<b>GitHub fork</b> QasimANaik/mistune @ f7ec702<br>issues, branch autose/issue-N, PR, reviews, labels;<br>"
  "main protected (ruleset + CODEOWNERS)<br><i>used by: gate, release, publish, finalize (gh CLI)</i>",
  520, 930, 290, 120, GREY)
v("<b>GitHub Actions</b><br>tests.yml CI (ruff, mypy, docs, pytest), dispatched by release; workflow artifacts<br>"
  "<i>used by: release (CI), all jobs (artifacts)</i>", 830, 930, 240, 120, GREY)
v("<b>Reused inputs</b><br>A1 skill requirements-spec (+ its validator)<br>A2 ARCHITECTURE.md<br>"
  "<i>used by: spec agent + spec check, design agent</i>", 1090, 930, 230, 120, GREY)
v("<b>Run records</b><br>out/: spec.md, design.md, diff.patch, test_report.md, pr.md, review.md, verdict.json, "
  "transcripts/, usage/ (tokens)<br>copied to results/ in the submission repo", 1340, 930, 340, 120, GREY)

OUT.write_text(
    '<mxfile host="app.diagrams.net">\n  <diagram id="autose-workflow" name="AutoSE workflow (Actions jobs, orchestrator, agents)">\n'
    '    <mxGraphModel dx="1245" dy="586" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" '
    'page="1" pageScale="1" pageWidth="1720" pageHeight="1080" math="0" shadow="0">\n      <root>\n'
    '        <mxCell id="0" />\n        <mxCell id="1" parent="0" />\n        '
    + "\n        ".join(cells) + "\n      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n"
)
print(f"wrote {OUT} ({len(cells)} cells)")
