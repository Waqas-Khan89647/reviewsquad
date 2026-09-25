# IBM Bob Usage Statement — TEMPLATE

> Replace the [brackets] with what REALLY happened and delete what doesn't apply.
> Keep it under 500 words. Judges compare this with your screenshots.
> You may say openly that the starting code was drafted with another AI assistant
> (the rules allow all LLMs), and describe exactly what Bob did.

## Bob runs the product
ReviewSquad is built as a set of IBM Bob custom modes, so Bob doesn't only help write code:
Bob performs the code review workflow itself.

- **Agent mode + custom modes:** six modes with separate roles and permissions. The Review Lead
  can run commands and start subtasks but cannot edit code. The four reviewers are read-only.
  Only the Fixer can edit, and only after the user approves.
- **Document understanding:** the Review Lead and reviewers read the team's guidelines PDF
  (`team_docs/CornerShop_Code_Review_Guidelines.pdf`) and cite its rule numbers in findings.
  [Example of a finding citing a rule.]
- **Subagents + parallel tasks:** the Review Lead started four reviewer subtasks [at the same time].
  Together they recorded [N] findings: security [n], logic [n], tests [n], team rules [n].
- **Fix and verify loop:** the Fixer [fixed N findings and added N tests]; tests went from
  [8/8 with hidden bugs] to [16/16], and automated warnings from [22] to [0].
- **Result:** [11/11] planted problems caught, versus 7/11 by automated checks alone.

## Bob during development
[List real Bob sessions, for example:]
- [Asked Bob to explain the reviewsquad code and fix an error when ___.]
- [Asked Bob to add a new check / improve the report / write tests for reviewsquad.]
- [Asked Bob to tune the reviewer instructions after it missed ___.]

## Evidence
Bob task session screenshots for every team member are in `bob_screenshots/` and in the submission.

## watsonx
[Not used.]
