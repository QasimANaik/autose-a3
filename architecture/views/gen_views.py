"""Generate the draw.io architecture views (component, stage map + job graph, sequence).

Usage: python3 architecture/views/gen_views.py architecture/views
Edit the .drawio files by hand afterwards if you like; re-running this overwrites them.
"""
import sys
from xml.sax.saxutils import quoteattr

OUT = sys.argv[1] if len(sys.argv) > 1 else "."

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

BUILDER_MODEL = "gemini-3-flash-preview"
REVIEWER_MODEL = "gemini-3-pro-preview"


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


# ------------------------------------------------------------------ component view
c = Page("comp", "Component view", 1700, 1150)
c.v("<b>AutoSE component view</b>: agents, jobs, tools, permissions (agent runtime: Gemini CLI, headless)",
    20, 0, 1100, 30, TEXT + "fontSize=18;")
human = c.v("Maintainer<br>(OWNER / MEMBER /<br>COLLABORATOR)", 30, 70, 40, 60,
            "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;")
c.v("GitHub fork  QasimANaik/mistune @ f7ec702  (main protected by ruleset + CODEOWNERS)", 140, 40, 1530, 140, LANE + GREY)
issue = c.v("<b>Issue #N</b><br>label <i>autose</i> / comment <i>/autose</i><br><font color='#b85450'>untrusted text</font>",
            160, 80, 190, 80, BOX + YELLOW)
branch = c.v("<b>Branch</b><br>autose/issue-N<br>(code + new tests only)", 380, 80, 170, 80, BOX + YELLOW)
pr = c.v("<b>Pull request</b><br>body = pr.md<br>reviews + labels", 580, 80, 170, 80, BOX + YELLOW)
arts = c.v("<b>Workflow artifacts</b><br>build-N, review-k<br>(state between jobs)", 780, 80, 190, 80, BOX + YELLOW)
ci = c.v("<b>tests.yml (CI)</b><br>ruff, mypy, docs, pytest<br>via workflow_dispatch", 1000, 80, 190, 80, BOX + YELLOW)
sec = c.v("<b>Secret</b><br>GEMINI_API_KEY<br>(budget alert set)", 1220, 80, 170, 80, BOX + YELLOW)
c.v("<b>State</b><br>out/state.json in artifact<br>+ marker comment on issue", 1420, 80, 220, 80, BOX + YELLOW)

c.v("Workflow  .github/workflows/autose.yml   (permissions: {} by default; concurrency group autose-issue-N, queued)",
    140, 220, 1530, 700, LANE + GREY)
gate = c.v("<b>job: gate</b><br>perm: issues:write<br>no secrets, no LLM<br>- event + author_association<br>- ignore bot comments<br>- outputs issue, mode, variant",
           160, 270, 210, 150, BOX + GREEN)
c.v("job: build   perm: contents, pull-requests, issues, actions = write   secret: GEMINI_API_KEY   timeout 45 min",
    400, 260, 760, 500, LANE + BLUE)
orch = c.v("<b>orchestrator.py</b>: deterministic state machine (stage, attempt, redesigns, token budget)<br>"
           "only process holding GH_TOKEN; agents run with stripped env + own HOME; checkout persist-credentials: false",
           420, 300, 720, 60, BOX + ORANGE)
a_spec = c.v(f"<b>Spec agent</b><br>gemini -p (fresh)<br>+ A1 skill<br>→ spec.md", 420, 390, 165, 90, BOX + PURPLE)
a_des = c.v("<b>Design agent</b><br>gemini -p (fresh)<br>+ ARCHITECTURE.md<br>→ design.md", 605, 390, 165, 90, BOX + PURPLE)
a_imp = c.v("<b>Implement agent</b><br>gemini -p (fresh)<br>read, replace, write<br>→ diff.patch", 790, 390, 165, 90, BOX + PURPLE)
a_tst = c.v("<b>Test agent</b><br>gemini -p (fresh)<br>pytest, ruff<br>→ test_report.md", 975, 390, 165, 90, BOX + PURPLE)
checks = c.v("<b>Deterministic checks</b> (pass/fail decided by code)<br>spec_lint.py | design_refs.py (AST) | build_check (uv sync, import, ruff, mypy) | diff_guard.py | pytest",
             420, 510, 720, 60, BOX + GREEN)
rel = c.v("<b>release</b> (no LLM, gh CLI): git push branch → gh pr create --body-file pr.md → gh workflow run tests.yml → gh run watch",
          420, 600, 720, 60, BOX + ORANGE)
c.v(f"Builder model: {BUILDER_MODEL}. Tools via Gemini CLI policy (--admin-policy): read_file, glob, grep_search, "
    "write_file, replace, run_shell_command(uv run pytest | ruff | mypy | python). Denied: web_fetch, google_web_search, "
    "git push, gh, curl, wget. Anything not allowed = ask_user = denied in headless mode.",
    420, 680, 720, 70, TEXT + "fontSize=11;")

c.v("job: review-k (k = 1, 2)   perm: contents:read, pull-requests:read", 1190, 260, 460, 230, LANE + RED)
rev = c.v(f"<b>Reviewer agent</b> (independent)<br>gemini -p, <b>{REVIEWER_MODEL}</b>, own prompt<br>"
          "sees ONLY: issue, PR diff, PR-head checkout<br>never downloads build-* artifacts<br>"
          "tools: read_file, glob, grep_search, shell(uv run pytest | python, git diff | log)<br>"
          "write_file, replace, gh, push denied<br>→ review.md + verdict.json",
          1210, 300, 420, 175, BOX + RED)
pub = c.v("<b>job: publish-k</b>  perm: pull-requests:write<br>no LLM, no API key<br>gh pr review --approve | --request-changes",
          1190, 520, 460, 80, BOX + GREEN)
rew = c.v("<b>job: rework-1</b> (only if changes requested in round 1)<br>same perms as build; orchestrator rework<br>route = code → stage 3, approach → stage 2",
          1190, 630, 460, 90, BOX + BLUE)
fin = c.v("<b>job: finalize</b> (always)<br>summary comment + label done | failed | needs-human", 1190, 750, 460, 60, BOX + GREEN)

api = c.v(f"<b>Gemini API</b><br>builder: {BUILDER_MODEL}<br>reviewer: {REVIEWER_MODEL}", 420, 960, 260, 80,
          "shape=cloud;whiteSpace=wrap;html=1;" + GREY)
skill = c.v("<b>A1 skill</b><br>requirements-spec", 720, 960, 180, 70, BOX + GREY)
archmd = c.v("<b>ARCHITECTURE.md</b><br>(from A2)", 930, 960, 180, 70, BOX + GREY)
merge = c.v("<b>Human decides</b><br>merge or close (bot never merges)", 1300, 960, 260, 70, BOX + YELLOW)

c.e(human, issue, "label / comment")
c.e(issue, gate, "issues.labeled /<br>issue_comment", points=[(255, 200), (265, 200)])
c.e(gate, orch, "needs: gate")
for a in (a_spec, a_des, a_imp, a_tst):
    c.e(orch, a, "", EDGE + "fontSize=10;")
    c.e(a, checks, "", DASH + "fontSize=10;")
c.e(checks, rel, "all pass")
c.e(rel, branch, "push", points=[(465, 200)])
c.e(rel, pr, "gh pr create", points=[(665, 200)])
c.e(rel, ci, "dispatch + watch", points=[(1095, 630)])
c.e(orch, arts, "upload artifacts", DASH, points=[(875, 280)])
c.e(pr, rev, "checkout PR head (read-only)", points=[(665, 240), (1420, 240)])
c.e(rev, pub, "review.md + verdict.json<br>(artifact)")
c.e(pub, pr, "post review", DASH, points=[(1670, 560), (1670, 200), (700, 200)])
c.e(pub, rew, "changes requested")
c.e(rew, rev, "round 2", points=[(1660, 675), (1660, 390)])
c.e(rew, fin, "")
c.e(sec, orch, "env (build, review only)", DASH, points=[(1305, 245), (780, 245)])
c.e(a_spec, skill, "", DASH, points=[(502, 940), (810, 940)])
c.e(a_des, archmd, "", DASH, points=[(687, 920), (1020, 920)])
c.e(a_tst, api, "generateContent", DASH, points=[(1057, 900), (550, 900)])
c.e(rev, api, "", DASH, points=[(1640, 390), (1680, 390), (1680, 1060), (550, 1060)])
c.e(fin, merge, "PR ready")
save(f"{OUT}/component-view.drawio", [c])

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

# ------------------------------------------------------------------ sequence view (planned)
q = Page("seq", "Sequence view (PLANNED)", 1600, 1150)
q.v("<b>Sequence view: PLANNED</b>. Replace with one real run after Step 5 (run id, timestamps, attempts).",
    20, 0, 1300, 30, TEXT + "fontSize=18;")
parts = ["Maintainer", "GitHub (issue/PR)", "gate job", "orchestrator.py", "Builder agent<br>(gemini -p)",
         "Checks / CI", "Reviewer agent<br>(review-1 job)", "publish-1 job"]
centers = []
for i, name in enumerate(parts):
    x = 20 + i * 190
    q.v(name, x, 50, 150, 1060,
        "shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;html=1;container=0;collapsible=0;"
        "recursiveResize=0;outlineConnect=0;size=50;" + (RED if "Reviewer" in name else BLUE))
    centers.append(x + 75)
M, GH, GA, OR, BU, CK, RV, PB = centers
RET = "html=1;verticalAlign=bottom;endArrow=open;dashed=1;fontSize=11;labelBackgroundColor=#ffffff;"
steps = [
    (M, GH, "1. add label autose to issue #N"),
    (GH, GA, "2. issues.labeled event"),
    (GA, GH, "3. check author_association; comment 'run started'", RET),
    (GA, OR, "4. needs: gate (issue N, mode=build)"),
    (OR, BU, "5. Stage 1: issue (in untrusted tags) + A1 skill"),
    (BU, OR, "6. spec.md", RET),
    (OR, CK, "7. spec_lint → pass"),
    (OR, BU, "8. Stage 2: spec.md + ARCHITECTURE.md"),
    (BU, OR, "9. design.md", RET),
    (OR, CK, "10. design_refs (AST) → pass"),
    (OR, BU, "11. Stage 3: design.md → edit on autose/issue-N"),
    (OR, CK, "12. build_check (ruff, mypy, import) → diff.patch"),
    (OR, BU, "13. Stage 4: tests per AC id"),
    (OR, CK, "14. pytest → fail? back to 11 (≤2) → test_report.md"),
    (OR, GH, "15. push, gh pr create (pr.md), dispatch tests.yml"),
    (CK, OR, "16. CI green (gh run watch)", RET),
    (GH, RV, "17. review-1: issue + PR diff + PR-head checkout ONLY"),
    (RV, CK, "18. reviewer runs pytest / own probes"),
    (RV, PB, "19. review.md + verdict.json (artifact)"),
    (PB, GH, "20. gh pr review (approve | request changes)"),
    (GH, M, "22. PR ready: human merges or closes", RET),
]
y = 140
for st in steps:
    if st[2].startswith("22."):
        q.v("<b>alt</b> [changes requested in round 1] → rework-1 job (route code→3 / approach→2) → review-2 → publish-2",
            GH - 60, y, 1300, 40, "shape=umlFrame;whiteSpace=wrap;html=1;width=40;height=20;" + YELLOW)
        y += 60
    q.msg(st[2], st[0], st[1], y, st[3] if len(st) > 3 else None)
    y += 42
save(f"{OUT}/sequence-view.drawio", [q])
print("wrote component-view, stage-map, sequence-view")
