# The UAT work section

Once user-acceptance testing starts, every agent on the team works only on what the testers raised. Without a written rule an agent drifts onto other open issues, and a tracker that was never cleaned up after the build holds plenty that nobody wants done any more. The section below, in the project's `CLAUDE.md`, is that rule. Fill the three placeholders from the config and from the user: `<queue label>` is the config's `tracker.queue_label`, `<feedback sheet>` where the testers log their feedback, and `<stakeholder>` the person on the client side who agrees what joins the queue.

```markdown
### UAT work

User-acceptance testing is under way, so build only issues labelled `<queue label>`. They are raised from <feedback sheet>, where <stakeholder> and the team choose, prioritise and allocate the rows. Every other open issue waits until UAT ends, however urgent it looks. Each owner works their rows with the uat-tracker skill.

Anything new you notice becomes a row or an issue for the next session, never a quiet fix.
```
