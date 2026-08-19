---
name: graph
description: Use when inspecting relationships for a requirement/task/design node, or analysing the downstream impact of a change — parses artifact metadata directly, no database required
---

# graph

## Overview

Queries the artifact graph — the typed metadata relationships (`implements:`, `design:`,
`architecture:`, `supersedes:`, ...) embedded directly in `artifacts/*` files. This is a static
data model for provenance and impact analysis, not a runtime execution graph — see
`docs/protocol.md` §3 for why Sprout deliberately doesn't route agent execution through it.

**Announce at start:** "I'm using the graph skill to inspect [NODE-ID]."

## Relationship query

Given a node ID (e.g. `TASK-071`), explain its upstream and downstream relationships by parsing
frontmatter across the artifact tree — no database, no index required for v1.

Given a requirement (e.g. `REQ-024-v2`), show: source intent, previous requirement version,
current design, architecture (ADRs), tasks, tests, verification runs, released versions.

## Impact analysis (folds in what the original brief called `impact`)

Given a changed node (typically a new requirement version), traverse the graph and classify every
downstream node as:
```
INVALIDATED       NEEDS_REVIEW       LIKELY_UNAFFECTED       UNAFFECTED
```
Use semantic judgment, not blanket invalidation — do not mark everything downstream
`INVALIDATED` just because an upstream requirement changed. Report affected designs, ADRs, tasks,
tests, implementations, evidence, and releases separately.

## Must not

- Require a graph database or index for v1
- Auto-invalidate all downstream nodes without semantic review
- Be used as a runtime router for agent execution
