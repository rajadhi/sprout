---
id: RUN-XXXXXX
task: TASK-XXX
commit: unknown
branch_pr: unknown
environment: unknown
tool_versions: {}

checks:
  # - name: unit
  #   result: PASS | FAIL
  -

evidence: []                  # evidence IDs produced by this run

verdict: unknown              # PASS | FAIL
failure_class: null            # SPEC_ERROR | DESIGN_ERROR | IMPLEMENTATION_ERROR |
                               # TEST_ERROR | ENVIRONMENT_ERROR | DEPENDENCY_ERROR |
                               # UX_ERROR | ACCESSIBILITY_ERROR | SECURITY_ERROR |
                               # ARCHITECTURE_ERROR | DATA_ERROR | UNKNOWN

started_at: unknown
finished_at: unknown
---

<!--
Immutable once recorded. A later run against the same task creates the next
RUN-XXXXXX — never overwrite. This is what makes intermittent failures
diagnosable: the history of runs, not just the latest one.

Independence: the verifier agent that produces this run must read the
requirement and acceptance criteria directly, not rely solely on the
implementation agent's summary.
-->
