"""Merge all reviewer findings into one pull-request review (REVIEW.md)."""
from collections import Counter

from .common import ROOT, STATE
from .findings import all_findings

ICON = {"high": "🔴", "medium": "🟠", "low": "🟡"}


def build():
    items = all_findings()
    counts = Counter(f["severity"] for f in items)
    verdict = "REQUEST CHANGES" if counts["high"] else ("APPROVE WITH COMMENTS" if items else "APPROVE")
    by_rev = Counter(f["reviewer"] for f in items)
    md = ["# ReviewSquad review", "",
          f"**Verdict: {verdict}**  ",
          f"{len(items)} findings: {counts['high']} high, {counts['medium']} medium, {counts['low']} low.  ",
          "Reviewers: " + ", ".join(f"{r} ({n})" for r, n in sorted(by_rev.items())), ""]
    for sev in ("high", "medium", "low"):
        group = [f for f in items if f["severity"] == sev]
        if not group:
            continue
        md += [f"## {ICON[sev]} {sev.capitalize()}", ""]
        for f in group:
            loc = f"{f['file']}:{f['line']}" + (f"-{f['end_line']}" if f["end_line"] != f["line"] else "")
            md.append(f"- [ ] **{f['title']}** (`{loc}`, {f['reviewer']} reviewer)  ")
            md.append(f"  Fix: {f['fix']}")
        md.append("")
    text = "\n".join(md)
    (STATE / "REVIEW.md").write_text(text, encoding="utf-8")
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs" / "REVIEW.md").write_text(text, encoding="utf-8")
    return verdict, items
