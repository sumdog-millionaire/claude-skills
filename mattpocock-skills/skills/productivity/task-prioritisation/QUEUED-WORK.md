# The queued work section

A project that runs this skill keeps a short section in its `CLAUDE.md`, so every agent on the team builds only what the prioritisation session chose. The check in [SKILL.md](SKILL.md) proposes it when the project's `CLAUDE.md` does not name the queue label. Fill the three placeholders from the config and from the user: `<queue label>` is the config's `queue_label`, `<stakeholder>` the person the team agrees priorities with, and `<feedback sheet>` where their testers' feedback is logged.

```markdown
### Queued work

Build only issues labelled `<queue label>`; the prioritisation session with <stakeholder> decides what joins the queue. Work each one in this order:

1. Diagnose whether it is data, a rule, code or an expectation. A data problem goes back to <stakeholder> through the row's response in <feedback sheet>, with no code.
2. When the request is unclear, write a proposed reading in its response and wait for <stakeholder>'s answer before writing code.
3. Fix it, then write the findings, root cause and decision on the issue.

Anything new you notice becomes an issue for the next session, never a quiet fix.
```
