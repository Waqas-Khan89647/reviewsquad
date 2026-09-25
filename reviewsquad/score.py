"""Compare what the review found with the planted issues (benchmark/answer_key.json)."""
from .common import ROOT, STATE, read_json, write_json
from .findings import all_findings


def _matches(issue, file, line, end_line, text, area):
    if area not in issue.get("areas", [area]):
        return False
    kws = issue.get("keywords")
    if kws and not any(k in text.lower() for k in kws):
        return False
    if file in issue.get("also_files", []):
        return True
    if issue["file"] != "*" and file != issue["file"]:
        return False
    return any(line <= b and end_line >= a for a, b in issue["lines"])


def run():
    key = read_json(ROOT / "benchmark" / "answer_key.json")
    agent = all_findings()
    checks = (read_json(STATE / "checks_before.json") or {}).get("findings", [])
    results = []
    for issue in key["issues"]:
        by_agents = sorted({f["reviewer"] for f in agent
                            if _matches(issue, f["file"], f["line"], f["end_line"], f["title"] + " " + f["fix"], f["reviewer"])})
        by_checks = any(_matches(issue, c["file"], c["line"], c["line"], c["title"] + " " + c["fix"], c["area"]) for c in checks)
        results.append({**{k: issue[k] for k in ("id", "title", "area", "severity")},
                        "caught_by_agents": by_agents, "caught_by_checks": by_checks})
    score = {"total": len(results),
             "caught_squad": sum(1 for r in results if r["caught_by_agents"] or r["caught_by_checks"]),
             "caught_checks_only": sum(1 for r in results if r["caught_by_checks"]),
             "caught_agents": sum(1 for r in results if r["caught_by_agents"]),
             "issues": results}
    write_json(STATE / "score.json", score)
    return score
