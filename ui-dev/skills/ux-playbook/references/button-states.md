# Button states

**Reach for this when** building or styling any button or interactive control, when a hover effect
misbehaves on touch, when a focus outline has been removed, when a click gives no feedback, or when
deciding whether to disable a button.

## The rule

A button is not one picture. It has six states, each sending a specific signal:

| State | Signal | Treatment |
|---|---|---|
| Default | "I can be pressed" | Solid fill, clear outline, perhaps a soft shadow so it looks slightly raised |
| Hover | "I will respond if you click" | A slight change of colour or outline, and the cursor becomes a hand. Mouse only. |
| Focus | "This is where you are" | A visible outline when reached by keyboard (Tab). An accessibility requirement, not a style choice. |
| Pressed | "Your tap did something" | Darkens, or a short animation of being pushed in; on a phone a haptic buzz or ripple |
| Loading | "I heard you, I'm working" | A spinner inside the button itself, replacing or beside the label, width preserved |
| Disabled | "Not available" | Greyed and lower contrast. Contested; see below. |

Define all six explicitly. Never build a hover-only affordance for something that must work on
touch. Never strip the focus outline without an equally visible replacement.

## Why

People use buttons all day and never notice the states, until one is missing. A pressed state with
zero feedback is where people start pressing again and again, because they assume the site is
frozen. A loading state inside the button keeps their attention where they were already looking,
instead of dragging it to a full-page loader. A focus outline is how anyone navigating by keyboard
or screen reader knows which control they are on; without it the page is unusable to them.

Hover exists only where there is a cursor. On a phone there is nothing to hover, and a hover style
that fires on touch gets stuck in a half-triggered state that reads as buggy.

Disabled buttons are the state the field is arguing about. A native disabled button cannot receive
keyboard focus, so keyboard and screen-reader users may never discover it exists, and even when it
is visible it says nothing about what the person must do to enable it. The recommended alternative
is to keep the button clickable and explain inline why it cannot proceed yet.

## How to build it

1. Every button has all six states defined in the design system and the code, not "the button" plus
   states bolted on later.
2. Never `outline: none` on a focusable element without a `:focus-visible` replacement of equal or
   higher contrast. Test: tab through every interactive element on the page and confirm a visible
   outline lands on each. This is WCAG 2.1 Success Criterion 2.4.7 (Level AA).
3. Hover changes are additive on top of a state that also works on touch. No interactivity signal
   is hover-only.
4. Pressed feedback appears within a short, consistent delay after every tap or click. Zero
   feedback is a defect.
5. Loading lives inside the button that triggered it, with the control disabled for the duration so
   it cannot fire twice. See `loading-states.md`.
6. Where a button gates submission until fields are valid, prefer keeping it focusable and clickable
   with an inline reason, using `aria-disabled="true"` rather than the native `disabled` attribute
   so it stays in the tab order and is announced. See `forms.md`.

## Evidence and caveats

- The six-state model matches Nielsen Norman Group's "Button States: Communicate Interaction" almost
  exactly (enabled, disabled, hover, focus, pressed, plus loading), including the treatments above.
- Focus visibility is a formal requirement, WCAG 2.1 SC 2.4.7. WebAIM's 2024 audit of a million home
  pages found 78% had detectable focus-indicator problems, mostly from developers removing the
  default outline for looks.
- The disabled-button debate is genuine and well documented (Adam Silver, Axess Lab, UX Tigers,
  NN/g's "Why Disabled Buttons Hurt UX"). The source video defers its own view to a later part;
  among accessibility-focused writers the debate is fairly one-sided against native disabled
  buttons, which is the position this playbook takes.
- The source video calls its own "Solid Fill" mock-up "a bad example" (plain fill, no outline or
  shadow) without showing a corrected one. The table's default treatment is from NN/g.

## Sources

- Synsation, Build for Good UX part 17 (button states).
- Nielsen Norman Group, "Button States: Communicate Interaction"; "Button States 101" (video); "Why
  Disabled Buttons Hurt UX (and How to Fix Them)" (video).
- W3C, WCAG 2.1 Understanding Success Criterion 2.4.7: Focus Visible; WebAIM Million (2024).
- Axess Lab, "Disabled buttons suck"; UX Tigers, "Inactive buttons"; Adam Silver, adamsilver.io.
