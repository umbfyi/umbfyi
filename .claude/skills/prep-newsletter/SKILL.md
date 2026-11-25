---
name: prep-newsletter
description: Prep this week's UMB.FYI newsletter end to end on the live site, in one go. Processes the tips inbox, creates the draft from the blueprint, runs the newsletter workflow, sweeps Bluesky, Mastodon and LinkedIn for anything tips missed, adds the reviewed items, sets the minute cryptic, writes the preheader and LinkedIn post, and checks the draft, stopping for Matt's approval at each step (in phone mode, it runs straight through and asks only what it's unsure of). Publishes early once the issue is complete, and sends the preview link. Use when asked to prep, set up, build or do this week's newsletter, or "do the newsletter".
---

# Prep newsletter

Runs the newsletter skills in order, as one session. Each skill keeps its own rules and its own approval step; this skill only sequences them, skips what's already done, and sums up at the end. Load each skill with the Skill tool when its turn comes and follow it exactly.

All of them talk to the LIVE site. Nothing is published until the issue is complete (step 8). Then it's published early: the site keeps it out of listings until its send time, and each republish before then just updates the mailing system. Limits in `publish-newsletter`.

## Run

0. **Note the start time.** Run `date -u` and keep the time: `publish-newsletter` uses it to say how long the prep took.
1. **Tips.** Run `process-tips` first, as Matt does. If the inbox is empty, say so in one line and move on. The workflow reads the media items that kept tips become, so this step must finish (approved and applied) before step 3 starts.
2. **The issue.** Run `create-newsletter`. If this week's issue already exists, that's fine: note its id and carry on with it. If it goes out today (the run started on send day), say so up front with the time left, and again more firmly if it's less than an hour away.
3. **Start the workflow.** Run `newsletter-items` up to and including its step 3: the workflow is now running in the background. Its tips check (its step 2) will pass, since step 1 here just cleared them.
4. **Puzzle and sweep, while the workflow runs.** The workflow takes a few minutes, so use them:
   - Hand `social-sweep` to one background subagent (the Agent tool, general-purpose). Tell it to load that skill and do steps 1 to 4, except the check against this week's items (the workflow hasn't finished), and to write its shortlist (at most 15, best first, each with platform, author, link to use, one-line English summary, date and why) to `sweep.json` in the scratchpad, then stop. It must not add anything to the site or ask Matt anything. Filtering 150+ LinkedIn posts is slow reading, so this keeps it off the main thread while the puzzle runs.
   - Run `weekly-cryptic` now, rather than waiting. The puzzle needs Matt's pick anyway. If the puzzle is already filled, skip it unless Matt wants a new one. If the workflow finishes mid-puzzle, finish the puzzle first.
5. **Items.** Carry on with `newsletter-items` from its step 4: save the results and review them (its steps 4 and 5, which write `items.json`).
   - Then finish `social-sweep` from `sweep.json`: drop what the workflow's results (`items.json`) already cover, check the rest against the tips rules, and show the list (its step 6). If the subagent failed or hasn't finished, run the sweep here instead. Its picks, once Matt approves them, go into `items.json`, so they appear in the review table and go in with everything else.
   - Then carry on from `newsletter-items` step 6: show the table, wait for Matt's go, add the items, tidy, check. Tidy goes last on purpose: once the puzzle and items are in, no more blocks are coming.
6. **Preheader.** Run `newsletter-preheader`, now that the items are in.
   - **Publish early.** The issue is now complete (items, tidy, preheader), so publish it: `publish-newsletter` steps 2, 4 and 5, no "Publish now?". Send the preview link, `https://umb.fyi/<issue>`, with the next message. From here on, republish after every change (LinkedIn post, fixes), and say so in one line with the link. Skip all of this, and say so, if it's 08:45 UK or later on send day.
7. **LinkedIn post.** Run `newsletter-linkedin`. It builds on the preheader picks, so it comes straight after.
8. **Check.** Run `check-newsletter` on the finished draft. If it finds problems, list them with their fixes and ask Matt which to fix; run only those. Fix items yourself with `umbfyi.sh edit-item`, `move-block` and `remove-block`, never by asking Matt to do it in the backoffice. If any item was fixed, re-run `newsletter-items` step 11 so its saved record matches what goes out. Then add the `fixes` row to the scorecard (see below); `clean` with 0 found if the check passed.
9. **Sum up.** One short message:
   - The issue's name and when it goes out (UK time).
   - What each step did, one line each (e.g. "Tips: 4 kept, 2 dropped", "Sweep: 2 added from Bluesky", "Items: 31 added, 2 skipped, Deadlines heading added", "Puzzle: CACHE").
   - Anything still open: unsure rows Matt deferred, workflow warnings not resolved.
   - The preheader as saved, the LinkedIn post's hook line, and the check result (ready, or what's still to fix).
   - The preview link, `https://umb.fyi/<issue>`, and that it's published and will go out at the send time as it stands.
   - What's left for Matt: look over the preview. Any change he asks for is made and republished, up to 08:45 UK on send day.
   - Any rule or tag corrections offered during the run that Matt hasn't answered yet.
   - The asks logged this run (see below), each with where it could be automated. One line each.
   - The scorecard: each step's result this week and its streak (e.g. "Tips: clean, 3 in a row"). Any step that just came off the `Ask:` line: say so (scorecard rules).

## Phone mode

The Tuesday scheduled task (18:00 UTC: 6pm UK in winter, 7pm in British Summer Time) runs this skill in phone mode in the cloud, and Matt answers from the Claude phone app. Also use phone mode whenever Matt says he's on his phone. The rest of this skill still applies; this changes how you ask, and what you do at the start and end.

Matt only wants to hear about what needs his approval (25-11-2026). Everything you're sure of goes straight in. It's normal, and fine, for a run to need nothing from him.

- **Start:** `git pull -q`. No site code here (`../UMB.FYI.v17` isn't in the cloud): skip code steps and say so.
- **Run straight through, no stops.** Do every step in order without waiting. At each skill's approval step, apply your own calls as if Matt had said go: keep and drop tips, add the items and social picks you'd add, take your top pick for the puzzle, preheader and LinkedIn post, and make the check fixes. Log each step's scorecard row as `auto`.
- **Unsure things get your call too, applied straight away,** then shown to Matt: anything you're not sure of (a tip, item or social post; a fix that's a judgement call), and any step on the scorecard's `Ask:` line. No reply means he agrees (Matt, 25-11-2026), so the issue is always complete as it stands. One exception: an unsure tip you'd drop stays open for now, so a `flip` can still convert it. List these in `.claude/skills/newsletter-items/history/<issue>-open-tips.json` (`[{"id", "link", "title"}]`, nothing about who sent it), and take a tip off the list if Matt flips it. The `newsletter-close` run after the send closes the rest: no flip by then means he agreed, so it dismisses them.
- **Publish** once the issue is complete (step 6), as usual.
- **One message at the end,** in your chat reply, in the format below. Nothing else: no per-step messages, no sum-up of what you did. The preview is how he checks the rest.
- **Where the message goes:** the whole message goes in your chat reply, as that's what Matt reads when he opens the app. If you also send a push notification, it's only a short heads-up ("Prep done: 2 need you"), and the chat must never say "details above" or point at the notification: its text can't be read once opened.
- **No files, no scratchpad paths, no backoffice steps** in anything he sees.

### Message format (strict)

Every phone message follows this exactly. Don't improvise a different layout.

**Before every line, ask: do I need to bother Matt with this?** Only things that need his approval go in. Things you added, dropped, fixed or checked stay out, and so does how you got there.

**When nothing needs him,** the whole message is:

```
**Prep · <issue>** · nothing needs you

Preview: [umb.fyi/<issue>](https://umb.fyi/<issue>)
```

**When something does,** each row must be complete, so he can decide in one look without opening anything else: your call (the emoji), the link, and just enough context to decide (why, and what happens if he says nothing). As short as possible, but plain: whole words, no shorthand.

```
**Prep · <issue>** · <n> to check, already done my way

1. ✅ [<title>](<link>)
   - Not sure: <what you couldn't settle>
2. ❌ [<title>](<link>)
   - Not sure: <what you couldn't settle>

Preview: [umb.fyi/<issue>](https://umb.fyi/<issue>)

**Reply:** `flip 2` to change one. No reply and it stays as it is.
```

- **One row = one numbered list item,** numbers running on through the whole message, so a reply like `flip 2` is never ambiguous.
- **Every row starts with exactly one emoji: your call.** ✅ yes (keep, add, fix) · ❌ no (drop, leave) · ✏️ yes, with changes. Always make a call, even when unsure, with a `- Not sure: …` sub-bullet saying why. No other emoji to start a row.
- **⚠️ is only for something blocking the run**: a step that failed or can't go on (the workflow failed, the site or a feed won't answer, a save or publish was refused, the logs couldn't be pushed). One line under the heading, `⚠️ <what's blocked>: <what it means>`. Send it straight away, don't wait for the end.
- **Every title is a link** to exactly what would go in the issue (for a drop, the link you looked at). If you weighed two links (tips rule 3), add `- Other link: [<site>](<url>)`.
- **Details go on indented sub-bullets,** one fact each, never on the title line. No markdown tables.
- **`Ask:` steps** (only if on that line): options (puzzle, preheader) get one row each, the one you put in first with ✅, others ❌, sub-bullets `- Answer:` / `- How:` or `- Angle:` / `- Fits:`; reply `pick 3` swaps. LinkedIn: one ✅ row, then the post as a quote block (`>`); reply `edit: …`. Fixes: `- Problem:` and `- Fix:`.
- **Always end with the Preview line, then a bold `Reply:` line** listing the replies you understand, as code spans. (Not in the "nothing needs you" message: that ends at the preview.)

- **Reply:** `flip <numbers>` does the opposite of your call for those rows: a ✅ comes out (`remove-block`), a ❌ goes in (kept tips become media items, items go in, `tidy`, checks), a fix is undone. `pick 3` swaps an option, `edit: …` changes the LinkedIn post. Republish, update that step's scorecard row (what changed), then one line: done, with the preview link. `ok` or no reply: nothing to do, rows stay `auto`.
- **Waiting:** after the message, end your turn. His reply, if any, comes back into this session. From 08:45 UK on send day, follow the after-send rule (each change needs his yes).
- **"That's wrong":** if Matt says something you did by yourself was wrong, fix it, republish, and follow the scorecard's "Coming back" rule (that step goes on the `Ask:` line).
- **End:** save the logs to main: `git add .claude/skills/*/references .claude/skills/newsletter-items/history`, commit ("Prep <issue>: logs"), `git push origin HEAD:main`. Only log files, never other changes. Do this just before sending the end message (no reply may ever come), and again after his reply if anything changed. If the push fails, that's a ⚠️ line.

## Keep the scorecard

`references/scorecard.md` records, for each step, what was proposed and what Matt changed. In phone mode every step runs by itself, except those on its `Ask:` line: a step goes there the moment Matt says it got something wrong, and comes off again once it has earned it (rules in the file). Each skill adds its own row at its approval step. At the start of prep, read it. At the end, check all 7 rows are there for this issue, add any missing one, and update the `Ask:` line.

## Log Matt's asks

Keep `references/asks.md` as a running log, for learning what prep should do on its own.

- **At the start**, read it. If an ask has come up two or more times with no skill change yet, say so in one line and offer to automate it.
- **During the run**, log every time Matt asks for something the skills didn't do by themselves: a fix, a change, a reorder, a redo, a one-off. Not his normal approvals, picks or "go"s. Add the entry when it's done, so the outcome is real.
- Each entry is a few lines under the issue date: what he asked, what you did, how it turned out, and a suggestion (the skill and step it belongs in, or "one-off" if it doesn't).
- This repo is public. Describe the ask, never paste private data (tips' submitter details, emails, keys).
- Also log asks from a newsletter skill run on its own, outside full prep.
- When a suggestion gets built into a skill, mark the entry `Done: <skill>` so it isn't offered again.

## Rules

- One step at a time, each to its approval (in phone mode, see there instead). Never batch two skills' approvals into one message, and never treat a "go" for one step as a "go" for the next.
- If a step fails, stop there. Say what's done and what isn't, and which skill to run to pick up from that point. Each skill is safe to re-run: create stops if the issue exists, tips only sees open tips, items skip links already in the issue, and the puzzle, preheader and LinkedIn post ask before replacing what's there.
- If Matt wants to skip a step ("no puzzle this week"), skip it and note it in the summary.
- **Unsure never goes in silently.** An unsure tip, item or social pick is always shown to Matt with your call. On a laptop run it goes in only on his answer; if a step has to move on without one (he said "go" but skipped it), leave it out and list it in the summary under "Left out, unsure". In phone mode your call is applied and shown, and no reply means he agrees (see Phone mode). Unsure tips stay open (not converted, not dismissed), so they come back next week; the tips window's 2-day grace and the workflow's 7-day look-back cover that, and the duplicate checks stop repeats.
- Don't deploy anything during a run. If a skill seems to need a code change, say so and stop that step.
