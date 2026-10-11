# Workflow

## Terms

These are this skill's working words. To the person, say each in plain words: SKILL.md has the table
("Words for the person").

- **Design file**: `docs/DESIGN.md`, the brand's visual identity and the project's design system in Google's open DESIGN.md format: exact values, reasons, logos and motion, written from the brand's guidelines and evolving with the built world (design-file.md).
- **Brand folder**: `docs/brand/` beside it, holding what the format has no place for: TONE-OF-VOICE.md, the asset files and the sources (brands.md).
- **Direction**: the project-specific composition, typography, palette, hierarchy and interaction intent for a surface.
- **Approved package**: the chosen Stitch screens, one per device type the surface needs, a motion storyboard where narrative motion is in scope, and the design file updated to match. The approved package is authoritative for the build.

## At every gate and every hand-off to an outside tool, say

What is ready (with the preview, file or project link); what the user must decide or do, as
numbered steps naming the tool and the screens; the recommendation and its consequence; what to
return (a selection, a screen id, a confirmation); and what happens next and whether the agent is
waiting. "Please confirm" and "review the design" are not instructions. Silence, a successful
import and a rendered preview are not approval.

If a task is possible through available tools, do it rather than assigning it. If login, visual
judgement or an unavailable tool needs a person, state the exact blocker and the shortest steps.
Read the current interface rather than inventing button names.

## 1. Discover

Read the request, the project's instructions, existing design documentation, framework and
dependencies. Identify the audience, the task, the required content and the scope: a new direction,
a material redesign, or a targeted change. Inspect an existing surface before proposing changes and
preserve its routes, behaviour, data and accessibility unless the request changes them.

Resolve the brand with brands.md. If no brand folder exists, ask what the user wants: onboard a brand
into one, or proceed without one. State the design read in plain words (SKILL.md has the line) and
load the mode's reference. Ask which device types the surface needs; never presume. List the `ux-playbook` situations each
screen meets, the state inventory: every screen on an operate surface, and on any other surface each
screen that fetches data, submits something or asks the person to choose. The inventory shapes the
questions and goes in the brief's inputs, never in a generation prompt, because Stitch draws only
the working state. Then invoke both `grilling` and `domain-modeling`, as two `Skill` calls in the
same message and never one without the other (the pair
`/grill-with-docs` runs), always, with the brief, the findings, the brand constraints and the open
decisions, and follow its rounds until the frontier is empty, writing each settled decision as a
record as it lands; the user leads the decisions. If `grilling` is not installed, say so once and ask the same way. For a
targeted change inside an approved direction, skip the gates below and Stitch, and apply only the
relevant rules.

**Complete when** scope, brand or explicit no-brand choice, content constraints, the mode, the dials
the device types and the state inventory are clear, and for a new direction the decision frontier
is empty.

## 2. Direction: first gate

For a new direction, register the design system in Stitch, then generate the first screens for each
device type and up to five variants at the reimagine range, so the choice is between rendered
directions (stitch.md). Present them with a recommendation and ask the user to select or revise
one. Selecting a direction authorises exploration, not the production build.

**Complete when** the user has selected a direction.

When the user rules Stitch out, the first gate presents two or three concepts in words, each with
its composition per device type, its focal idea and its trade-off, and the second gate is the built
surface verified in a browser; the approved package is then the build itself.

## 3. Render and approve: second gate

Follow stitch.md's route, one surface at a time and one subscreen at a time within it: the agent
iterates a subscreen in Stitch until it is about eighty per cent there, hands it over with a short
list of what is worth looking at, waits for the user to iterate in Stitch and say it is done, then
fetches their version and draws the next subscreen from it. A Stitch screen is looked at only
through Stitch's own tools, never a browser.

Then the state pass. Walk each fetched screen through its state inventory, infer what the working
state leaves out, and put the gaps to the user as one round, each with a recommendation ("the
projects list can be empty on first run: one sentence on what goes here and one Create action, or
hide the section?"). A state that changes the layout, such as a first-run screen, a full-page error
or a payment confirmation, is proposed as a screen of its own; the ones the user chooses are
generated in Stitch, so they are seen there before build.

The outcome is a rendering per device type, a motion
storyboard where narrative motion is in scope (motion.md), and the design file updated with the
resolved tokens, the supported themes, the responsive rules and the open limitations. Offer Stitch's
prototype view for checking hover states and input sizing before build; a runnable prototype (the
`prototype` skill) only when the open question is how an interaction feels.

Show the rendered direction, its interaction intent and its limitations, name the screens to
inspect, and ask for approval of an identifiable version.

**Complete when** the user approves a named version and any issue that affects the build is
answered or explicitly deferred.

## 4. Implement

Read verification.md and define the checks before changing code. Reuse the current stack,
components, semantic HTML, native CSS and installed dependencies; add a library only when the
approved behaviour needs it. Keep the raw export unchanged in the evidence folder and translate the
design into the project's own code, extracting tokens and components only where they carry real
shared meaning. Motion is written by `animate`. States are built where they belong, to their
`ux-playbook` entries: a component that fetches owns its loading, empty, error and success states,
and a section that fetches separately gets its own failure boundary and retry. Protected text and facts are never edited for fit;
use layout or progressive disclosure instead.

Work in small coherent changes, each with its focused check, following the project's own commit
policy.

## 5. Verify and deliver

Follow verification.md against the running build and the approved package. Report the implemented
scope, the exact checks and results, where the evidence is, and what remains failing or untested.
Start the project's development server only when useful to the review, on its documented command.
