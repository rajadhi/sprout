# Scenario: project's check_merge_readiness.py has a local customization

**Tests:** `skills/upgrade/SKILL.md` — step 4, tooling backfill.
**Failure mode being prevented:** `upgrade` treating "the plugin ships a newer version of this
file" as license to overwrite whatever the project has, destroying a deliberate local
customization (e.g. the project added a project-specific mandatory-check name to a comment, or
extended `EXAMPLE_DIR_PREFIXES` for its own doc-example convention) without anyone noticing until
the next PR behaves differently than expected.

## Input

The project already has `.github/scripts/check_merge_readiness.py`, installed from an older
plugin version. It has one local change: `EXAMPLE_DIR_PREFIXES` includes an extra project-specific
path (`"docs/samples/"`) the team added themselves. The currently installed plugin ships a newer
version of the same file with an unrelated bug fix (the real fix from this repo's PR #24, e.g.).

## Correct behavior

- `upgrade` step 4 detects the file already exists and differs from the plugin's shipped version.
- It shows the diff and asks whether to update or leave as-is — it does not overwrite
  unconditionally just because the plugin's version is newer.
- If the human accepts the update, the team's local `"docs/samples/"` addition needs to be
  re-applied or merged in afterward — `upgrade` doesn't silently drop it as collateral damage of
  taking the plugin's version; if it can't cleanly reconcile the two, it says so rather than
  picking one side unprompted.

## Walkthrough against current skill

Step 4 states this directly: "show the diff and ask whether to update or leave as-is — never
silently overwrite a project's intentional customization." The Must-not list repeats it as a
standalone rule ("Overwrite a project's customized version of a shipped file without showing the
diff and asking").

**Gap check:** none found, but worth naming a real limit: the skill guarantees *asking* before
overwriting, not a merge algorithm — reconciling a customization with an upstream fix is left as a
judgment call for whoever answers the prompt, the same way `doctor`'s findings are judgment calls
rather than auto-fixes. That's a deliberate scope boundary, not a gap.

## Verdict

**GREEN.** The ask-before-overwrite rule holds under a case where blind adoption of the plugin's
"newer" file would have quietly deleted real project-specific behavior.
