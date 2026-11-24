"""Generate the stage map (+ job graph) and the sequence view of a real run as draw.io files.

Usage: python3 architecture/views/gen_views.py architecture/views
Edit the .drawio files by hand afterwards if you like; re-running this overwrites them.
"""
import sys
from xml.sax.saxutils import quoteattr

OUT = sys.argv[1] if len(sys.argv) > 1 else str(__import__("pathlib").Path(__file__).resolve().parents[1])

BLUE = "fillColor=#dae8fc;strokeColor=#6c8ebf;"
GREEN = "fillColor=#d5e8d4;strokeColor=#82b366;"
ORANGE = "fillColor=#ffe6cc;strokeColor=#d79b00;"
RED = "fillColor=#f8cecc;strokeColor=#b85450;"
PURPLE = "fillColor=#e1d5e7;strokeColor=#9673a6;"
YELLOW = "fillColor=#fff2cc;strokeColor=#d6b656;"
GREY = "fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;"
BOX = "rounded=1;whiteSpace=wrap;html=1;arcSize=8;"
LANE = "swimlane;whiteSpace=wrap;html=1;startSize=30;rounded=0;"
EDGE = "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=block;endFill=1;fontSize=11;labelBackgroundColor=#ffffff;"
DASH = EDGE + "dashed=1;"
TEXT = "text;html=1;align=left;whiteSpace=wrap;"

BUILDER_MODEL = "gemini-3.5-flash-lite"
REVIEWER_MODEL = "gemini-3.5-flash-lite"


class Page:
    def __init__(self, pid, name, w=1700, h=1200):
        self.pid, self.name, self.w, self.h = pid, name, w, h
        self.cells, self.n = [], 0

    def _id(self):
        self.n += 1
        return f"{self.pid}-{self.n}"

    def v(self, label, x, y, w, h, style=BOX + BLUE):
        cid = self._id()
        self.cells.append(
            f'<mxCell id="{cid}" value={quoteattr(label)} style={quoteattr(style)} vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        return cid

    def e(self, src, dst, label="", style=EDGE, points=None):
        cid = self._id()
        pts = ""
        if points:
            pts = '<Array as="points">' + "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in points) + "</Array>"
        self.cells.append(
            f'<mxCell id="{cid}" value={quoteattr(label)} style={quoteattr(style)} edge="1" parent="1" '
            f'source="{src}" target="{dst}"><mxGeometry relative="1" as="geometry">{pts}</mxGeometry></mxCell>')
        return cid

    def msg(self, label, x1, x2, y, style=None):
        cid = self._id()
        st = style or "html=1;verticalAlign=bottom;endArrow=block;endFill=1;fontSize=11;labelBackgroundColor=#ffffff;"
        self.cells.append(
            f'<mxCell id="{cid}" value={quoteattr(label)} style={quoteattr(st)} edge="1" parent="1">'
            f'<mxGeometry relative="1" as="geometry"><mxPoint x="{x1}" y="{y}" as="sourcePoint"/>'
            f'<mxPoint x="{x2}" y="{y}" as="targetPoint"/></mxGeometry></mxCell>')

    def xml(self):
        return (f'<diagram id="{self.pid}" name={quoteattr(self.name)}>'
                f'<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
                f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="{self.w}" pageHeight="{self.h}" math="0" shadow="0">'
                f'<root><mxCell id="0"/><mxCell id="1" parent="0"/>{"".join(self.cells)}</root></mxGraphModel></diagram>')


def save(path, pages):
    with open(path, "w") as f:
        f.write('<mxfile host="app.diagrams.net" agent="gen_views.py">' + "".join(p.xml() for p in pages) + "</mxfile>\n")


# ------------------------------------------------------------------ stage map + job graph
s = Page("stages", "Stage map", 1700, 800)
s.v("<b>Stage map</b>: 6 fixed stages, each with an artifact and a check; loop-backs owned by the orchestrator",
    20, 0, 1200, 30, TEXT + "fontSize=18;")
W, H, Y = 220, 150, 200
xs = [20, 290, 560, 830, 1100, 1370]
labels = [
    ("1 Requirements", "Builder (fresh ctx) + A1 skill", "spec.md", "every AC has id + Given/When/Then"),
    ("2 Design", "Builder (fresh ctx) + ARCHITECTURE.md", "design.md", "named files + functions exist (AST)"),
    ("3 Implement", "Builder (fresh ctx), branch autose/issue-N", "diff.patch", "uv sync, import, ruff, mypy, diff_guard"),
    ("4 Test", "Builder (fresh ctx)", "test_report.md", "pytest old + new, ≥1 test per AC id"),
    ("5 Release", "orchestrator (no LLM), gh CLI", "pr.md + PR link", "PR open + tests.yml green"),
    ("6 Review", f"Reviewer: own job, {REVIEWER_MODEL}, read-only", "review.md + verdict.json", "approve, or 2 rounds used"),
]
ids = []
for x, (t, ag, art, chk), col in zip(xs, labels, [BLUE, BLUE, BLUE, BLUE, ORANGE, RED]):
    ids.append(s.v(f"<b>{t}</b><br><i>{ag}</i><br><br>artifact: <b>{art}</b><br><font color='#006600'>check: {chk}</font>",
                   x, Y, W, H, BOX + col))
issue_s = s.v("Issue + label <i>autose</i>", 20, 80, 220, 50, BOX + YELLOW)
human_s = s.v("<b>Human decides</b><br>merge or close", 1370, 520, 220, 70, BOX + YELLOW)
stop = s.v("<b>STOP</b><br>reason written in the failing stage's artifact<br>label autose:failed", 560, 600, 490, 70, BOX + GREY)
s.e(issue_s, ids[0], "")
for a, b, lab in zip(ids, ids[1:], ["pass", "pass", "builds", "all pass", "PR open, CI green"]):
    s.e(a, b, lab)
s.e(ids[3], ids[2], "tests fail:<br>retry ≤ 2", points=[(940, 160), (670, 160)])
s.e(ids[3], ids[1], "still failing:<br>redesign ≤ 1", points=[(970, 120), (400, 120)])
s.e(ids[5], ids[2], "code issue (round 1)", points=[(1450, 420), (640, 420)])
s.e(ids[5], ids[1], "approach issue (round 1)", points=[(1500, 470), (370, 470)])
s.e(ids[5], human_s, "approve / rounds used up")
for i in range(5):
    s.e(ids[i], stop, "", DASH + "strokeColor=#999999;endArrow=open;", points=[(xs[i] + 60, 560), (805, 560)])
s.v("Budgets: turn limit per agent call, token cap per run (from stream-json stats), timeout-minutes per job. "
    "Every arrow back is chosen by orchestrator.py (code), never by an agent.", 20, 700, 1500, 40, TEXT + "fontSize=12;")

j = Page("jobs", "Job graph (Actions)", 1700, 600)
j.v("<b>Actions job graph</b>: the review loop is unrolled into fixed jobs (max 2 rounds, no recursion)",
    20, 0, 1200, 30, TEXT + "fontSize=18;")
jy = 150
g = j.v("<b>gate</b><br>authorise + parse", 20, jy, 150, 70, BOX + GREEN)
b = j.v("<b>build</b><br>stages 1–5", 210, jy, 150, 70, BOX + BLUE)
r1 = j.v("<b>review-1</b><br>read-only", 400, jy, 150, 70, BOX + RED)
p1 = j.v("<b>publish-1</b><br>no LLM", 590, jy, 150, 70, BOX + GREEN)
w1 = j.v("<b>rework-1</b><br>route 2 or 3, rerun 4–5", 780, jy, 170, 70, BOX + BLUE)
r2 = j.v("<b>review-2</b><br>read-only", 990, jy, 150, 70, BOX + RED)
p2 = j.v("<b>publish-2</b><br>no LLM", 1180, jy, 150, 70, BOX + GREEN)
f = j.v("<b>finalize</b> (always)<br>summary + label", 1370, jy, 170, 70, BOX + GREEN)
rv = j.v("<b>mode = review</b><br>(/autose review on a PR,<br>used for seeded PRs)", 210, 330, 170, 80, BOX + YELLOW)
j.e(g, b, "mode=build")
j.e(b, r1, "PR #")
j.e(r1, p1, "artifact")
j.e(p1, w1, "changes<br>requested")
j.e(w1, r2, "")
j.e(r2, p2, "artifact")
j.e(p2, f, "")
j.e(p1, f, "approved", points=[(665, 100), (1455, 100)])
j.e(g, rv, "mode=review", points=[(95, 370)])
j.e(rv, r1, "", points=[(475, 370)])
save(f"{OUT}/stage-map.drawio", [s, j])

# ------------------------------------------------------------------ sequence view (real run 45354704591, issue #4)
q = Page("seq", "Sequence view: run 45354704591", 1700, 1000)
q.v("<b>Sequence view: real run 45354704591</b> (issue #4 → PR #11). Times are UTC from the job timings and state "
    "events; durations are measured agent-call times (usage/*.json).", 20, 0, 1500, 30, TEXT + "fontSize=16;")
parts = ["Maintainer", "gate job", "main graph (code)", "builder agents<br>(gemini -p)", "test workers x4<br>(parallel)",
         "GitHub PR + CI", "review graph<br>(read-only job)", "publish / finalize"]
fills = [YELLOW, GREEN, GREEN, BLUE, PURPLE, RED, BLUE, RED]
centers = []
for i, (name, fill) in enumerate(zip(parts, fills)):
    x = 110 + i * 190
    q.v(name, x, 50, 150, 900,
        "shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;html=1;container=0;collapsible=0;"
        "recursiveResize=0;outlineConnect=0;size=50;" + fill)
    centers.append(x + 75)
M, GA, MG, BU, WK, GH, RV, PB = centers
RET = "html=1;verticalAlign=bottom;endArrow=open;dashed=1;fontSize=11;labelBackgroundColor=#ffffff;"
steps = [
    ("08:16:38", M, GA, "/autose comment on issue #4"),
    ("08:16:48", GA, MG, "author OWNER ✓ → mode=build; 'run started' comment"),
    ("08:17:09", MG, BU, "intake (branch autose/issue-4) → understand + A1 skill"),
    ("08:17:40", BU, MG, "spec.md: 6 ACs; AC lint ✓ (29.9 s)", RET),
    ("08:18:03", BU, MG, "design.md: files + functions exist ✓ (23.0 s)", RET),
    ("08:18:46", BU, MG, "src/mistune/toc.py: import, ruff, strict mypy ✓ (42.9 s)", RET),
    ("08:18:46", MG, WK, "orchestrator: Send 3 AC groups + e2e worker"),
    ("08:19:51", WK, MG, "4 WorkerResults (28.8-41.7 s) → merge: full suite ✓, 6/6 ACs covered", RET),
    ("08:19:51", MG, GH, "release: push, open PR #11 (pr.md), dispatch tests.yml"),
    ("08:23:26", GH, MG, "CI run 45355186100 green (lint, docs, py3.11-3.15, pypy)", RET),
    ("08:23:32", GH, RV, "review-1: linked issue + PR diff + PR-head checkout only"),
    ("08:24:10", RV, PB, "verdict.json: approve, 0 findings (pytest, ruff, mypy, issue example; 15.8 s)"),
    ("08:24:30", PB, GH, "review posted + label autose:approved", RET),
    ("08:24:53", PB, M, "finalize: summary comment on #4, label autose:done", RET),
    ("human", M, GH, "a human merges or closes PR #11 (the bot never merges)"),
]
y = 140
for tm, a, b, label, *st in steps:
    q.v(tm, 10, y - 14, 90, 20, TEXT + "fontSize=11;fontFamily=Courier New;fontColor=#2f5fbf;")
    q.msg(label, a, b, y, st[0] if st else None)
    y += 52
q.v("Total 8 min 15 s · 8 agent calls · 2.00M input tokens (79% cached), 14.5k output · $0.21 · hidden tests 4/4",
    110, y + 10, 1300, 24, TEXT + "fontSize=12;")
save(f"{OUT}/sequence-view.drawio", [q])
print("wrote stage-map.drawio and sequence-view.drawio")
