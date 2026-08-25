---
name: merge-readiness
description: Use when judging whether a pull request may merge under project.yaml's merge_policy — checks the PR's claimed task against a real VERIFIED status, a matching PASS verification run bound to the PR's exact head commit, mandatory checks satisfied, valid evidence, and no illegal backward state transition in the diff. Invoked headlessly by CI (.github/workflows/sprout-merge-readiness.yml), never by a developer expecting an implementation change.
---

# merge-readiness

## Overview

`artifacts/project.yaml`'s `merge_policy` says a change can merge only when the task is
`VERIFIED`, required evidence exists, required CI checks pass, required approvals exist, and
branch protection passes. Nothing mechanically checked the first three of those against the
*actual PR* until now — a PR could claim a task in its description without the task, the
verification run, and the PR's own commit actually agreeing with each other.

This skill is that check. It runs read-only, judging evidence rather than producing any — the
same independence principle `skills/verify/SKILL.md` applies to implementation vs. verification
applies here to verification vs. merge: the agent that wrote the code must not be the same
judgment that waves it through.

**This is an LLM-judgment gate, not a deterministic one** (unlike
`hooks/check-immutable-artifacts.py` or the CI scripts under `.github/scripts/`, which are
pattern-matching and don't need judgment). That's a deliberate tradeoff, not an oversight: it
avoids a second brittle parser for Sprout's own relational schema, at the cost of being
non-deterministic. Treat a PASS from this skill as informative, not infallible — it does not
replace `skills/verify/SKILL.md`'s own verification run, only checks that one actually happened
and actually matches this PR.

**Announce at start:** "I'm using the merge-readiness skill to judge PR #[N]."

## Steps

1. **Find what this PR claims.** Read the PR description and diff for a referenced task ID
   (`TASK-XXX`). If the diff touches no `TASK-*.md`/`RUN-*.md`/`EVD-*.md`/`APR-*.md` files and the
   PR description names no task, there is nothing to check — record `merge_ready: true`,
   `reasons: ["no Sprout artifacts or task reference in this PR — nothing to verify"]` and stop.
   Do not invent a task reference that isn't actually there.

2. **Resolve the task.** Locate `TASK-XXX.md` on the PR's head commit. If it doesn't exist, or its
   `status` is not `VERIFIED`, fail: `merge_ready: false` with the actual status found.

3. **Resolve the verification run.** Find the `RUN-*.md` the task's evidence trail points to
   (or the most recent one referencing this task ID). Confirm:
   - `verdict: PASS`. Any other verdict (or no run at all) fails.
   - Its `checks:` list is a superset of `artifacts/project.yaml`'s
     `verification_policy.mandatory_checks` (read the actual project profile —
     `.sprout/project.yaml` in a downstream repo, `artifacts/project.yaml`'s shipped defaults
     here). A run missing a mandatory check fails, even with verdict `PASS` — a run that never
     covered `lint` cannot prove a lint-covered merge policy was satisfied, whatever its verdict
     says.
   - Its `commit` field equals the PR's head SHA passed in, or is an ancestor of it on this
     branch (`git merge-base --is-ancestor`). A run captured against a different, earlier, or
     unrelated commit does not prove *this* diff was verified — fail with the SHA mismatch named
     explicitly.

4. **Resolve evidence.** Every check the run lists must have a corresponding `EVD-*.md` it
   references, and that evidence's `redaction_state` must not be `unredacted`. Missing or
   unredacted evidence fails, regardless of the run's own verdict field — the run's self-reported
   verdict is not proof by itself (same principle as `skills/verify/SKILL.md`'s "a required check
   with no corresponding evidence is an automatic FAIL").

5. **Check the diff for illegal artifact transitions.** For any `REQ-*.md`/`DES-*.md`/
   `ADR-*.md`/`DEC-*.md` changed in this PR whose *pre-PR* status was `APPROVED`, `SUPERSEDED`,
   `VERIFIED`, or `ACCEPTED`: the only legal `status` transitions forward from each are
   `APPROVED → SUPERSEDED`, `APPROVED → VERIFIED`, `ACCEPTED → SUPERSEDED`. Any other status
   change on an already-locked artifact (including moving back to `PROPOSED`, `DRAFT`, or any
   earlier state) is illegal regardless of what `hooks/check-immutable-artifacts.py` allowed
   locally — that hook only covers Claude's own Edit/Write tool calls; this step is the actual
   enforcement boundary and must catch a transition made by any tool. A body change alongside a
   status change on a locked artifact is also illegal, even if the status change itself is legal.

6. **Record the verdict.** Emit exactly one structured verdict: `merge_ready` (boolean) and
   `reasons` (array of strings, one per finding — cite the specific file, field, and value, not a
   vague summary). Do not soften a fail into a pass because the surrounding work looks
   well-intentioned; do not fail a PR over something outside this skill's scope (unrelated lint
   warnings, style, code quality — that's other CI jobs' job, not this one).

## Must not

- Treat a plausible-sounding task/run/evidence trail as sufficient without actually resolving
  each reference to a real file with the claimed field values
- Accept a verification run whose `commit` doesn't match (or isn't an ancestor of) the PR head SHA
- Accept a `PASS` verdict that doesn't cover the project's mandatory checks
- Treat this skill's own judgment as a substitute for `skills/verify/SKILL.md` actually having run
- Block a PR that touches no Sprout artifacts — that's scope creep past what `merge_policy` covers
- Produce output in any shape other than the structured `merge_ready`/`reasons` verdict CI parses
