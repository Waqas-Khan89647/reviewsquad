# Long Description: Problem & Solution Statement

## The problem
Code review is one of the slowest steps in software delivery. Pull requests wait hours or
days for a busy reviewer, and when the review finally happens it's often rushed: the tests
pass, the diff looks reasonable, approved. But passing tests don't mean safe code. SQL
injection, leaked passwords, inverted conditions and untested business logic regularly slip
through, and a bug found after merge costs far more to fix than one caught in review.
Reviews are also inconsistent: every reviewer checks different things, and the team's written
guidelines are rarely checked line by line.

## The solution
ReviewSquad turns code review into a coordinated team of IBM Bob agents. The developer opens
the pull request in Bob, selects the Review Lead mode and types "Review this pull request."
From there:

1. ReviewSquad converts the git diff into a review brief with exact line numbers, and runs
   fast automated checks plus the test suite for hard evidence.
2. The Review Lead reads the team's code review guidelines PDF (document understanding).
3. It starts four specialist reviewer subagents in parallel: Security, Bugs & Logic, Tests,
   and Team Rules. Each is read-only, focuses on its specialty, cites guideline rules, and
   records structured findings.
4. The findings are merged into one review with a clear verdict, sorted by severity.
5. With the developer's approval, a Fixer agent repairs every finding and adds a test for
   each bug. Tests and checks run again.
6. ReviewSquad publishes a report showing what was found, by whom, and the before/after state.

Target users are development teams of any size, especially those where senior reviewers are
a bottleneck. Developers interact entirely through Bob's chat; reviewers read one report.

## Why it's different
Most AI review tools are a single pass that leaves a list of comments. ReviewSquad runs
the full workflow: understand the rules, review, merge, fix, verify, report. Splitting the
review across specialist subagents mirrors how strong human teams work and keeps each agent
focused, so it finds deep logic bugs a single generic pass skims over. Deterministic checks
provide evidence; agents provide judgment; a human approves before any fix. And because the
guidelines are a document, each team gets reviews against its own rules, not generic advice.

We also measure it honestly. Our demo pull request contains 11 planted problems and passes
all its tests. Automated checks alone found 7. ReviewSquad found [11] of 11, including an
inverted coupon-expiry check and unvalidated discounts that no test or linter flagged.

## Impact
- Review time: [X] minutes by hand vs [Y] minutes with ReviewSquad.
- Problems caught before merge: [11/11] vs 7/11 for automated checks alone.
- After fixes: tests went from 8 to [16], all passing, and automated warnings from 22 to [0].
