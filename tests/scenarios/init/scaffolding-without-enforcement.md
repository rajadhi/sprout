# Scenario: a freshly `init`-ed repo believes it has evidence-gated delivery but doesn't

**Tests:** `skills/init/SKILL.md` — step 9, enforcement installation.
**Failure mode being prevented:** the exact gap the original external review named — "`init` does
not install enforcement into downstream repositories; projects must wire their own CI. So
'evidence-gated delivery' is not yet a system property." A team runs `/sprout:init`, sees
`.sprout/project.yaml`'s `merge_policy` declared, and reasonably assumes that policy is now
enforced — when in fact nothing in the newly-scaffolded repo checks a PR against it at all.

## Input

A brand-new repository, no prior Sprout state. The team runs `/sprout:init`, answers the setup
questions, and immediately opens a PR claiming a task is `VERIFIED` with no real verification run
behind it — to see whether anything catches it.

## Correct behavior

- `init` must not silently leave enforcement entirely to convention. Step 9 requires it to
  *offer* copying `check_merge_readiness.py` into `.github/scripts/` plus the CI job that runs it,
  and point at the GitHub-native settings checklist (branch protection, R3/R4 environment, secret
  scanning) as explicit follow-up steps — not implied, not left for the team to discover only
  after a bad merge.
- If the team declines the offer, step 10 requires the report to say so explicitly ("merge
  readiness check install: declined") rather than reporting scaffolding success as if enforcement
  were now in place. A silent report that only lists artifact directories would leave the team
  believing more was enforced than actually was.

## Walkthrough against current skill

**Gap found (pre-fix).** The skill as written before this change stopped at "establish artifact
directories" and "establish GitHub conventions" (labels) — no step ever mentioned that
`merge_policy` needs a CI workflow to mean anything, and step 9 (now step 10)'s report requirement
didn't distinguish "structure created" from "enforcement wired." A team following the skill
literally would get exactly the false assurance the review described.

**Fix applied.** New step 9 makes the offer explicit and requires asking before writing into
`.github/`; the report step (now step 10) requires stating which offers were accepted or declined,
so "I ran init" can no longer be silently read as "merge_policy is now enforced."

## Verdict

**RED → GREEN.** `skills/init/SKILL.md` now surfaces the enforcement gap as something to actively
resolve or explicitly decline, rather than leaving it invisible until a team discovers it the hard
way.
