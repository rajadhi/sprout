<!-- Plain markdown, not a governed artifact type -- see RELEASE-CANDIDATE-001.md in the parent
     directory for why. -->

# Release candidate RC-002

status: BLOCKED_AWAITING_APPROVAL

Contains:
  - TASK-201 (commit c88a4f2, verdict PASS, RUN-00201, risk R2)

Tagged: 2026-02-06T09:00:00Z

Blocked: production_approval_policy is `autonomous_with_R0_R1_only`, but TASK-201 is R2 --
above the policy's stated ceiling. Per skills/release/SKILL.md step 5, this candidate requires
explicit human approval regardless of the general autonomous policy setting. No APR-*.md exists
yet for this candidate -- release stops here, exactly as it should, rather than treating the
policy's general "autonomous" framing as license to release an above-ceiling task on its own.
