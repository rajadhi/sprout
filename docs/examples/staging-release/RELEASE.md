# Dogfood: `/sprout:release` against a simulated staging release

Two synthetic release candidates, real artifact files actually produced by walking
`skills/release/SKILL.md`'s steps — not a narrative of what would happen. `production_approval_policy`
is `unknown` by default in the shipped `artifacts/project.yaml`; both candidates here set it
explicitly, per `init`'s instruction to fill in genuinely unresolved policy fields rather than
leave them `unknown` once a project has an actual policy.

Staging deployment itself is simulated (`docs/protocol.md` §10: Sprout doesn't own or replace a
project's real deployment mechanism) — `EVD-00201`'s content describes what a real staging smoke
test would show, the same "simulated where full execution wasn't in scope" treatment
`docs/examples/ambient-journal/README.md` uses for the parts of that example a markdown fixture
can't literally execute.

## RC-001: the `human_required` path (this directory)

`project.yaml`: `production_approval_policy: human_required`. Candidate: `TASK-200` (R1, MERGED,
`RUN-00200` verdict `PASS`).

Walkthrough against `skills/release/SKILL.md`:

1. Confirm every task is `MERGED` with a `VERIFIED`-strength verdict — `TASK-200`/`RUN-00200`:
   `PASS`. ✓ See `TASK-200.md`, `RUN-00200.md`, `EVD-00200.md`.
2. Tag the release candidate — `RELEASE-CANDIDATE-001.md`, recording exactly which
   commit/task it contains.
3. Deploy to staging — `EVD-00201.md` (`type: DEPLOYMENT_RECORD`, `environment: staging`).
4. Run staging verification — same record, smoke-test result captured as evidence the way
   `verify` captures evidence (`skills/verify/SKILL.md`'s evidence-sufficiency bar applied here
   too: specific, checkable behavior described — cache-hit then cache-miss — not "looked fine").
5. `production_approval_policy` is `human_required` → stop, present the candidate for approval.
   `APR-00200.md`: `decision: approved`, naming exactly what was reviewed (RC-001's contents and
   the staging evidence).
6. Transition to `RELEASED` — `TASK-200.md`'s `status` is `RELEASED` (compare to
   `docs/examples/schema-migration/before/TASK-100.md`'s `MERGED` for what pre-release looks
   like). `RELEASE-001.md` records which task, which commit, under what approval.
7. Report: released `TASK-200` (commit `3e7bd41`) under `APR-00200`'s human approval.

**Gap check:** none found — every step, applied literally, produces the files in this directory.

## RC-002: the risk-ceiling override (`policy-variant/`)

The subtler rule, and the one worth actually testing rather than trusting the skill text alone:
step 5 says an *autonomous* `production_approval_policy` doesn't mean every task in the candidate
gets released without a human — only tasks at or below the policy's stated risk ceiling do.

`policy-variant/project.yaml`: `production_approval_policy: autonomous_with_R0_R1_only`.
Candidate: `TASK-201` (**R2**, MERGED, `RUN-00201` verdict `PASS`).

Walkthrough:

1-4. Same shape as RC-001 — `TASK-201`/`RUN-00201` verified, candidate tagged
   (`RELEASE-CANDIDATE-002.md`).
5. `production_approval_policy` is autonomous, *not* `human_required` — but `TASK-201` is R2,
   above the policy's stated `R0_R1_only` ceiling. Step 5 is explicit: "otherwise stop and
   require human approval anyway, regardless of the general policy setting." No `APR-*.md`
   exists in `policy-variant/` — release stops here.
6-7. Not reached. No `RELEASE-*.md` in `policy-variant/`, because nothing was released.
   `RELEASE-CANDIDATE-002.md`'s own status field (`BLOCKED_AWAITING_APPROVAL`) is the honest
   record of where this candidate actually sits.

**Gap check:** none found. This is the case worth having dogfooded specifically — a policy field
named "autonomous" is exactly the kind of thing an agent under time pressure could read as
blanket permission; the skill's own text already forecloses that reading, and applying it for
real to an R2 task inside an ostensibly-autonomous policy produces the correct stop rather than a
rationalized release.

## Verdict

**GREEN** on both candidates. `release`'s steps, walked for real against two different policy
shapes, produce a completed release with a genuine human-approval record in the ordinary case,
and a correctly-blocked candidate — not a silent autonomous release — in the case designed to
tempt the wrong shortcut.
