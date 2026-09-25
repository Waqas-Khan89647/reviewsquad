"""Record review start/finish and the manual baseline for the impact numbers."""
import time

from .common import STATE, read_json, write_json

PATH = STATE / "metrics.json"


def _load():
    return read_json(PATH, {"manual_baseline_minutes": None, "started_at": None, "finished_at": None})


def mark(which):
    data = _load()
    data[f"{which}_at"] = time.time()
    write_json(PATH, data)


def baseline(minutes):
    data = _load()
    data["manual_baseline_minutes"] = float(minutes)
    write_json(PATH, data)
