# ReviewSquad

**Parallel AI code review with IBM Bob.** When a pull request arrives, a Review Lead agent
starts four specialist reviewer subagents at the same time: Security, Bugs & Logic, Tests,
and Team Rules. They check the change against the team's own guidelines document, a Fixer
agent repairs what they found, and ReviewSquad publishes a before-and-after report.

Live report: `https://<your-github-username>.github.io/reviewsquad/`

## The problem
Code review is slow and inconsistent. Reviewers are busy, so pull requests wait for hours,
and a tired reviewer skims: tests pass, looks fine, approved. Security holes and logic bugs
that tests don't cover slip into production, and fixing them later costs far more.

## How it works
| Step | Who | What happens |
|------|-----|--------------|
| Read the change | `python -m reviewsquad prepare` | Turns the git diff into a review brief with line numbers |
| Quick checks | `python -m reviewsquad checks before` | Linter-style checks and the test suite give hard evidence |
| Read the rules | Review Lead (document understanding) | Reads the team's guidelines PDF |
| Review in parallel | 4 reviewer subagents | Security, logic, tests and team rules, at the same time; each records findings |
| Merge | `python -m reviewsquad summary` | One review with a verdict, sorted by severity |
| Fix | Fixer agent | Fixes every finding and adds a test for each bug |
| Prove it | `checks after`, `score`, `report` | Tests and checks rerun; report published to `docs/` |

## The demo
`setup_demo.py` creates a store app (`main`) and a teammate's pull request
(`feature/coupons-and-admin-login`) containing 11 planted problems. **The pull request passes
all its tests**, just like many buggy pull requests do. `benchmark/answer_key.json` lists the planted
problems so the review can be scored; it is hidden from Bob with `.bobignore`.

In our run: automated checks alone caught 7 of 11; ReviewSquad caught [11] of 11.

## Quick start
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python setup_demo.py
```
Then, in IBM Bob, choose the **Review Lead** mode and type: *Review this pull request.*

## Layout
```
sample_app/        demo store app + tests
reviewsquad/       the CLI (prepare, checks, add, summary, score, report, ...)
team_docs/         the team's code review guidelines (PDF read by Bob)
.bob/, bob_modes/  Bob custom modes (Review Lead, 4 reviewers, Fixer) and rules
benchmark/         planted-problem answer key (hidden from Bob)
docs/              generated report (GitHub Pages)
submission/        hackathon texts, video script, slide outline
```
No credentials are needed or stored.
