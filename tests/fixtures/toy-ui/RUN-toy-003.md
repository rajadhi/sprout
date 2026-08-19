---
id: RUN-toy-003
task: none — see EVD-toy-003.md and README.md
commit: n/a
branch_pr: n/a
environment: "Claude Code Browser pane"
tool_versions: {}

checks:
  - name: visual
    result: PASS
  - name: review
    result: PASS

evidence: [EVD-toy-003]

verdict: PASS
failure_class: null

started_at: "2026-08-19T00:00:00"
finished_at: "2026-08-19T00:02:00"
---

## Verifier reasoning

This is a mechanism proof, not a task verification — there is no acceptance criterion to read
because no task claims this evidence. What's being verified is narrower: does Sprout's
computer-use/runtime-verification workflow (`docs/architecture.md` §9: navigate → interact →
capture evidence → assert expected state) actually execute against a real rendered page using
tools available in this session, or does it only exist as prose?

Confirmed real: navigation, screenshot, DOM text assertion, accessible-name assertion, real click,
console-error check. All six actually ran; none were described without being executed.

**Verdict: PASS** — the mechanism works. See README.md for what this explicitly does not prove.
