"""Fast automated checks (like a linter) plus the test suite.

These give the reviewer agents hard evidence. They catch the obvious problems;
the Bob agents are needed for logic bugs, intent and risk.
"""
import ast
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

from .common import ROOT, STATE, short, write_json
from .prepare import added_lines, changed_files

PATTERNS = [
    ("hardcoded-secret", "security", "high", "Hard-coded password/secret",
     re.compile(r"^\s*\w*(PASSWORD|SECRET|TOKEN|API_KEY)\w*\s*=\s*[\"'][^\"']+[\"']", re.I),
     "Load secrets from environment variables or a secrets manager."),
    ("sql-string", "security", "high", "SQL built from a string (injection risk)",
     re.compile(r"execute\(\s*f[\"']|execute\([^)]*(\.format\(|\"\s*%\s|\"\s*\+)"),
     "Use a parameterised query with ? placeholders."),
    ("eval-exec", "security", "high", "eval()/exec() on data",
     re.compile(r"\b(eval|exec)\("), "Never evaluate text as code; parse it explicitly."),
    ("bare-except", "logic", "medium", "Bare except hides all errors",
     re.compile(r"^\s*except\s*:"), "Catch specific exceptions and log them."),
    ("print-call", "guidelines", "low", "print() used instead of logging",
     re.compile(r"^\s*print\("), "Use the logging module."),
]


def _ast_checks(path, text, new_lines, test_text):
    out = []
    try:
        tree = ast.parse(text)
    except SyntaxError as err:
        return [("syntax-error", "logic", "high", f"Syntax error: {err.msg}", err.lineno or 1, "Fix the syntax.")]
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.lineno in new_lines:
            for d in node.args.defaults + node.args.kw_defaults:
                if isinstance(d, (ast.List, ast.Dict, ast.Set)):
                    out.append(("mutable-default", "logic", "medium",
                                f"Mutable default argument in {node.name}()", node.lineno,
                                "Use None as the default and create the list inside the function."))
            public = not node.name.startswith("_")
            if public and ast.get_docstring(node) is None:
                out.append(("missing-docstring", "guidelines", "low",
                            f"Public function {node.name}() has no docstring", node.lineno,
                            "Add a one-line docstring saying what it does."))
    for node in tree.body:  # top-level public functions only
        if isinstance(node, ast.FunctionDef) and node.lineno in new_lines and not node.name.startswith("_"):
            if not re.search(rf"\b{node.name}\b", test_text):
                out.append(("untested-function", "tests", "high",
                            f"New function {node.name}() is never called by any test", node.lineno,
                            "Add unit tests covering normal, edge and error cases."))
    return out


def run_tests(label):
    xml_path = STATE / f"junit_{label}.xml"
    STATE.mkdir(exist_ok=True)
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q", f"--junitxml={xml_path}"],
                          cwd=ROOT, capture_output=True, text=True)
    tests = []
    if xml_path.exists():
        for case in ET.parse(xml_path).getroot().iter("testcase"):
            bad = case.find("failure") if case.find("failure") is not None else case.find("error")
            tests.append({"name": f"{case.get('classname')}::{case.get('name')}", "passed": bad is None,
                          "message": bad.get("message", "")[:200] if bad is not None else ""})
    return tests, proc.stdout


def run(label):
    test_text = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "sample_app" / "tests").glob("test_*.py"))
    findings = []
    files = [f for f in changed_files() if f["status"] != "deleted" and "/tests/" not in f["path"]]
    for f in files:
        path = ROOT / f["path"]
        text = path.read_text(encoding="utf-8")
        new = set(added_lines(f["path"]))
        for no, line in enumerate(text.splitlines(), 1):
            if no not in new:
                continue
            for cid, area, sev, title, rx, fix in PATTERNS:
                if rx.search(line):
                    findings.append({"check": cid, "area": area, "severity": sev, "file": short(f["path"]),
                                     "line": no, "title": title, "fix": fix, "code": line.strip()})
        for cid, area, sev, title, no, fix in _ast_checks(path, text, new, test_text):
            findings.append({"check": cid, "area": area, "severity": sev, "file": short(f["path"]),
                             "line": no, "title": title, "fix": fix})
    tests, output = run_tests(label)
    result = {"label": label, "findings": sorted(findings, key=lambda x: (x["file"], x["line"])),
              "tests": tests}
    write_json(STATE / f"checks_{label}.json", result)
    return result, output
