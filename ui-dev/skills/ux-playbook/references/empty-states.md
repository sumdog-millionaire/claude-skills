# Empty states

**Reach for this when** any container can legitimately hold nothing: a new account's dashboard, a
list before its first item, a search or filter with no matches, an inbox or queue that has been
cleared. Also for first-run onboarding, since the empty state is usually the first screen a new
person sees.

## The rule

A good empty state does three things: tells the person why it is empty, shows them what to do
next, and does not feel broken.

There are three different kinds, and they should not share a component or a message:

- **First use** (a new dashboard, no projects yet): the explanation plus one primary action the
  person can take right now ("+ Create new project"), and where several setup steps follow, a
  checklist with visible progress.
- **No results** (a search or filter that matched nothing): name the exact term that failed and,
  where a likely correction exists, offer it as one click. "No results for 'prple shoes'. Did you
  mean 'purple shoes'?"
- **The goal was empty** (an inbox at zero, a cleared queue, a finished checklist): this is an
  achievement, designed as a reward, with something the person looks forward to seeing.

Every section of an app that has no content yet says what the section is for and how to start
using it. Nothing is left blank.

## Why

The empty state is not the exciting part to build, so it gets forgotten, and yet it is the state a
new person meets first. A blank area with no text cannot be told apart from a screen that is still
loading or has broken, so the person's first impression is "is this working?". "You have no
projects" with nothing else is a step up, but leaves them with no action and no idea what the
screen is for. Adding the one action turns the dead end into a start. Adding a progress checklist
turns the start into a path.

A search that returns "no results" and stops has made the person retype from scratch, when the
system could see the near miss. Offering the correction keeps them moving.

The cleared inbox is the opposite case: the person worked to reach it. Treating it like a "nothing
here yet" screen throws away the one moment the product can feel rewarding.

## How to build it

1. Every container that can be empty has an explicit empty-state component, designed before the
   feature is called done. No bare blank areas.
2. First-use empty states pair one sentence of explanation with one primary action, in place, not a
   link elsewhere or a menu to hunt through.
3. Where onboarding has several steps, show them as a checklist with a count or percentage complete
   and a time estimate per step, ticking off as each is done.
4. No-results states quote the failed term. Where a correction can be inferred (a typo, a near
   miss), it is a single link that runs the corrected search.
5. Goal-reached empty states get their own copy and treatment (a streak, an illustration, a warm
   background), separate from the first-use component.
6. Every empty-state message reads as designed, never as absence. Test each one cold: load the
   screen with an empty database and check it explains itself without instructions.

## Evidence and caveats

- The three-part test matches Nielsen Norman Group's three guidelines for empty states almost
  exactly: communicate system status, provide learning cues, offer direct pathways for key tasks.
  NN/g names unpopulated dashboards and no-match search results as two of the standard cases.
- "Inbox zero" originates with Merlin Mann (43 Folders, 2006). Mann's "zero" meant zero mental
  attention spent on email, not a literally empty inbox. The popular literal reading, which the
  source video uses, is a flattening of the original, though it is now the common usage.

## Sources

- Synsation, Build for Good UX part 8 (don't forget the empty state), with part 1's framing of the
  empty state as one of the states AI-built software skips.
- Nielsen Norman Group, "Designing Empty States in Complex Applications: 3 Guidelines" (Kaplan,
  2021).
- Merlin Mann, Inbox Zero series, 43 Folders (2006).
