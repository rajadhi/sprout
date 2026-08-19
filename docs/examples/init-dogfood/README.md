# init dogfood — a real fresh downstream repo

Everything so far (`docs/examples/ambient-journal`) exercised `shape`/`design`/`plan`/
`develop-next`/`verify` inside Sprout's own repo, against a fixture. `init` never actually ran
against what it's meant for: a brand-new, genuinely separate project repository that doesn't
already have Sprout's own docs sitting next to it.

This ran for real, on disk (path intentionally outside this repo — a real separate `git init`,
not a subdirectory here): a fresh repo called `recipe-box`, one pre-existing commit (a plain
README, no Sprout awareness at all), then `init`'s actual steps applied against it.

## What actually happened, in order

1. **Detect repo state** — existing repo (one commit), no `.sprout/` present. Not previously
   initialized. Proceed.
2. **Inspect the repository** — read the only file that existed: `README.md`
   ([copy: pre-existing-README.md](pre-existing-README.md)). Learned the project is about saving
   and organizing family recipes, "very early." No package manifest, no CI config to infer a
   stack from.
3. **Ask only for genuinely unresolved context** — simulated the interview `init` would run.
   Answered what a real early-stage note would plausibly answer; explicitly left several fields
   `unknown` rather than guessing, per `init`'s own "must not invent" rule:
   - `platforms: [web]`, `accessibility_target: "WCAG 2.2 AA"` — stated
   - `technology_stack`, `repository`, `deployment_environments`, `testing_approach`,
     `security_privacy_constraints` — left `unknown`, genuinely undecided this early
4. **Create the project profile** — [.sprout/project.yaml](project.yaml), copied from this
   plugin's `artifacts/project.yaml`, filled with the above. Policy sections kept at shipped
   defaults — nothing surfaced a reason to override them for a small personal project.
5. **Establish artifact directories** — `.sprout/{approvals,state,graph,runs}/` and
   `thoughts/ requirements/ designs/ architecture/ tasks/ verification/ evidence/` at the repo
   root, per `skills/init/SKILL.md` step 5.
6. **Establish project-specific Claude instructions** — [CLAUDE.md](CLAUDE.md) created (didn't
   exist before), pointing at `.sprout/`/the artifact tree as canonical and naming the two
   commands most relevant to get started.
7. **Establish GitHub conventions** — **not done**, and said so rather than faking it:
   `repository:` is `unknown` because `recipe-box` has no GitHub remote yet. There's nothing to
   apply `sprout:*` labels or branch protection to. This is the correct behavior, not a gap —
   `init` must not invent a remote that doesn't exist.
8. **Establish verification configuration** — also deferred honestly: `technology_stack` is
   unknown, so there's no real toolchain to detect checks against yet. Noted in `project.yaml`
   as a comment rather than guessed at.
9. **Establish initial graph state** — `.sprout/graph/` created, empty (no artifacts exist yet
   for it to index).
10. **Report exactly what was created** — this document, plus the real commit in the downstream
    repo: [git-log.txt](git-log.txt), [final-tree.txt](final-tree.txt).

Then committed for real in the downstream repo (`git commit -m "sprout init: bootstrap project
profile and artifact directories"`) — a real commit exists, this isn't a description of one.

## What this proves

- `init` genuinely adapts to what's actually knowable from a real, mostly-empty repo — it didn't
  wait for a fully-specified project to run, and it didn't invent a stack, a deployment target, or
  a GitHub remote to fill gaps. Multiple fields are legitimately `unknown` in the resulting
  `project.yaml`, which is the correct output here, not an incomplete one.
- `init`'s "must not overwrite existing project artifacts" held: `README.md`'s original content is
  untouched (compare [pre-existing-README.md](pre-existing-README.md) — identical to what's still
  in the downstream repo).
- The framework is genuinely project-agnostic (`docs/protocol.md` §10 non-goals: no mandatory
  stack) — `recipe-box` shares nothing with Ambient Journal (different domain, different
  platforms, no backend chosen at all) and `init` handled it the same way.
