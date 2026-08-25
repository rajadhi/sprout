# Scenario: PR diff flips an approved artifact's status backward, then edits the body

**Tests:** `skills/merge-readiness/SKILL.md` — step 5, illegal transition detection.
**Failure mode being prevented:** the original external review reproduced this exact sequence
against `hooks/check-immutable-artifacts.py` — change `status: APPROVED` to `status: PROPOSED`
(allowed, since `status` is in `ALLOWED_FIELDS`), then rewrite the now-"unlocked" body (allowed,
since the current on-disk status no longer reads as locked). The hook only watches Claude's own
Edit/Write calls, so any other tool — Bash, a script, a different editor, Codex's `apply_patch` —
bypasses it entirely. This scenario checks whether the CI-facing skill, which reads the *diff*
rather than intercepting a live tool call, catches the same sequence regardless of which tool
produced it.

## Input

`REQ-007.md`'s state on `main` (the PR's base): `status: APPROVED`. The PR's diff changes it to
`status: PROPOSED` in one hunk and rewrites two paragraphs of the requirement body in the same
file. The PR was made entirely via `git apply` in a script, never through Claude Code's Edit/Write
tools — the local hook never ran at all.

## Correct behavior

- `REQ-007`'s pre-PR status (`APPROVED`, read from the base commit, not the PR's proposed content)
  is a locked state. `APPROVED → PROPOSED` is not one of the legal forward transitions
  (`APPROVED → SUPERSEDED`, `APPROVED → VERIFIED`) — illegal regardless of which tool produced the
  diff, since this check reads the diff itself rather than intercepting a tool call.
- The accompanying body rewrite is illegal on its own terms too, independent of the status
  question — step 5 explicitly says a body change alongside a status change on a locked artifact
  is illegal "even if the status change itself is legal."
- `merge_ready: false`, citing both the illegal transition and the body rewrite as separate
  reasons — not collapsed into one vague "artifact was modified improperly."

## Walkthrough against current skill

Step 5 defines the legal-transition table explicitly, states plainly that this check must catch a
transition "made by any tool" (naming the hook's bypass directly as the reason it can't be trusted
alone), and separately forbids a body change on a locked artifact even under a legal status
change. Applied to this diff: the base commit's `status: APPROVED` is resolved independent of the
PR's proposed edit, `APPROVED → PROPOSED` isn't in the legal set, and the body diff is flagged
separately.

**Gap check:** none found — step 5, read literally, catches this transition. The load-bearing part
is that step 5 explicitly reads the *pre-PR* status from the base commit rather than trusting
whatever the PR's own diff claims the "current" status is — the whole failure mode ceases to be a
gap the moment that ordering is fixed.

## Verdict

**GREEN.** Directly closes the bypass the original review demonstrated: enforcement now lives in
a CI-facing diff check that isn't tied to which tool produced the change, rather than solely in a
locally-scoped hook.
