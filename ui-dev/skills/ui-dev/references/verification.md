# Verification

Define success against the approved package before production edits. Use the project's own build,
lint, type-check and test commands; run the focused check as each change lands and the combined
checks at the end.

## The detector

A finding from the hook names the command that records a narrow exception; a `detect` run reports
findings only.

- A real problem: fix it and re-run the check.
- A confident false positive or an approved aesthetic: record the narrowest exception, scoped to the value and the file, with the evidence and the reason, and disclose it. "User confirmed" goes in a reason only when the user did.
- Unsure: leave it visible and ask in one line.

Whole-rule or whole-file suppression needs the user's explicit approval, and an exception is never
added to push a blocked write through. The detector's design-system rules read the design file's
token block, so a value it reports as undeclared is fixed either in the CSS or in DESIGN.md
(design-file.md). Finish with an explicit scan of every changed UI file:
`node "$HOME/.claude/skills/ui-dev/scripts/impeccable.ts" detect <paths>`. The same script runs the
exception commands a finding names (`hooks ignore-value`, `hooks ignore-rule`, `hooks ignore-file`,
`hooks status`). Report a missing binary or a scan fault as a check not performed.

## The design file

`npx -p @google/design.md designmd lint docs/DESIGN.md` after any change to it; `diff` against the
previous version when a direction changes. An error is a blocker.

## Browser evidence

Use a real browser against the running build. Test a narrow phone, a larger phone, a tablet and a
desktop (375, 430, 768 and 1280 CSS pixels are starting points), plus a short landscape viewport
and the widths around each layout change. Compare screenshots with the approved screens.

- Required content, facts, navigation and primary tasks are correct. Exercise long text and realistic item counts, and run `ux-playbook`'s cold test: an empty database, then one request forced to fail at a time, with the rest of the screen still working.
- Every device type preserves the approved direction; touch does not rely on hover. No accidental overflow or clipped text; zoom and reflow work, not only the named breakpoints.
- Keyboard order, visible focus, native semantics and accessible names work. Visible labels over aria-labels; decorative images have empty alt, informative ones a description. Dialog focus enters, stays, closes with the expected controls and returns.
- Contrast: 4.5:1 for text, 3:1 for large text (24px regular, about 18.7px bold), controls, focus indicators and text over imagery. Touch targets 44 by 44 CSS pixels where practical. Report the criteria actually tested.
- Reduced motion is tested: fewer and gentler, no compulsory delay, no scroll trap, nothing unreachable. Test reversing and interrupting motion, resizing, a failed animation, slow and broken images.
- Only the requested themes exist, and each works.
- Images reserve their space and off-screen assets load without delaying the main image. Console errors, network failures and build output are inspected.
- Performance is measured in a stated environment. Lab results do not prove field interaction latency; investigate expensive filters, oversized media and heavy animation bundles.

## The pre-flight

Reported as pass, fail, not applicable or not checked, with evidence. Failed or unrun required checks
stay visible.

- The design read, mode and dials were stated and reasoned from the brief.
- Brand rules, source content, the width route and approved exceptions were honoured.
- Authored copy went through the writing skill; supplied facts, quotations and protected text are unchanged; every visible string was re-read.
- One corner-radius system; elevation declared once; button and form contrast pass; primary labels on one line; one label per intent.
- Fonts suit the brand or were chosen with a stated reason; loaded fonts are the design file's, never a Stitch render's stand-in; licences permit use.
- Every state the state pass named is built, and each `ux-playbook` entry it drew on passes its "How to build it" list.
- Motion: one authored moment; every animation justified in one sentence; `animate`'s rules met; scroll storytelling built to motion.md's skeletons where used.
- The mode file's tells and triage order, where it carries them.
- Approved assets took priority; placeholders are labelled; no placeholder image service in a deliverable.
- Responsive geometry keeps the approved concept, content and functionality, including touch.
- Performance measured and limitations recorded; the detector's final scan clean or its findings disclosed.
- One design system per project.

Fix the required failures, explain legitimate exceptions, and disclose untested conditions.
