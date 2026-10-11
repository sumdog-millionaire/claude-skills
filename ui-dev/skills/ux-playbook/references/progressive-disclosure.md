# Progressive disclosure

**Reach for this when** deciding what a screen shows first and what waits behind a click: a busy
toolbar, a dropdown that has grown until it scrolls, a settings page, an editor with many block
types, a feature that only some people need.

## The rule

Show people what they need right now, the next step or the next layer of options, and keep the rest
reachable on request. Nothing is deleted; it is staged.

- The primary screen shows only the options most people need for the task they came to do.
- Everything else sits behind an explicit, visible trigger: a button, a "show more", a command key.
- At most two levels: the primary view and one secondary layer. A feature that needs a third click
  is reconsidered rather than nested deeper.
- The trigger is visible and taught on the primary screen, so the person can tell there is more
  before they go looking.
- Nothing frequently needed is hidden. If reaching a feature needs a tutorial, it is either surfaced
  higher or its trigger made more discoverable.

## Why

Driving somewhere new, nobody wants all thirty-five turns listed before leaving the driveway; they
want the next turn as it comes. An interface that shows every capability at once makes the person
scan and reject everything irrelevant before they can act, and buries what they want among things
they do not. A video-generation site whose Image and Video menus are so long they need scrolling
had a motion-graphics option at the bottom that the creator, a regular user, did not know existed.

Notion does a million things, and the interface feels clean, because the AI chat only appears when
asked for and the block menu is hidden until the person types a slash. Once it opens, they can keep
typing to narrow it. The placeholder text ("Press '/' for commands") is what teaches the trigger;
without it, the same design would be a hidden feature.

The two-level ceiling exists because people get lost beyond it: deeper nesting produces low
usability in testing, however tidy the top level looks.

## How to build it

1. For each screen, list every visible option and ask whether it is needed at this moment for the
   task the person came for. Move what is not behind a trigger.
2. Keep disclosure to two levels. Anything needing a third click gets surfaced or merged instead.
3. Every secondary layer has a visible, labelled trigger on the primary screen. A menu with no
   affordance fails even if the feature exists.
4. Before adding an item to a busy menu, check it belongs at that level. A menu that scrolls has
   stopped disclosing progressively and become a dumping ground.
5. For a genuinely large option set, a command-style trigger that filters as the person types beats
   a static dropdown, but only with a placeholder hint that teaches it.
6. Deciding which features are "most important" is the hard part. Use usage data where it exists;
   where it does not, the task the person came for is the test.

## Evidence and caveats

- The pattern is long-standing, not the source creator's. Wikipedia traces the seminal idea to
  Kristina Hooper Woolsey at Apple's Human Interface Group, 1985. Nielsen Norman Group calls it more
  than thirty years old and gives the two rules (most important options first, the rest on request)
  and the two-level warning above.
- A secondary source attributed the term to Jakob Nielsen in 1995 with a 2006 restated definition;
  this could not be verified against a primary NN/g text and is recorded as unconfirmed.
- Laws of UX's page on progressive disclosure (Stripe's hover menu as its example) did not resolve
  during research and is reported second-hand.
- The source video's bad example is higgsfield.ai; the audio mishears it as "Hexel's". The screen
  is the authority.
- The source video presents a clean binary (bad site, good site) and omits NN/g's two-level ceiling
  and the question of how to decide what counts as important. Both are added above.

## Sources

- Synsation, Build for Good UX part 15 (progressive disclosure).
- Nielsen Norman Group, "Progressive Disclosure".
- Wikipedia, Progressive disclosure (Woolsey, 1985).
- Laws of UX, Progressive Disclosure (unconfirmed during research).
