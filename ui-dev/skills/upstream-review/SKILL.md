---
name: upstream-review
description: Review what has changed in the repositories this plugin took skills and text from since each was last reviewed, and adopt the changes worth having into our customised copies. Use when the user asks to review, sync, upgrade or update the plugin's upstreams, or asks whether a source skill has moved on.
disable-model-invocation: true
---

# Upstream review

Read `upstream.json` at the plugin root and work through its entries. Merge every adopted change
into our copy by hand; our copies carry local edits, never paste over them.

## 1. Fetch, read-only

For each entry, clone the repository shallowly into a temporary folder outside the plugin
(`git clone --depth 200` is enough to reach the reviewed commit; deepen if it is not there), and
resolve the default branch rather than assuming its name. Record the fetched head commit and date.

Diff `sourcePath` and every `alsoWatch` path between `reviewedCommit` and the head. Read each changed
section in context, including removed text and changed code examples. Check the licence file for
changes too.

## 2. Table the changes

Show one table per upstream, one row per distinct change:

| Upstream change | Where in ours | Recommendation | Reason |
|---|---|---|---|
| what changed, with the upstream file and section | the file of ours it would touch, or "not carried" | adopt, adapt or skip | the benefit, and any local decision it collides with |

Recommend with a reason every time. A change that contradicts a decision recorded in the entry's
`reviewNotes` is recommended as skip with that decision named, so the user can overrule it knowingly.
Then wait for the user's choices. A request to review is not permission to apply.

## 3. Apply what was chosen

Apply each chosen change to our copy by hand, comparing three things: the reviewed upstream version,
the new upstream version, and ours. Keep every local edit that the change does not deliberately
replace. For text that was lifted rather than vendored, rewrite the passage in the voice of the file
it lives in.

Then strip em dashes. List every one from the plugin root:

```bash
git grep -nP '\x{2014}' -- '*.md'
```

Replace each by hand with what the sentence needs, usually a comma, colon, full stop or brackets, and
a spaced hyphen where a dash really is the right mark. Run the command again; it must print nothing.

## 4. Check, then record

Run the plugin's checks before recording anything: `claude plugin validate . --strict` from the
plugin root, the em dash command above printing nothing, and a read of every description that changed,
to confirm no two skills now trigger on the same phrase. If a check fails, fix it or leave the
entry's `reviewedCommit` where it was and say the review is incomplete.

Only when the checks pass, set the entry's `reviewedCommit` to the fetched head and rewrite its
`reviewNotes` to say what was adopted, adapted and skipped in this review. Record the skipped changes
too, so the next review does not propose them again. Show the final diff. Commit only if the user
asks, with a message that says which upstream moved and what was taken.
