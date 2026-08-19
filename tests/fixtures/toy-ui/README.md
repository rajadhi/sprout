# toy-ui — real runtime/computer-use verification mechanism proof

Same spirit as `tests/fixtures/toy-app` (real TDD, not simulated) applied to
`docs/architecture.md` §9's computer-use/runtime verification policy: this proves the mechanism
executes for real, using a real browser tool against a real rendered page, rather than leaving it
as unproven prose.

`empty-state.html` renders `docs/examples/ambient-journal/DES-001-v1.md`'s Empty state exactly as
specified — real markup, real CSS, no framework. `RUN-toy-003.md`/`EVD-toy-003.md` record a real
Browser-pane session against it: navigate, screenshot, assert exact text content, assert
accessible name, click, assert no console errors.

## What this does and does not prove

**Proves:** the navigate → interact → capture evidence → assert expected state loop
(`docs/architecture.md` §9) is executable, not just described, using tools actually available in
a Claude Code session — real DOM assertions, a real click, a real console check, all logged.

**Does not prove:** any specific Ambient Journal task is verified. `TASK-004` ("display empty
state") targets **native iOS/macOS**, per `docs/examples/ambient-journal/project.yaml`'s
`platforms: [macOS, iOS]` — this fixture is a **web** page. A screenshot of a web mockup of the
same copy is not evidence that a native SwiftUI view renders correctly; different rendering
engine, different accessibility tree, different platform conventions
(`docs/architecture.md` §9 already says computer-use is for native macOS/iOS testing via the iOS
Simulator, browser tools are the *web* path — this fixture deliberately used the browser path
because it's the lower-friction real tool available, not because it's the right one for Ambient
Journal specifically). `TASK-004.md` is **not** updated to claim this evidence — doing so would
misrepresent what was actually checked. Real native verification (build a minimal SwiftUI view,
run it in the iOS Simulator via `mcp__Claude_Code_iOS_Simulator__control`, screenshot, assert) is
possible in a session with those tools but is a materially larger effort (an Xcode project, a
build step) than this proof needed to establish that the mechanism itself works — left as an
explicit next step, not faked by substituting a web mockup for it.

## Also honest about the evidence gap this surfaced

`EVD-toy-003.md` documents a real screenshot that was visually confirmed but whose binary image
is **not** persisted to this repo — no tool available in this session writes a Browser-pane
screenshot to disk as a file. The evidence record relies on DOM-level assertions (exact text,
accessible name, console state) plus a precise description of what was seen, not a stored PNG.
`docs/protocol.md`'s evidence model (§33-34) assumes screenshots are storable artifacts;
`SCREENSHOT` as a real persisted file is a real capability gap in this session's toolset, not a
Sprout design flaw — worth knowing about, not worth pretending around.
