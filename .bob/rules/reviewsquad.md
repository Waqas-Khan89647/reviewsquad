# Project rules for IBM Bob (ReviewSquad)
- Reviewers never edit files; they record findings with `python -m reviewsquad add`.
- Never open, read or search anything in `benchmark/`. It is the scoring key.
- Never write passwords, API keys or tokens into files. Secrets live only in `.env` (git-ignored).
- Never delete or weaken tests.
- Line numbers in findings refer to the new version of the file.
