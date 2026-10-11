# Forms

**Reach for this when** building or reviewing any form: sign-up, checkout, settings, a single field
with a rule attached (email, password, phone, a length limit), or a submit button and what gates it.

## The rule

Six rules, in the order a person meets them:

1. **Mark required fields before the person tries to submit**, never only after a failed attempt
   reveals them. Nobody should be guessing why they cannot proceed.
2. **Validate a field once the person has left it**, not while they are still typing it. Tell them
   the email is wrong the moment they move on, not after they have filled the rest, submitted,
   waited, and scrolled back up.
3. **Show a live character count** on any length-limited field as soon as there is content in it,
   not only once the limit is hit. Do not let someone write a paragraph and then tell them to
   delete half.
4. **Prefill anything already known** about a signed-in person. Their email address is not asked for
   twice.
5. **List a field's requirements before typing starts and tick them off live** as each is met. This
   is the one case for while-typing validation: a password or a chosen username, whose valid shape
   the person cannot judge for themselves.
6. **Be liberal in what you accept.** A phone number with dashes, brackets or nothing at all is
   accepted and normalised in the backend, never rejected for its punctuation.

On the submit button: keep it enabled and clickable. Clicking it while something is wrong moves
focus to, and describes, the first invalid field. See the caveat below on why the greyed-out
button is the one piece of the source advice that is behind current guidance.

## Why

Nobody likes filling in forms, so every rule here removes a specific frustration. Marking required
fields removes guessing. Inline validation removes the scroll-back-and-fix loop, and the research
behind it is concrete: the best inline design cut completion time by 42% and errors by 22% against
validate-on-submit. Character counts and live requirement lists remove the discovery of a rule only
after breaking it. Prefill is Nielsen's "recognition rather than recall": what the system already
knows, it shows rather than asks. Tolerant input is Postel's Law applied to people: converting what
they typed into what the system needs is the system's job, not theirs.

The timing of validation matters as much as its presence. Validating an ordinary field while the
person is still typing it frustrated test users, because it flags an email as wrong before they have
finished writing it. Validate on leaving the field for anything whose correct shape is obvious, and
while typing only for fields whose rules the person cannot know in advance.

## How to build it

1. Every required field carries a visible required marker before any interaction.
2. Ordinary fields validate on blur. Password and username fields validate on input, against a
   visible list of requirements that update as each is met.
3. Error text sits directly under or beside its field, with a coloured border on the field. See
   `error-messages.md` for the wording.
4. Length-limited fields show "used / limit" or "remaining" from the first character.
5. Any value already held for the signed-in person is filled in, and visually distinguished so they
   can see it was done for them.
6. Free-format inputs (phone, postcode, card number) accept common punctuation variants and
   normalise server-side. Test with at least three punctuation styles.
7. The submit button stays enabled. On click with invalid fields, focus moves to the first one and
   its error is shown. If a disabled button is used anyway, it must be paired with visible required
   markers so the person is never guessing, and prefer `aria-disabled` over the native attribute so
   it stays focusable and announced (see `button-states.md`).
8. Long forms are split into steps; see `optimising-choices.md` for the threshold.

## Evidence and caveats

- **The greyed-out submit button is the advice to override.** The source video keeps it, softened
  by "mark what is missing". Nielsen Norman Group's forms guidance prefers inline validation with an
  always-clickable button. Designer Adam Silver argues disabled buttons are an anti-pattern
  outright: no feedback on what is wrong, they look unresponsive even when only one error remains,
  low contrast hurts readers with visual impairments, a native disabled button cannot receive
  keyboard focus, and it is often unclear the button is disabled at all. This playbook follows
  Silver and NN/g.
- **Inline validation has a named study.** Wroblewski and Etre, 22 participants, six form
  variants, A List Apart 2009: 22% higher success, 22% fewer errors, 31% higher satisfaction, 42%
  faster, 47% fewer eye fixations. Its conclusion is more specific than "validate inline": validate
  on blur for most fields, while typing only for unpredictable ones.
- **Character counts** have no dedicated study found; they are established convention, sitting
  inside NN/g's broader guidance on reducing the effort a form demands.
- **Postel's Law** is from Jon Postel's TCP specification (RFC 761, 1980; RFC 1122, 1989). Laws of
  UX extends it to interfaces: be tolerant of whatever a person provides and convert it, rather than
  turn it away.

## Sources

- Synsation, Build for Good UX part 6 (building a good form).
- Wroblewski, "Inline Validation in Web Forms", A List Apart 2009; "Web Form Design: Filling in the
  Blanks" (Rosenfeld, 2008).
- Nielsen Norman Group, "10 Design Guidelines for Reporting Errors in Forms"; "Few Guesses, More
  Success: Four Principles to Reduce Cognitive Load in Forms"; "10 Usability Heuristics" (heuristic
  6, recognition rather than recall).
- Adam Silver, "The problem with disabled buttons and what to do instead", adamsilver.io.
- Laws of UX, Postel's Law; RFC 761 and RFC 1122.
