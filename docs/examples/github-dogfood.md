# M4 dogfood: real branch protection + real issue mechanics

Unlike the Ambient Journal fixture (markdown artifacts, simulated where full execution wasn't in
scope) and the toy-app fixture (real code, no live GitHub), this is Sprout's actual repository on
GitHub. Applied with explicit scope approval before touching any live setting.

## Branch protection (applied to `main`, github.com/rajadhi/sprout)

```
required_status_checks: {strict: true, contexts: [validate-structure, toy-app-tests, hook-tests,
                                                    risk-approval-check]}
required_pull_request_reviews: {required_approving_review_count: 0}
enforce_admins: false
allow_force_pushes: false
allow_deletions: false
required_conversation_resolution: true
```

(`hook-tests` and `risk-approval-check` were added after the immutability hook and the R3/R4
approval gate landed — this reflects the current ruleset, not the original M4 pass; see below.)

Matches `docs/architecture.md` §7's minimum recommended ruleset: required PR, required CI status
checks, no force-push, no deletion, required conversation resolution. `enforce_admins: false` and
`required_approving_review_count: 0` are a deliberate choice for a solo-maintainer repo — a PR is
still required to merge, but the owner isn't blocked waiting on a second approver that doesn't
exist. `enforce_admins: true` and a non-zero review count are the natural next step once there's
more than one maintainer.

**The review-count-0 gap is closed for R3/R4 specifically**, without needing a second maintainer:
`risk-approval-check` (`.github/scripts/check_risk_approval.py`) is a required status check that
fails CI if any task claims `risk: R3`/`R4` without a real `APR-*.md` approval record naming it.
This doesn't replace human judgment (a human still writes the approval), but it does mean the
*absence* of one is now caught by GitHub, not just by convention.

This is the real enforcement mechanism behind M4's exit criterion: an unverified task cannot merge
through the normal GitHub path, because merging now requires the two CI status checks to pass —
Sprout can document that a task should be `VERIFIED` before merging, but it's GitHub's branch
protection, not any Sprout skill, that actually blocks it.

## Issue mechanics ([issue #1](https://github.com/rajadhi/sprout/issues/1), closed)

Proved `plan`'s step 10 (`skills/plan/SKILL.md`) and `docs/architecture.md` §7's label mechanics
for real, in order:

1. `gh label create --force` — idempotent creation of `sprout:type:engineering`,
   `sprout:state:ready`, `sprout:risk:R0`, `sprout:size:XS`.
2. `gh issue create` with those labels and a body pointing back to a (nonexistent, since this was
   a throwaway) canonical task artifact — not a copy of task content, per the "issue is a
   pointer, not the content" rule.
3. `gh issue edit --add-label sprout:state:verified --remove-label sprout:state:ready` — the state
   transition mechanism, confirmed to add/remove rather than close-and-recreate.
4. `gh issue close --comment "..."` — closed with an explanation, not deleted (deletion isn't
   available via the mechanics Sprout uses, and closing is the correct reversible action anyway).

## What this proves for M4

- Branch protection is real, not documented-only — `git push` directly to `main` would now be
  rejected for anyone other than the repo owner without CI passing and without a PR (see
  `enforce_admins: false` caveat above for why the owner specifically can still push directly;
  that's a known, deliberate gap for a solo-maintainer repo, not an oversight).
- The label taxonomy in `docs/architecture.md` §7 produces real, correctly colored, correctly
  described GitHub labels when created via the documented commands — not just plausible-looking
  YAML.
- The "never close-and-recreate, always add/remove labels" rule from `plan`'s Must-not list holds
  under real API calls, not just as a written constraint.
