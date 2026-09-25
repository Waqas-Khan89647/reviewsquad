# Slide outline (8 slides)
1. **ReviewSquad**: parallel AI code review with IBM Bob. Team names.
2. **Problem**: reviews are slow and rushed; passing tests ≠ safe code.
3. **Example**: the pull request passes 8/8 tests but hides 11 problems.
4. **Solution flow**: Prepare → Read rules (PDF) → 4 reviewers in parallel → Merge → Fix → Verify → Report.
5. **How Bob powers it**: 6 custom modes, subagents, parallel tasks, document understanding, human approval before fixing. Screenshot of Bob.
6. **Results**: the report screenshot. [11/11] vs 7/11; [Y] min vs [X] min; tests 8 → [16], warnings 22 → [0].
7. **Why it's trustworthy**: reviewers are read-only, findings cite rules, fixes come with tests, measured against a benchmark.
8. **Next steps**: GitHub PR comments, CI trigger, more reviewer types (performance, accessibility). Links.
