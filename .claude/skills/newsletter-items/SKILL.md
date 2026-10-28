---
name: newsletter-items
description: Fill this week's UMB.FYI newsletter with its news, event and package items. Finds the upcoming draft newsletter on the live site, runs the newsletter-generator workflow, tidies the results, shows one review table, then adds the approved items as blocks under their group headings once Matt says go. Never publishes. Use when asked to run the workflow, generate, import, populate or fill the newsletter items, or as part of newsletter prep.
---

# Newsletter items

This does what the Workflow tab does in the backoffice: run the `newsletter-generator` workflow, then add one Newsletter Item block per result under its group heading. The difference is that the items get reviewed as data before anything is written.

All API calls go through `.claude/skills/process-tips/scripts/umbfyi.sh` (run it with no args for usage). It talks to the LIVE site. Reads and the workflow run need no sign-off. The one write (step 7) happens only after Matt's go in step 6. If credentials are missing, stop and tell Matt to set up `~/.umbfyi-tips.env` (see the script header).

Judgement rules live in `references/rules.md`. Read it before every run. It wins over anything general you think you know about the newsletter. Tags are judged by example rather than rule: `references/tags.md` (how each tag has been used, regenerated from past issues) and `references/tag-corrections.md` (Matt's fixes to past runs).

## Run

1. **Find the next issue.** Exactly as in the `weekly-cryptic` skill, step 1: the newsletter under Archive whose `publishDate` is still in the future (compare full UTC date and time, get "now" from `date -u`). Note whether it is already published, and show Matt the send time in UK time.
   - None: stop. Offer to run the `create-newsletter` skill first.
   - More than one: ask which.
   - It already has Newsletter Item blocks: say how many, and carry on. The endpoint skips links already there, so a re-run never doubles up.
2. **Check tips are done.** `umbfyi.sh tips`. Kept tips become media items, and the workflow reads media items, so open tips would be missed. If any are open, say how many and suggest running `process-tips` first. Carry on only if Matt says to.
3. **Run the workflow.** `umbfyi.sh workflow-create` (note `workflowId`), then `umbfyi.sh workflow-start <id>`. Poll `umbfyi.sh workflow-status <id>` every 30 seconds in a single background Bash loop until `status` is no longer `Pending` or `Running`. Give up after 20 minutes and tell Matt.
   - The run lives only in the site's memory. A deploy or restart mid-run loses it: if `workflow-status` starts returning 404, say so and offer to start again.
   - `Failed`: stop, show the error logs, write nothing.
   - `SucceededWithWarnings` or `PartiallyFailed`: carry on. These are normal: the warnings are the workflow's to-do list for this step.
4. **Save the results and flags.** `umbfyi.sh workflow-model <id>` to `items-raw.json` in the scratchpad, and the final `workflow-status` to `status.json`. Never edit either, so there's always a record of what the workflow produced.
   - Collect every log with `level` `Warning` or `Error`: `jq '[.. | objects | select(.level? == "Warning" or .level? == "Error") | {level, message, correlationId}]' status.json`.
   - Tie each one to its item: a per-item log's `correlationId` is `<stage>-<task>-<item id>`, so it ends with the item's `id` from `items-raw.json`. Logs with no item id are about the whole run; list them separately.
   - Flagged items stay in the results; the workflow doesn't drop them. Each flag means something needs fixing or deciding. `references/rules.md` section 0 says what to do for each kind.
5. **Review.** Fix every flag first (rules section 0), then work through the rest of `references/rules.md` item by item. If a festival or big event is on (rules section 10), or it's December and 24 Days is running (section 10a), propose its section in the table. Write your result to `items.json` in the scratchpad: the same items, with your fixes, minus the ones you drop. For each item note what you changed, or why you dropped it. Anything `unsure` gets a one-line reason and is left in for Matt to decide.
6. **Show one table.** Write it as a markdown file in the scratchpad and print it. Header: the newsletter's name, send time, item counts per group, and any run-level warnings. Each flagged item shows its flag (e.g. "⚠️ no read time: set 14 from video length") so Matt can see what the workflow missed and what you did about it. One section per group, in the order the server will put them (newest first; Events and Deadlines soonest first). Columns: `#`, decision (keep / changed / drop / unsure), emoji, title, source, date, mins, tags. Show tags as the workflow had them and as you'd set them (e.g. `ai, ~~search~~, +umbracoai`), as tags are the field most often wrong. Put the summary on a line under each row. For changed rows, show the old value too. Drops at the bottom of each group. Wait for Matt. He may edit rows, flip decisions or say "go". Unsure rows need his decision before anything is written.
7. **Add the items.** Build the request body from the kept items, one object each, with exactly these fields: `link`, `title`, `summary`, `source`, `emoji`, `category`, `date`, `consumptionTimeMinutes`, `contentTags`, plus `cluster` where the rules give one (rules section 8 for packages, 10b for forum release posts). Write it to `items-approved.json` in the scratchpad, then `umbfyi.sh add-items <newsletter-id> items-approved.json`. The server sorts each group and saves a draft.
   - If Matt approved a festival section, create it first: `umbfyi.sh add-group <newsletter-id> <alias> "<title>" "<emoji>"`. It goes at the very top; it's a no-op if the heading is already there. Then send its items with that alias as their `category`.
   - `422` with `missingGroups`: the newsletter has no heading for those categories. Nothing was written. Tell Matt which, and offer to move those items to another group (any existing `groupAlias` works as a `category`) or drop them. Then send again.
   - Any other error: stop and say what was and wasn't done.
8. **Tidy the layout.** `umbfyi.sh tidy <newsletter-id>`. It removes the blueprint's poll if it's still the placeholder, removes headings with nothing under them, moves the first signup block to 3 to 6 items in, at a group end where it can (above the fold on the web) and makes sure the last signup block is last. Report what it did. Removed headings can't take items afterwards, so this goes after the last items are in; if Matt later wants items under a removed heading, he adds the heading back first.
9. **Check it.** Say how many were added and list any `skippedLinks` (already in the newsletter). Then `umbfyi.sh get-newsletter <id>` and confirm the number of `item` blocks went up by that many.
10. **Never publish.** Never publish, schedule or unpublish the newsletter. If it was already published (step 1), tell Matt to publish it again so the items sync to the newsletter system. Finish with one line: how many items went into which newsletter, and whether it needs republishing.
11. **Learn.** If Matt changed any decision or rewrote any field, say which rule it suggests and offer to update `references/rules.md`. Don't edit it without his OK. Tag changes go in `references/tag-corrections.md` instead (one line each: title, your tags, his tags, his reason if given), again with his OK. Every few months, offer to regenerate `references/tags.md` (see the script's header).

## Item fields

What the workflow returns per item, and what each becomes in the block:

| Workflow field | Block field | Notes |
| --- | --- | --- |
| `link` | Link | Must be unique in the newsletter. |
| `title` | Title | |
| `summary` | Description | For events: date, time, time zone and venue. |
| `source` | Source | Author or site URL. |
| `emoji` | Emoji | Defaults to 🔗 if empty. |
| `category` | (which heading) | `Hq`, `Community`, `WatchAndListen`, `Packages`, `Events`, `Deadlines` (the server adds a ⏰ Deadlines heading after the Events items if there isn't one), `Training`, `Social`, `Forum` (forum announcements: package releases, tools, community news), `Misc` (goes under Miscellaneous), or any existing `groupAlias`. `Uncategorized` is never accepted. |
| `date` | (sort order only) | Required. Upcoming items (events, deadlines) sort first, soonest first; past items (posts) after, newest first. |
| `consumptionTimeMinutes` | Read time | 0 for events and packages. |
| `contentTags` | Tags | Lowercased by the server. |
| `cluster` (you add it) | (sort order only) | Developer or company name for packages, `Releases` for forum release posts. Items sharing one are kept together at the bottom of the group, and a cluster of one still goes to the bottom. |

The workflow also returns `description`, `author`, `tags` and others. Those are inputs to the workflow, not block fields; leave them out of the request.

## Learn from history

Use this to improve `references/rules.md` from what Matt actually did. Run it when the rules feel off.

1. Media items are what the workflow reads. `umbfyi.sh recent <from> <to>` for a past issue's window (the 7 days before its Wednesday) gives roughly what the workflow had to work with.
2. `umbfyi.sh featured-all <from>` gives what was actually sent, with the group each item went in.
3. Compare: items in (1) but not (2) were dropped; items in both but under a different title or group were changed. Look for patterns: kinds of item Matt always drops, title clean-ups he always makes, groups he moves things to.
4. Write the patterns as a proposed diff to `references/rules.md`, with a few real examples each. Show Matt. Apply only what he agrees with.
