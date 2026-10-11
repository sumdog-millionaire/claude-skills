# Acting on a video digest

Follow only the branch or branches the user selected. The evidence map is not automatic authority
to create work or change a project. Set `<report>` to `meeting-notes.md` for a recorded meeting and
`digest.md` for another video.

For every write outside `<report>`:

1. inspect the destination and its local instructions;
2. identify what already exists;
3. show the exact proposed creations or changes, including destination and content;
4. resolve any material fork with AskUserQuestion;
5. obtain approval; and
6. make exactly the approved change and verify it through the destination's normal checks.

If implementation reveals a change outside the proposal, stop and explain it rather than
improvising.

## Issue tracker work

Use the issue tracker named by the user or documented by the current project. This may be Linear,
GitHub Issues, Jira or another system. Do not introduce a tracker when the project has none.

1. Read the project's tracker guidance and inspect available tracker tools.
2. Search for existing issues covering the selected findings. A meeting action does not necessarily
   need a new issue; it may belong in an existing issue, a comment, a relation, or nowhere.
3. Ask which findings the user wants tracked if their selection was broader than the digest supports.
4. Present a concrete proposal for each write:
   - tracker and project;
   - create, update, comment, relation or status change;
   - title and full content;
   - labels, milestone, owner and relations only when supported by project rules or source evidence;
   - the digest timestamp and frame evidence that justify it.
5. After approval, perform the writes and return the issue identifiers or links. Record them in
   `<report>`'s **Outcome** line.

Preserve source certainty. Do not assign an owner, due date, priority or commitment that the
recording did not establish unless the user explicitly supplies it.

## Project or documentation changes

1. Ask what selected finding should change and in which project.
2. Read only the files and instructions needed to make that proposal concrete.
3. Show every file that would change and what would change in it. For a large change, show a plan;
   for a small change, describe the exact edit.
4. Get approval, make the change using the project's workflow and run its smallest relevant check.
5. Report changed files and checks, then name the project in `<report>`'s **Outcome** line.

Implement the finding that the recording supports. Do not expand it into adjacent cleanup or future
plumbing.

## External research

Research only the selected names, claims, tools or methods. Prefer current primary sources: official
documentation, source repositories, standards and vendor material. Separate:

- what the recording stated;
- what the external source confirms;
- what has changed since the recording; and
- what remains unverified.

Add the researched findings and links to a clearly labelled section in `<report>`. Do not silently
rewrite the source-bound chronology using later information.

## Create or update a skill or agent

Load the `skill-creator` skill before creating or editing any skill or agent file. It owns current
frontmatter, triggering, progressive disclosure, evaluation and packaging conventions.

Ask only what the digest leaves materially uncertain:

- skill or agent;
- which method or behaviour is in scope;
- phrases or contexts that should trigger it;
- behaviour it must exclude; and
- required tools, services or credentials.

Recommend a skill when it teaches a reusable method inside a conversation. Recommend an agent when
it should be dispatched to carry out a bounded job. Check whether an official skill or plugin already
covers the need before writing a duplicate.

Give `skill-creator` the report path, transcript, relevant frame evidence, source metadata and the
user's answers. State that the scoping interview is complete so it does not repeat settled questions.
Do not draft the skill yourself.

Any generated skill or agent must start by using AskUserQuestion for choices that materially change
its output, unless the invoking request already answered them. This keeps generated tooling from
running ahead of the user's intent.

After the draft, ask whether the user wants the longer evaluation and benchmark loop. Do not start
that work by default.

## Another deliverable

Ask for the intended reader, purpose, destination format and required level of detail only where the
request has not already answered them. Propose the output and location, obtain approval, then create
it from the digest and linked evidence. Preserve the distinction between source facts, inference and
recommendation.

## Digest only

Make no further changes. Add:

```markdown
**Outcome:** Digest only.
```
