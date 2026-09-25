"""Store review findings. Each reviewer subagent records findings with `add`.

Every finding is its own small JSON file, so subagents running in parallel
never overwrite each other.
"""
import time

from .common import FINDINGS, read_json, write_json

REVIEWERS = ["security", "logic", "tests", "guidelines", "lead"]
SEVERITIES = ["high", "medium", "low"]


def add(reviewer, file, line, severity, title, fix, end_line=None):
    if reviewer not in REVIEWERS:
        raise SystemExit(f"reviewer must be one of {REVIEWERS}")
    if severity not in SEVERITIES:
        raise SystemExit(f"severity must be one of {SEVERITIES}")
    file = file.replace("\\", "/")
    if file.startswith("sample_app/"):
        file = file[len("sample_app/"):]
    item = {"reviewer": reviewer, "file": file, "line": int(line),
            "end_line": int(end_line) if end_line else int(line),
            "severity": severity, "title": title, "fix": fix, "created": time.time()}
    write_json(FINDINGS / f"{reviewer}-{time.time_ns()}.json", item)
    return item


def all_findings():
    if not FINDINGS.exists():
        return []
    items = [read_json(p) for p in sorted(FINDINGS.glob("*.json"))]
    order = {s: i for i, s in enumerate(SEVERITIES)}
    return sorted(items, key=lambda f: (order[f["severity"]], f["file"], f["line"]))
