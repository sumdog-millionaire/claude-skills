# Streamlining complex sections

**Reach for this when** a task has a hard step and someone has to do it: a lookup, a calculation,
remembering a value, entering details the system already has, a multi-step confirmation. Also when
weighing engineering time for something that "only" saves the person a step.

## The rule

Every system has an inherent amount of complexity that cannot be removed, only moved. The only
decision is who carries it: the person building the app, once, or the person using it, every time.
As far as possible, take the burden off the person and put it on yourself, during design and
development.

Google autocomplete finishes the query. Netflix's "skip intro" button exists because someone found
the exact second the intro ends for thousands of shows. Apple Pay with Face ID replaces a password,
a card and sixteen digits with one tap. In each case the hard part was done once, in the product,
so it is never done by the person.

## Why

If a million people each waste a minute on a complexity an engineer could have removed in a week,
the product has penalised its users to make the engineer's job easier. That is Larry Tesler's
argument from the 1980s at Xerox PARC, and it is why he is also the person to thank for copy and
paste.

The person on the other end is not the perfectly patient, rational one the design was reviewed
against. They are busy and distracted and want the easiest path, and a product that handles the hard
part for them is more likeable for it. A reduction in steps is not polish trimmed when the deadline
is tight; it is the feature.

## How to build it

1. Before shipping a feature, name who carries its complexity. If the answer is "the person, one
   click at a time", treat that as a cost to justify, not a default.
2. Where a task has one unavoidable hard step, do it once in the code rather than asking every
   person on every visit.
3. Design for the distracted person looking for the shortest path, and route the interface towards
   that path by default.
4. Treat removed setup steps (fields, confirmations, passwords) as engineering work worth its time.
5. Check any quotation or statistic against its source before putting it in product copy or a pitch.
   The source video's own quote card is a paraphrase presented as verbatim.
6. Measure what happens after a simplification. People given an easier basic path often attempt
   harder tasks with the same tool, so "simpler" may shift what they try rather than reduce total
   demand.

## Evidence and caveats

- **Tesler's Law**, the Law of Conservation of Complexity, was formulated by Larry Tesler in the
  mid-1980s at Xerox PARC and became widely known through his interview in Dan Saffer's "Designing
  for Interaction", the source Laws of UX cites.
- **The quotation is a paraphrase.** The commonly cited original: "If a million users each waste a
  minute a day dealing with complexity that an engineer could have eliminated in a week by making
  the software a little more complex, you are penalizing the user to make the engineer's job
  easier." The video's version drops "a day" and "by making the software a little more complex".
- **The counterpoint the video omits**: Bruce Tognazzini's observation, recorded on Laws of UX,
  that people resist a real reduction in complexity and, once a task is easier, attempt more
  ambitious ones with the same tool. Tesler's position is one side of a live discussion.
- The on-screen slide says "inherent complexity", the more precise term; the audio says only
  "complexity".
- The video shows only good examples and no product that dumps its complexity on the person.

## Sources

- Synsation, Build for Good UX part 16 (Tesler's Law).
- Laws of UX, Tesler's Law; Saffer, "Designing for Interaction" (the Tesler interview).
- Wikipedia, Law of conservation of complexity.
