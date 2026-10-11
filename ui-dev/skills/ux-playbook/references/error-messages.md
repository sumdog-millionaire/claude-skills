# Error messages

**Reach for this when** writing the words of an error, deciding where on the screen it appears
(inline, a toast, a modal), handling a failed payment, save or submit, or reviewing any place a
backend error could reach a person.

## The rule

**The words.** A good error message says three things, in this order: what happened, why it
happened, and what to do next. "Your payment didn't go through. Your card was declined. Please
check your card details or try a different payment method." A message that gives only one or two of
the three is incomplete.

Two failures sit either side of that:

- **Raw backend output** (a stack trace, a database error, a connection string) is never shown to a
  person. They cannot read it, and it is a security disclosure.
- **A bare "something went wrong"** is not enough either. After pressing pay, the person cannot tell
  whether money moved.

And the worst of all is **silence**: a click that does nothing, a screen that does not change, and
no way to tell whether it worked or broke.

**The placement.** Put the error as close to the problem as possible. Three placements, chosen by
how much the error blocks the person:

| Placement | What it is | Use it for |
|---|---|---|
| Inline | Next to the thing that went wrong: a red border and a line under the field, or a line under the button just clicked | Almost everything. Field errors, failed saves, failed actions. |
| Modal | Takes over the centre, blocks everything until answered | Only when the person cannot continue without resolving it: a payment that failed and the subscription will lapse, access denied to the page itself. Always with a button that resolves it. |
| Toast | Pops up at an edge and dismisses itself in a few seconds | Never for an error the person must act on. Only for status the system resolves on its own: "couldn't connect, retrying". |

## Why

An error message is the moment the product either takes responsibility or hands the blame to the
person. Technical output says "this is your problem to decode". A vague message says "we know
something is wrong but not what", which for a payment or a booking leaves the person unable to
decide whether to try again. The three-part shape gives them exactly what they need to recover, and
nothing they cannot use.

Exposing backend detail is not only unhelpful, it is a catalogued weakness (CWE-209): stack
traces, paths, table names, hostnames and credentials all help an attacker's reconnaissance. The
fix is the same either way: log the full detail on the server, show the person a plain message.

Placement follows attention. When someone has just clicked a button or left a field, their eyes are
already there, so an error anywhere else makes them go looking, and a message next to the problem
can be read while fixing it rather than remembered from a banner at the top. A toast that
disappears while the person looks away has told nobody anything, which is why it cannot carry
anything important. A modal steals the whole screen, which is only justified when the whole screen
is genuinely unusable until the problem is fixed, and even then it must hand back a way forward or
it is just a dead end with a dimmed background.

## How to build it

1. Catch every error at the boundary. Log the full detail server-side; render a human-readable
   message. Treat any leak of paths, table or field names, credentials or internal hostnames as a
   security defect, not a style issue.
2. Every user-facing error states what happened, why (where known and safe to say), and what to do
   next. Write the "what to do next" as an action the person can take, not an apology.
3. "Something went wrong" is an internal fallback only, and even then it is paired with a next
   action (retry, contact support, go back). It is never the final wording of a designed error.
4. Every action that can fail (submit, save, pay, upload, delete) shows a visible state change on
   failure. Test the failure path explicitly: force the request to fail and confirm the screen
   changes.
5. Field errors render inline: a coloured border plus a short message directly under or beside the
   field, never only a summary banner or a toast.
6. A failed button action shows its error immediately next to that button ("Couldn't save, try
   again").
7. Before adding a modal, ask whether the person could reasonably carry on with the error unresolved.
   If yes, it is inline or a banner. If the modal has only "OK" or "Dismiss" and no way to fix the
   problem, it fails the way-forward rule.
8. Financial flows are held to a stricter standard: the person must always be able to tell whether
   money moved.
9. When asking an AI coding tool for a form, payment or submit flow, name the error states wanted
   explicitly. Generic or silent failure handling is what these tools produce by default.

## Evidence and caveats

- The three-part shape is a plain-language version of Nielsen's heuristic 9: "expressed in plain
  language, precisely indicate the problem, and constructively suggest a solution." The heuristic is
  broader (a system's whole approach to errors), but the wording rule is a faithful slice of it.
- Severity-matched placement is Nielsen Norman Group's own guidance: toasts and banners for
  low-impact issues, modals reserved for severe errors that need resolution. Inline proximity is
  their forms guidance, justified by working memory: the person sees the message while fixing it.
- "Silent failure" is not a named term in the literature. The idea maps onto Nielsen's heuristic 1,
  visibility of system status, which warns that without feedback people "end up confused and
  mistrustful".
- Laws of UX has no entry on error handling. Postel's Law there concerns tolerant input, not output
  wording, and should not be cited for this topic.
- "Toast" is a UI pattern name from Android's notification API, not a research term.

## Sources

- Synsation, Build for Good UX parts 5 (what makes a good error message) and 7 (where to put the
  error).
- Nielsen Norman Group, "Error-Message Guidelines"; "10 Usability Heuristics" (heuristics 1 and 9);
  "Modal & Nonmodal Dialogs: When (& When Not) to Use Them"; "10 Design Guidelines for Reporting
  Errors in Forms".
- OWASP Error Handling Cheat Sheet; MITRE CWE-209, Generation of Error Message Containing Sensitive
  Information.
