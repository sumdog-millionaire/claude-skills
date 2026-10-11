# Operate

Read when the design read picks operate: app UI, dashboards, editors, admin, settings, tools, data
tables, authenticated surfaces, anything where the person is in a task. Familiarity is a feature.
Avoid strangeness without purpose: over-decorated buttons, mismatched controls, gratuitous motion,
display fonts where labels should be, invented affordances for standard tasks.

How components behave is `ux-playbook`'s: loading, empty, error and success states, sections that
fail on their own, button states, forms, control placement, how many choices a screen asks for, and
what waits behind a click. This file adds the operate rules around it.

## Space

- Measure the element, never the window.
- Predictable structure, stable density and navigable linearity are affordances. Standard navigation patterns belong here: top bar plus side navigation, breadcrumbs, tabs, a command palette.
- Density is permitted: tables with many rows, panels with many labels, dense information when the task needs it. Data and compact UI can run denser than prose; a table at 120 characters wide is fine.
- Responsive behaviour is structural (collapse the sidebar, reflow the table, change the column count), not fluid typography. At desktop: side navigation visible, several panels at once, hover for additional information, keyboard shortcuts, context menus, drag and drop where it helps, multi-select with modifier keys.
- Repetition supports recognition; break it only when content or priority changes. Related items sit close and distinct groups sit apart, so containers are not compensating for weak proximity.
- Overlays escape their container: a dropdown positioned inside an ancestor with overflow hidden gets clipped, so reach for `<dialog>`, the popover API, `position: fixed`, or a portal.

## Type and colour

- One family is often right; a well-tuned sans carries headings, buttons, labels, body and data. A fixed rem scale with a tighter ratio (1.125 to 1.2 between steps), never fluid headings that shrink inside a sidebar.
- Colour defaults to restrained. Accent for primary actions, current selection and state indicators; a second neutral layer for sidebars, toolbars and panels. Inactive states never carry heavy or full-saturation colour.

## Labels, copy and tooltips

- Labels are factual, and every word earns its place. A title says what the thing is, plainly; an extra word stays only when it changes the meaning ("Your compass": yours, not the project's) and goes when it is only warmth ("Today's use" becomes "Usage"). Whatever fact the label needed that word for goes under it, smaller, as a clarification ("Resets at 00:00 UTC").
- Every control explains itself on hover. A list row is one line; its detail is the tooltip; the list's mechanics are said once on its header. On a touch surface the same detail is reachable by a press or an expanded row; when the surface is also the phone, which of those is a question for the round.
- Say a thing once per surface, where it is first met and seen on arrival, not at the end of a scroll or below a fold. Repeat only what answers "what do I do next?" or "what is this?". A page that lists many of the same thing carries the line once, for the page, not under every row.
- Actions use a specific verb and object when the outcome is not obvious; the same noun and verb for the same concept everywhere. A destructive action names the object and the consequence; prefer undo to confirmation when recovery is safe, and when confirmation is necessary the button names the action rather than "Yes", "OK" or "Submit".

## States

- Visible keyboard focus, logical tab order, labels, and platform-sized touch targets on every control.
- Loading is separate for the initial load, pagination and refresh. Large datasets paginate or virtualise.
- A permission state shows what is unavailable and why, not a blank.

## Cognitive load

- Single focus: the primary task completes without competing elements.
- Working memory: the current screen never needs a fact remembered from a previous one.
- Match neighbouring mental models: terminology, disclosure, routing, save behaviour, optimistic or pessimistic patterns, all the same screen to screen.

## Motion and delight

Motion conveys state, feedback, loading and reveal; routine transitions stay fast and there is no
page-load choreography. A control used a hundred times a day gets none. Delight concentrates at the
meaningful moments: first use, completion, recovery, mastery. `animate` writes whatever moves.

## Affordances

Standard affordances rather than reinvented ones (custom scrollbars, odd form controls,
non-standard modals are strangeness without purpose); consistency over surprise, screen after
screen.

## Triage when polishing

1. Broken or blocked tasks, data loss, misleading state, inaccessible paths.
2. Missing loading, empty, error, success, disabled and permission states.
3. Flow, hierarchy, responsive and design-system drift.
4. Visual and motion inconsistencies.
5. Code and asset clean-up.

Never perfect one corner while the rest sits below the same bar.
