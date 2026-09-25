"""Turn the pull request (git diff against main) into a review brief for the agents."""
import re

from .common import APP, BASE_BRANCH, STATE, git, short, write_json


def changed_files():
    out = git("diff", "--name-status", f"{BASE_BRANCH}...HEAD", "--", APP)
    files = []
    for line in out.strip().splitlines():
        status, path = line.split("\t")[0], line.split("\t")[-1]
        if path.endswith(".py"):
            files.append({"path": path, "status": {"A": "added", "M": "modified", "D": "deleted"}.get(status[0], status)})
    return files


def added_lines(path):
    """Return {line_number: text} for lines added by the PR in this file."""
    diff = git("diff", "-U0", f"{BASE_BRANCH}...HEAD", "--", path)
    lines, new_no = {}, 0
    for raw in diff.splitlines():
        m = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", raw)
        if m:
            new_no = int(m.group(1))
            continue
        if raw.startswith("+") and not raw.startswith("+++"):
            lines[new_no] = raw[1:]
            new_no += 1
    return lines


def run():
    branch = git("rev-parse", "--abbrev-ref", "HEAD").strip()
    commits = git("log", "--format=%s", f"{BASE_BRANCH}..HEAD").strip().splitlines()
    files = changed_files()
    total_added = 0
    md = [f"# Pull request under review: `{branch}` -> `{BASE_BRANCH}`", "",
          "Commits: " + "; ".join(commits), "",
          "Line numbers below are line numbers in the NEW version of each file.", ""]
    for f in files:
        added = added_lines(f["path"]) if f["status"] != "deleted" else {}
        f["added_lines"] = sorted(added)
        total_added += len(added)
        md.append(f"## `{f['path']}` ({f['status']}, +{len(added)} lines)")
        md.append("```python")
        md += [f"{n:>4} | {t}" for n, t in sorted(added.items())]
        md.append("```")
        md.append("")
    brief = {"branch": branch, "base": BASE_BRANCH, "commits": commits,
             "files": [{"path": f["path"], "short": short(f["path"]), "status": f["status"],
                        "added_lines": f["added_lines"]} for f in files],
             "lines_added": total_added}
    write_json(STATE / "pr.json", brief)
    (STATE / "pr.md").write_text("\n".join(md), encoding="utf-8")
    return brief
