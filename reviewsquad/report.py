"""Build docs/index.html: the shareable review report (GitHub Pages ready)."""
import html
import time

from .common import ROOT, STATE, read_json
from .findings import all_findings

LANES = [("security", "Security"), ("logic", "Bugs & logic"), ("tests", "Tests"), ("guidelines", "Team rules")]


def _tests_line(checks):
    if not checks or not checks.get("tests"):
        return "not run"
    t = checks["tests"]
    return f"{sum(x['passed'] for x in t)} of {len(t)} passing"


def build():
    score = read_json(STATE / "score.json")
    pr = read_json(STATE / "pr.json") or {"branch": "feature", "base": "main", "files": [], "lines_added": 0}
    before, after = read_json(STATE / "checks_before.json"), read_json(STATE / "checks_after.json")
    metrics = read_json(STATE / "metrics.json") or {}
    items = all_findings()
    e = html.escape

    if score:
        headline = f"Caught {score['caught_squad']} of {score['total']} planted problems before merge."
        lede = (f"Automated checks alone caught {score['caught_checks_only']}. "
                f"Bob's four specialist reviews found {score['caught_agents']}, including the logic bugs "
                f"that passed every test.")
    else:
        headline = f"{len(items)} review findings on {e(pr['branch'])}."
        lede = ""
    mins = None
    if metrics.get("started_at") and metrics.get("finished_at"):
        mins = max((metrics["finished_at"] - metrics["started_at"]) / 60, 0.1)
    base = metrics.get("manual_baseline_minutes")
    if mins and base:
        lede += f" Review time: {mins:.0f} min with ReviewSquad vs about {base:.0f} min by hand."
    elif mins:
        lede += f" Review time: {mins:.0f} min."

    tiles = ""
    if score:
        for r in score["issues"]:
            who = ", ".join(r["caught_by_agents"]) or ("automated check" if r["caught_by_checks"] else "")
            state = "hit" if who else "miss"
            tiles += (f'<li class="tile {state}"><span class="tid">{r["id"]}</span>'
                      f'<span class="ttl">{e(r["title"])}</span>'
                      f'<span class="who">{e(who) if who else "missed"}</span></li>')
        tiles = f'<section><h2>The planted problems</h2><ul class="tiles">{tiles}</ul></section>'

    lanes = ""
    for key, name in LANES:
        mine = [f for f in items if f["reviewer"] == key]
        rows = "".join(f'<li class="sev-{f["severity"]}"><b>{e(f["title"])}</b>'
                       f'<code>{e(f["file"])}:{f["line"]}</code><span>{e(f["fix"])}</span></li>' for f in mine)
        lanes += (f'<div class="lane"><h3>{name}<small>{len(mine)} finding{"" if len(mine) == 1 else "s"}</small></h3>'
                  f'<ul>{rows or "<li class=empty>No findings recorded.</li>"}</ul></div>')

    def chk(c):
        return len(c["findings"]) if c else "–"

    facts = (f'<table><thead><tr><th></th><th>As submitted</th><th>After fixes</th></tr></thead><tbody>'
             f'<tr><td>Tests</td><td>{_tests_line(before)}</td><td>{_tests_line(after)}</td></tr>'
             f'<tr><td>Automated check warnings</td><td>{chk(before)}</td><td>{chk(after)}</td></tr>'
             f'</tbody></table>')
    note = ('<p class="note">The pull request passed all its tests as submitted. '
            'Passing tests did not mean the code was safe.</p>') if before and before.get("tests") and all(
        t["passed"] for t in before["tests"]) else ""
    files = "".join(f"<li><code>{e(f['path'])}</code> {f['status']}</li>" for f in pr["files"])

    page = TEMPLATE.format(headline=e(headline), lede=e(lede), branch=e(pr["branch"]), base=e(pr["base"]),
                           nfiles=len(pr["files"]), nlines=pr["lines_added"], files=files, tiles=tiles,
                           lanes=lanes, facts=facts, note=note, generated=time.strftime("%d %B %Y, %H:%M"))
    out = ROOT / "docs" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return out


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>ReviewSquad report</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400&family=IBM+Plex+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>
:root {{ --ink:#1B1F2A; --paper:#F6F7F9; --panel:#FFFFFF; --line:#DADFE7; --muted:#596273;
  --hit:#198038; --miss:#DA1E28; --med:#B28600; --accent:#6929C4;
  box-sizing:border-box; padding-top:env(safe-area-inset-top,0px); padding-bottom:env(safe-area-inset-bottom,0px); }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --ink:#E8EBF1; --paper:#12151C; --panel:#1B2029;
  --line:#2E3542; --muted:#9BA4B4; --hit:#42BE65; --miss:#FF8389; --med:#F1C21B; --accent:#A56EFF; }} }}
:root[data-theme="dark"] {{ --ink:#E8EBF1; --paper:#12151C; --panel:#1B2029; --line:#2E3542; --muted:#9BA4B4;
  --hit:#42BE65; --miss:#FF8389; --med:#F1C21B; --accent:#A56EFF; }}
*,*::before,*::after {{ box-sizing:border-box; }}
html {{ scroll-padding-top:env(safe-area-inset-top,0px); }}
body {{ margin:0; background:var(--paper); color:var(--ink); font:16px/1.55 "IBM Plex Sans","Segoe UI",system-ui,sans-serif; }}
main {{ max-width:1080px; margin:0 auto; padding:44px 24px 72px; }}
.brand {{ color:var(--accent); font-weight:600; margin:0 0 6px; }}
.pr {{ color:var(--muted); margin:0 0 36px; font-size:0.95rem; }}
h1 {{ font-size:clamp(1.9rem,4.4vw,3rem); line-height:1.1; margin:0 0 16px; max-width:22ch; font-weight:600; }}
.lede {{ font-size:1.12rem; color:var(--muted); max-width:62ch; margin:0 0 44px; }}
h2 {{ font-size:1.2rem; margin:0 0 14px; font-weight:600; }}
section {{ margin:0 0 48px; }}
.tiles {{ list-style:none; margin:0; padding:0; display:grid; grid-template-columns:repeat(auto-fill,minmax(180px,1fr)); gap:10px; }}
.tile {{ background:var(--panel); border:1px solid var(--line); border-left:6px solid var(--hit); border-radius:4px;
  padding:10px 12px; display:flex; flex-direction:column; gap:4px; min-height:118px; }}
.tile.miss {{ border-left-color:var(--miss); }}
.tid {{ font-family:"IBM Plex Mono",Consolas,monospace; font-size:0.8rem; color:var(--muted); }}
.ttl {{ font-weight:600; font-size:0.93rem; line-height:1.3; }}
.who {{ margin-top:auto; font-size:0.85rem; color:var(--hit); }}
.miss .who {{ color:var(--miss); }}
.lanes {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:14px; }}
.lane h3 {{ margin:0 0 10px; font-size:1rem; padding-bottom:8px; border-bottom:3px solid var(--accent); }}
.lane h3 small {{ display:block; font-weight:400; color:var(--muted); font-size:0.85rem; }}
.lane ul {{ list-style:none; margin:0; padding:0; display:grid; gap:8px; }}
.lane li {{ background:var(--panel); border:1px solid var(--line); border-radius:4px; padding:9px 11px; font-size:0.88rem;
  display:flex; flex-direction:column; gap:3px; border-top:3px solid var(--line); }}
.lane li.sev-high {{ border-top-color:var(--miss); }} .lane li.sev-medium {{ border-top-color:var(--med); }}
.lane li span {{ color:var(--muted); }} .lane li.empty {{ color:var(--muted); }}
code {{ font-family:"IBM Plex Mono",Consolas,monospace; font-size:0.84em; overflow-wrap:anywhere; }}
table {{ border-collapse:collapse; background:var(--panel); border:1px solid var(--line); min-width:420px; }}
th,td {{ text-align:left; padding:9px 16px; border-bottom:1px solid var(--line); }}
th {{ font-weight:400; color:var(--muted); }}
.scroll {{ overflow-x:auto; }}
.note {{ color:var(--muted); margin:10px 0 0; }}
.files {{ margin:0; padding-left:20px; color:var(--muted); }}
footer {{ color:var(--muted); font-size:0.9rem; border-top:1px solid var(--line); padding-top:16px; }}
@media (max-width:860px) {{ .lanes {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} }}
@media (max-width:520px) {{ .lanes {{ grid-template-columns:1fr; }} main {{ padding-top:28px; }} }}
</style></head><body><main>
<p class="brand">ReviewSquad</p>
<p class="pr">Pull request <code>{branch}</code> into <code>{base}</code>: {nfiles} files, {nlines} new lines</p>
<h1>{headline}</h1>
<p class="lede">{lede}</p>
{tiles}
<section><h2>Four specialist reviews</h2><div class="lanes">{lanes}</div></section>
<section><h2>Before and after the fixes</h2><div class="scroll">{facts}</div>{note}</section>
<section><h2>Files in this pull request</h2><ul class="files">{files}</ul></section>
<footer>Generated {generated} by ReviewSquad with IBM Bob.</footer>
</main></body></html>
"""
