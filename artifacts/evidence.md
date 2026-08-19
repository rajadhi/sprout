---
id: EVD-XXXXXX
type: unknown        # SCREENSHOT | VIDEO | INTERACTION_TRANSCRIPT | API_REQUEST |
                      # API_RESPONSE | DATABASE_ASSERTION | UNIT_TEST_RESULT |
                      # INTEGRATION_TEST_RESULT | BUILD_RESULT | DEPLOYMENT_RECORD |
                      # ACCESSIBILITY_REPORT | VISUAL_COMPARISON | LOG |
                      # CODE_REVIEW | SECURITY_RESULT
verification_run: RUN-XXXXXX
task: TASK-XXX
commit: unknown
environment: unknown
timestamp: unknown
source: unknown        # tool/agent that produced this
description: unknown
redaction_state: unredacted   # unredacted | redacted | not_applicable
---

<!--
Immutable once captured. Must prove the acceptance criterion, not just be
adjacent to it — "HTTP 200" alone is not proof of a semantic API requirement;
pair it with schema validation + required fields + persisted state.

Always redact before storing: api_keys, bearer_tokens, cookies, passwords,
credentials, unnecessary personal data. Never trade privacy for auditability.
-->

## Content
