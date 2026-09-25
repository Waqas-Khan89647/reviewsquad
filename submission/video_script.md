# Video script (about 2:50, never over 3:00)

Record in parts and join them (Clipchamp comes free with Windows).
You may speed up waiting parts; add a small "sped up" label so it stays honest.

| Time | Show on screen | Say |
|------|----------------|-----|
| 0:00-0:20 | Title "Tests passed. Code approved. Hacked." then the pull request files | "Code review is where bugs should be caught, but reviewers are busy. Pull requests wait for hours, then get a quick look: tests pass, approved. Security holes and logic bugs slip through." |
| 0:20-0:40 | Terminal: `python -m reviewsquad checks before` showing 8/8 passed | "Here's a real example: a teammate's pull request adding coupons and an admin login. All tests pass. Would you approve it?" |
| 0:40-1:00 | Bob chat, Review Lead mode, typing "Review this pull request"; Bob opening the guidelines PDF | "Meet ReviewSquad, built on IBM Bob. I ask the Review Lead to review it. First, Bob reads our team's own code review guidelines, a PDF, using document understanding." |
| 1:00-1:40 | Four reviewer subtasks running; findings appearing | "Then it starts four specialist reviewers in parallel: security, bugs and logic, tests, and team rules. Each is read-only, and each cites our guideline rules." |
| 1:40-2:00 | Verdict: REQUEST CHANGES; the list of findings | "The results are merged into one review: request changes. SQL injection, a backdoor password, and an inverted expiry check that accepted expired coupons, which the tests never noticed." |
| 2:00-2:25 | Typing "yes"; Fixer editing; `checks after` showing all tests passing and 0 warnings | "With my approval, the Fixer repairs every finding and adds a test for each bug. All tests pass, zero warnings." |
| 2:25-2:45 | Report page in the browser | "The report shows the result: [11 of 11] planted problems caught, versus 7 for automated checks alone, in [Y] minutes instead of [X]." |
| 2:45-2:55 | Title card + links | "ReviewSquad: every pull request gets a full team review, in minutes. Built with IBM Bob." |
