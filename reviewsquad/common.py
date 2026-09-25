"""Shared paths and small helpers."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / ".reviewsquad"
FINDINGS = STATE / "findings"
APP = "sample_app"
BASE_BRANCH = "main"


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout


def read_json(path, default=None):
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def short(path):
    """sample_app/store/x.py -> store/x.py"""
    p = str(path).replace("\\", "/")
    return p[len(APP) + 1:] if p.startswith(APP + "/") else p
