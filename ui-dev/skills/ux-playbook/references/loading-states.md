# Loading states

**Reach for this when** a screen, a section or a control has to wait for something: a page load, a
fetch, a submit, an upload, a download, an export, a like, a save. Also when choosing between a
skeleton, a spinner, a progress bar and no indicator at all, and when deciding what to show while a
spinner runs on.

## The rule

Match the indicator to the length of the wait and to what is known about it.

| Expected wait | Show |
|---|---|
| Under about one second | Nothing. Render the result directly. |
| One to five seconds | A plain spinner, no text, inside the element that is waiting. |
| Five to ten seconds | A spinner with text, and prefer two or three messages that change during the wait over one static line. |
| Over ten seconds, or any wait whose length is knowable | A determinate indicator: a percentage bar or a step list that tracks real progress. Never a looped spinner. |

Then pick the shape by what is waiting:

- **A whole page or a large section whose layout is already known** (a feed, a list of cards, a
  profile): a skeleton screen that mirrors the eventual layout, roughly the same number and size of
  blocks as the loaded content.
- **One small, contained thing** (a clicked button, one card refreshing): an inline spinner inside
  that element, with the element disabled for the duration so the action cannot fire twice.
- **A task with a measurable duration** (upload, download, install, export): a progress bar. A
  spinner here reads as "stuck".
- **A near-certain, cheap action** (a like, adding to a list, moving a card): optimistic UI. Apply
  the change instantly, confirm with the server afterwards, and roll back visibly if it fails.

On failure, show the error the moment it is known. Never let a spinner run its full course and then
announce that the action failed.

## Why

A spinner takes over a second just to be read. Shown for less than that, it flashes, and the flash
registers as something odd having happened, which makes a fast response feel slower than showing
nothing would. Past a few seconds a bare spinner stops meaning "working" and starts meaning
"broken", because the person has no idea whether anything is happening. Text that changes restores
that sense of progress: people believe visible effort even when the messages are not tied to
anything, which is why a fabricated "connecting to your account, almost there" buys patience out
to about ten seconds. Past that, looped animation of any kind flips from reassuring to
infuriating, and only a real measure of progress holds attention.

Skeletons work because the brain starts parsing the layout before the data arrives, so the wait is
spent doing something. Progress bars work because people prefer a moving indicator of progress to
none, even when it is inaccurate: 86% preferred one in the original 1985 study. Optimistic UI works
because the action feels instant and the failure case is rare enough that a visible rollback is a
fair trade.

The reason all of this matters is that a missing loader is read as a broken app, while a good one
is not consciously noticed at all. Even the crude indicators of the 1980s, a static wristwatch
cursor or hourglass, beat silence.

## How to build it

1. Below roughly 400ms to one second, mount no loading state. Test by timing the interaction and
   asserting no indicator appears for fast responses.
2. Every data-driven view has a skeleton that matches its loaded layout. Do not use a full-page
   spinner as the default for a page whose layout is known.
3. Every button that triggers a request goes into a loading state inside itself (spinner replacing
   or beside the label, width preserved, control disabled) and out of it on success or failure.
4. Anything with a knowable duration gets a determinate bar or step list driven by real milestones
   in the request, never a decorative animation on a timer. A percentage that stalls, drops or
   jumps destroys trust the moment it is noticed.
5. For a multi-stage determinate bar, put the slow or unpredictable stage first and let a fast,
   reliable stage finish it, so the bar appears to accelerate. A pause near the end is judged far
   more harshly than the same pause near the start.
6. No spinner, static or animated, runs past ten seconds. If a wait can exceed that, it needs a real
   indicator instead.
7. Optimistic UI only for actions that almost always succeed and that the client can safely assume,
   never for a login, a payment or anything the server must verify. Build the visible rollback
   (a toast and a reversal) before shipping the optimistic path.
8. On failure, surface the error immediately and clear the loading state.

## Evidence and caveats

- **Skeletons feeling faster than spinners is not settled.** A 2017 industry test (Viget, 136
  participants) found the skeleton performed worst of three conditions on perceived wait,
  satisfaction and completion time. A 2018 peer-reviewed study (Mejtoft et al., ECCE) found a small,
  non-significant edge for skeletons and concluded the claim could not be proven. Use skeletons
  because they show layout, and treat "it feels faster" as something to test with real users.
- **The time bands are a practitioner's rule of thumb.** Nielsen's documented limits are 0.1s
  (instant), 1s (flow unbroken) and 10s (attention lost). The finer two-to-five and five-to-ten
  second bands are the video creator's own granularity and appear in no source checked.
- **The 86% figure is real but slightly misdated.** Brad Myers, CHI 1985, 48 participants, 86.1%
  liked progress bars. "Even when inaccurate" comes from Myers's later commentary, not a separate
  statistic in the paper.
- **The labour illusion is peer-reviewed.** Buell and Norton (2011) found that showing effort
  raises perceived value, and people sometimes prefer a slower, visibly working process to an
  instant one. This is the mechanism behind changing status text, and it cuts both ways: it is
  also why a fake progress number that is noticed does so much damage.
- **Nielsen Norman Group's own split** is skeletons for a full-page load and a plain spinner for a
  single module inside an already-loaded page. Follow that: a dashboard card refreshing on its own
  gets a spinner, not a skeleton.
- **The Doherty threshold (400ms)** sets the point below which no indicator is needed. Nielsen's
  scale decides which indicator once the wait is longer. They answer different questions.
- **Optimistic UI has no single coiner.** It descends from optimistic concurrency in computer
  science; the clearest front-end popularisation is Meteor's 2015 writing, which also gives the
  risk rule above.

## Sources

- Synsation, Build for Good UX parts 2 (history of loading indicators), 3 (which loading state to
  choose) and 4 (the psychology of spinners).
- Nielsen, "Response Times: The 3 Important Limits" (1993), nngroup.com.
- Nielsen Norman Group, "Progress Indicators Make a Slow System Less Insufferable" (2014) and
  "Skeleton Screens 101" (2023).
- Myers, "The Importance of Percent-Done Progress Indicators", CHI 1985.
- Harrison et al., "Rethinking the Progress Bar", UIST 2007.
- Buell and Norton, "The Labor Illusion", Management Science 2011.
- Wroblewski, "Mobile Design Details: Avoid The Spinner" (2013), the origin of the term skeleton
  screen.
- Viget, "A Bone to Pick with Skeleton Screens" (2017); Mejtoft, Långström and Söderström, ECCE 2018.
- Laws of UX, Doherty Threshold; Doherty and Thadani, IBM Systems Journal 1982.
- Meteor, "Optimistic UI with Meteor" (2015).
