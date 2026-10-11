---
name: ux-playbook
description: A playbook of UX rules for building screens, each with the rule, why it holds, how to build it, what the evidence says and where it is contested. Organised by the situation a builder is in (a loading state, an error message, a form, an empty list, a button, a long menu) and cross-indexed by the named law behind it (Jakob's, Hick's, Tesler's, progressive disclosure, graceful degradation). Inside design and build work, ui-dev loads it at the brief, the Stitch hand-over, the state pass and verification. Reach for it directly for a UX review, a phase-end UX sweep, reviewing a single component, form, dashboard, checkout or onboarding flow, or a question like "how should this load", "where does the error go", "should this button be disabled" or "is this menu too long", even when the request never says UX.
---

# UX playbook

A reference for building screens that behave well, distilled from Synsation's "Build for Good UX"
series and checked against the primary sources behind each claim (Nielsen Norman Group, Laws of UX,
the original papers). Every entry is organised around a situation, not a video, so the question to
ask is "what am I building?" rather than "which video was that?".

This is a reference, not a generator. It asks the user nothing; it is read while building or
reviewing and the rules are applied to the screen in hand.

## How to use it

1. Find the entry for the situation you are in, from the first table below. If you only know the
   law's name, use the second table.
2. Read that entry's `references/` file in full. Each one is short and has the same shape: when it
   applies, the rule, why, how to build it, evidence and caveats, sources.
3. Apply the "How to build it" list as a checklist against the screen. Those items are written to be
   testable, so a review can say which ones the screen fails.
4. Where an entry's "Evidence and caveats" section says a claim is contested, do not present the rule
   as settled fact to the user. Say what the evidence supports and what it does not.

Two entries almost always apply together: every screen that fetches data needs all of
`loading-states`, `empty-states`, `error-messages` and `success-feedback` built, because those are
the four states a screen can be in, and a screen that only renders when the data is present is
unfinished.

## Find the entry by situation

| I am building or reviewing... | Read |
|---|---|
| Something that waits: a page load, a fetch, a spinner, a skeleton, an upload, a progress bar, an optimistic update | `references/loading-states.md` |
| The wording or the placement of an error: a failed payment, a bad field, a toast, a modal, a stack trace that leaked | `references/error-messages.md` |
| A form: required fields, validation, a submit button, a password field, a phone number, a character limit | `references/forms.md` |
| A list, dashboard, inbox or search result that can be empty, including a first-run screen | `references/empty-states.md` |
| What happens after a click succeeds: a confirmation, a success page, a saved state, a drag that lands | `references/success-feedback.md` |
| A page made of several sections that fetch separately, and what happens when one of them fails or is slow | `references/partial-failure.md` |
| A button, or any control that can be hovered, focused, pressed, loading or disabled | `references/button-states.md` |
| Where to put a standard control (cart, search, menu, primary action), on desktop, on a phone, or in a right-to-left locale | `references/control-placement.md` |
| A menu, a landing page, a long form, a catalogue: anywhere the person has to choose between many options | `references/optimising-choices.md` |
| What to show first and what to hide behind a click: a busy toolbar, a dropdown that scrolls, a command palette | `references/progressive-disclosure.md` |
| A section with a hard step in it: a lookup, a calculation, re-entered details, a multi-step confirmation, anything the product could do for the person instead | `references/streamlining-complex-sections.md` |

## Find the entry by law or term

| Law or term | Entry |
|---|---|
| Visibility of system status (Nielsen heuristic 1) | `success-feedback`, `loading-states`, `empty-states` |
| Help users recognise, diagnose and recover from errors (Nielsen heuristic 9) | `error-messages` |
| Recognition rather than recall (Nielsen heuristic 6) | `forms`, `streamlining-complex-sections` |
| Nielsen's response-time limits (0.1s, 1s, 10s) | `loading-states` |
| Doherty threshold (400ms) | `loading-states`, `success-feedback` |
| Labour illusion (Buell and Norton) | `loading-states` |
| Skeleton screens, optimistic UI, stale-while-revalidate | `loading-states`, `partial-failure` |
| Graceful degradation | `partial-failure` |
| Jakob's Law | `control-placement` |
| Thumb zone (Hoober) and right-to-left mirroring | `control-placement` |
| Hick's Law, choice overload, the jam study | `optimising-choices` |
| Progressive disclosure | `progressive-disclosure` |
| Tesler's Law (conservation of complexity) | `streamlining-complex-sections` |
| Postel's Law (be liberal in what you accept) | `forms` |
| WCAG 2.4.7 Focus Visible | `button-states` |
| Inline validation (Wroblewski) and the disabled-button debate | `forms`, `button-states` |

## The one principle underneath all of it

A beautiful screen with unpredictable behaviour loses people, and the failure people remember is
the one where they clicked something and nothing happened, then blamed themselves. The builder
never sees this, because the builder knows the app and only ever walks the happy path. So the
habit this playbook exists to build is: for every screen, ask what it looks like while waiting,
when there is nothing to show, when something breaks, and when it works, and build all four
before calling the screen done. Someone who did not build it, with an empty database and one
request forced to fail, is the test.

## Adding a video

New videos in the series, or from anywhere else, are folded in like this:

1. Run the `source-to-skill` skill on the video with the notes-only route. It writes a full
   `findings.md` into `~/source-to-skill-runs/<id>--<slug>/`, with what the video teaches, what
   was on screen, what the research found, and applied rules.
2. Read the findings and decide whether the video extends an existing entry or opens a new one.
   Extend when the situation already has a file, which is most of the time: a second video on
   forms goes into `forms.md`, however it is titled. Open a new file only for a genuinely new
   situation, and give it the same six sections as the others.
3. Fold the content in by section: new rules into "The rule" and "How to build it", new reasoning
   into "Why", anything the research qualified or contradicted into "Evidence and caveats", and the
   video plus its primary sources into "Sources". Merge, do not append: a reader should not be
   able to tell which video a sentence came from.
4. Add the situation to the first table above and any new law or term to the second. The tables
   are how an entry gets found, so an entry missing from them does not exist.

The entry is named for the situation, never for the video or the creator. That is what keeps it
findable a year from now, when nobody remembers the series.
