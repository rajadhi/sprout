# Scenario: unattended run's outcome note targets a directory init never creates

**Tests:** `skills/develop-all-unattended/SKILL.md` — "Outcome note" section, path correctness.
**Failure mode being prevented:** an unattended overnight run finishes, tries to write its outcome
note to `artifacts/runs/<timestamp>-develop-all-unattended.md`, and either fails outright (no
`artifacts/` directory exists in a downstream repo — `skills/init/SKILL.md` step 5 never creates
one; it creates `.sprout/{approvals,state,graph,runs}/` and separate top-level
`requirements/ designs/ ...` directories instead) or, worse, silently creates a stray
`artifacts/runs/` directory that nothing else in the project ever looks at — a report nobody would
ever find, from a run meant to be checked by a human the next morning.

## Input

A downstream repo, freshly `init`-ed, no manual directory changes made. `/sprout:develop-all-unattended`
runs overnight and reaches its outcome-note step.

## Correct behavior

- The outcome note must land in a directory that actually exists after `init`, per
  `skills/init/SKILL.md` step 5 — `.sprout/runs/`, not `artifacts/runs/`.
- A human checking the next morning must be able to find the report using the paths `init`
  actually documents, not a path that only exists in the skill's own (previously incorrect) text.

## Walkthrough against current skill

**Gap found (pre-fix).** The skill's "Outcome note" section named `artifacts/runs/...` while
`init`'s step 5 only ever creates `.sprout/{approvals,state,graph,runs}/` — a real path
contradiction between two skills that would produce divergent behavior depending on which an
agent trusted, exactly the class of bug the original external review flagged under "lifecycle and
path contradictions."

**Fix applied.** The outcome-note path now reads `.sprout/runs/...`, with an explicit
cross-reference to `skills/init/SKILL.md` step 5 so the two skills can't silently drift apart
again without the reference itself going stale and visible.

## Verdict

**RED → GREEN.** The path now matches what `init` actually creates; an unattended run's report is
findable where the rest of `.sprout/` state already lives.
