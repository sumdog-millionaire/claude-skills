# Success feedback

**Reach for this when** deciding what a person sees after an action succeeds: a button press, a
save, a payment, a booking, a like, a drag between columns, the end of an onboarding flow. Also
when reviewing whether a screen ever leaves a click unanswered.

## The rule

When a person does something, there has to be feedback. When an action completes, they need to
know it worked.

Match the weight of the confirmation to the weight of the action:

- **A high-value or irreversible action** (a payment, a booking, a delete, finishing a milestone)
  earns a dedicated confirmation state or page: "You're all set to fly!", with the details restated.
- **A routine action** (checking off a task, saving a draft, moving a card to Done) is confirmed by
  the visible result of the action itself. The card is now in the Done column. Nothing else is
  needed, and adding a pop-up on top is noise.
- **Anything that takes long enough for "did it work?" to arise** shows an intermediate state
  ("Processing..." with a spinner) between the click and the result. See `loading-states.md`.

A completed action must never look identical to a pending or failed one.

## Why

The worst feeling for a person is uncertainty after spending money: "Did it go through? Did it
charge me? Should I press it again?" A $450 confirm button that does nothing produces exactly that,
and the re-press it invites can double the charge. A small success state removes the whole feeling.

But not every success is a milestone. A full-page celebration after moving a to-do card trains
people to ignore confirmations, and a huge pop-up after every checkout step is friction dressed as
reassurance. Sometimes the cleanest confirmation is the action itself: it slides over, and you just
know.

Underneath this is Nielsen's first heuristic, visibility of system status: keep people informed
about what is going on, through appropriate feedback within a reasonable time. Without it, they
cannot tell that their action was understood, and they end up confused and mistrustful.

## How to build it

1. Every user-triggered action that changes state produces a visible change in the interface before
   control returns to the person. Test: click each action and assert the DOM changes within the
   same interaction.
2. Walk the app's actions and, for each, ask whether the feedback is proportionate. Payments,
   bookings, deletes and milestones get a confirmation state. Routine changes are confirmed by
   their result alone.
3. For drag-and-drop, reordering or status changes, the new position is the confirmation. Do not add
   a second indicator on top of a change the person can already see.
4. A submit button that looks the same whether the request is in flight, succeeded or failed is a
   defect, regardless of whether the request actually worked.
5. Where a success state is a page, restate the essentials (what, when, how much) so it doubles as
   a receipt.

## Evidence and caveats

- This is a slice of Nielsen's heuristic 1, not the whole of it. The heuristic also covers ongoing
  state (location, mode, connection), which would not be called a "success state".
- The Doherty threshold (under 400ms) is about the speed of feedback, not its presence. This entry
  is about presence: "show that something happened", not "make it instant". The two are easy to
  conflate.
- The source video mentions confetti for milestones but never shows it. Treat celebration
  animation as an option for genuine milestones, used sparingly; the video's own warning is "please
  don't overdo it".

## Sources

- Synsation, Build for Good UX part 11 (success states), with part 1's opening scenario of a button
  that does nothing.
- Nielsen Norman Group, "10 Usability Heuristics" (heuristic 1) and "Visibility of System Status".
- Laws of UX, Doherty Threshold.
