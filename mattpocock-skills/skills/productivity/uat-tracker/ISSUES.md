# Raising the worklist's issues

One issue per group, so each group's investigation, decisions and hand-overs have one home the whole team can see. The sheet keeps what the testers asked and what they were told; the issue keeps everything else.

1. **Read the conventions.** Read the project's tracker conventions (`docs/agents/issue-tracker.md` where it exists) for title style, body sections and labels, and run `rows --owner all` for each worklist row's current issue link, since a row waiting on the user's work may not carry their code yet.
2. **Match existing issues.** A group whose rows already link one issue joins it: a comment on that issue adds the group's other rows, and the issue gets the config's queue label if it lacks it. Rows of one group that link different issues go to the user to settle.
3. **Draft.** For each group with no issue, draft one: a plain title naming the problem, and a body listing each row's ID, its feedback in plain words, any reference it gives (a booking, an order, a page), its priority, and why the rows are grouped. Use the config's tracker project and queue label.
4. **Show, then create.** Show every draft and every joining comment in one list. Create them on the user's yes.
5. **Link the rows.** Write each issue's address into its rows with `write --issue` (with `--dry-run` first). The script refuses a row that already links a different issue.
6. **Record.** Add each group's issue to the worklist in the `rewind-durable` file.
