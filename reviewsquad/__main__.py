"""ReviewSquad commands:  python -m reviewsquad <command>

  prepare                 read the pull request, write .reviewsquad/pr.md for the reviewers
  checks <before|after>   run automated checks + tests
  add ...                 record one finding (used by the reviewer agents), see below
  list                    show all findings
  summary                 merge findings into one review: .reviewsquad/REVIEW.md
  score                   compare findings with the planted problems (benchmark)
  report                  build docs/index.html
  start / finish          mark when the review starts / ends (timing)
  baseline <minutes>      how long a manual review takes (your measured number)
  reset                   go back to the pull request as submitted (for practice)

add example:
  python -m reviewsquad add --reviewer security --file store/users.py --line 44
      --severity high --title "SQL injection" --fix "Use ? placeholders"
"""
import argparse
import shutil
import sys

from . import checks, findings, prepare, report, score, summary, timer
from .common import STATE, git, read_json, write_json


def main(argv):
    if not argv or argv[0] in ("help", "-h", "--help"):
        print(__doc__)
        return 0
    cmd, rest = argv[0], argv[1:]
    if cmd == "prepare":
        b = prepare.run()
        print(f"Pull request {b['branch']} -> {b['base']}: {len(b['files'])} files, {b['lines_added']} new lines.")
        for f in b["files"]:
            print(f"  {f['status']:<9} {f['path']}")
        print("Review brief written to .reviewsquad/pr.md")
    elif cmd == "checks":
        label = rest[0] if rest else "before"
        result, _ = checks.run(label)
        t = result["tests"]
        print(f"[{label}] tests: {sum(x['passed'] for x in t)}/{len(t)} passed")
        print(f"[{label}] automated check warnings: {len(result['findings'])}")
        for f in result["findings"]:
            print(f"  {f['severity']:<6} {f['file']}:{f['line']:<4} {f['title']}")
    elif cmd == "add":
        p = argparse.ArgumentParser(prog="python -m reviewsquad add")
        p.add_argument("--reviewer", required=True, choices=findings.REVIEWERS)
        p.add_argument("--file", required=True)
        p.add_argument("--line", required=True, type=int)
        p.add_argument("--end-line", type=int)
        p.add_argument("--severity", required=True, choices=findings.SEVERITIES)
        p.add_argument("--title", required=True)
        p.add_argument("--fix", required=True)
        a = p.parse_args(rest)
        f = findings.add(a.reviewer, a.file, a.line, a.severity, a.title, a.fix, a.end_line)
        print(f"Recorded [{f['severity']}] {f['file']}:{f['line']} {f['title']}")
    elif cmd == "list":
        items = findings.all_findings()
        for f in items:
            print(f"{f['severity']:<6} {f['reviewer']:<10} {f['file']}:{f['line']:<4} {f['title']}")
        print(f"{len(items)} findings")
    elif cmd == "summary":
        verdict, items = summary.build()
        print(f"Verdict: {verdict} ({len(items)} findings). Written to .reviewsquad/REVIEW.md and docs/REVIEW.md")
    elif cmd == "score":
        s = score.run()
        for r in s["issues"]:
            who = ", ".join(r["caught_by_agents"]) or ("automated check" if r["caught_by_checks"] else "MISSED")
            print(f"  {r['id']} {r['title'][:55]:<55} {who}")
        print(f"ReviewSquad caught {s['caught_squad']}/{s['total']} "
              f"(automated checks alone: {s['caught_checks_only']}/{s['total']})")
    elif cmd == "report":
        print(f"Report written to {report.build()}")
    elif cmd in ("start", "finish"):
        timer.mark("started" if cmd == "start" else "finished")
        print(f"Timer: {cmd} recorded.")
    elif cmd == "baseline":
        timer.baseline(rest[0])
        print(f"Manual review baseline: {rest[0]} minutes.")
    elif cmd == "reset":
        answer = input("This erases the review and all code changes made after the pull request. Type yes to continue: ")
        if answer.strip().lower() != "yes":
            print("Cancelled. Nothing was changed.")
            return 0
        keep = (read_json(STATE / "metrics.json") or {}).get("manual_baseline_minutes")
        git("reset", "--hard", "pr-submitted")
        shutil.rmtree(STATE, ignore_errors=True)
        if keep:
            write_json(STATE / "metrics.json", {"manual_baseline_minutes": keep, "started_at": None, "finished_at": None})
        print("Reset to the pull request as submitted. Findings cleared.")
    else:
        print(f"Unknown command '{cmd}'.\n{__doc__}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
