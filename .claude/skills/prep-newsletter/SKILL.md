---
name: prep-newsletter
description: Prep this week's UMB.FYI newsletter end to end on the live site, in one go. Processes the tips inbox, creates the draft from the blueprint, runs the newsletter workflow, sweeps Bluesky, Mastodon and LinkedIn for anything tips missed, adds the reviewed items, sets the minute cryptic, writes the preheader and LinkedIn post, and checks the draft, stopping for Matt's approval at each step. Publishes early once the issue is complete, and sends the preview link. Use when asked to prep, set up, build or do this week's newsletter, or "do the newsletter".
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
   - The scorecard: each step's result this week and its streak (e.g. "Tips: clean, 3 in a row"). Automatic steps: one line each on what they did. Any step that just qualified: put it on the `Automatic:` line and say so (scorecard rules).

## Phone mode

The Tuesday scheduled task (18:00 UTC: 6pm UK in winter, 7pm in British Summer Time) runs this skill in phone mode in the cloud, and Matt answers from the Claude phone app. Also use phone mode whenever Matt says he's on his phone. The rest of this skill still applies; this changes how you ask, and what you do at the start and end.

- **Start:** `git pull -q`. No site code here (`../UMB.FYI.v17` isn't in the cloud): skip code steps and say so.
- **Automatic steps:** the scorecard's `Automatic:` line lists steps that have earned it. For those, don't wait: apply what you proposed, log an `auto` row, and say what you did in the sum-up. Unsure things in them still need his answer. If he says one got something wrong, it comes off the list (scorecard rules).
- **Where the message goes:** the whole message goes in your chat reply, as that's what Matt reads when he opens the app. If you also send a push notification, it's only a short heads-up ("Tips ready: 6 to check"), and the chat must never say "details above" or point at the notification: its text can't be read once opened.
- **Asking:** one message per approval, in the strict format below. No files, no scratchpad paths, no backoffice steps.
- **Sum-up:** step 9, in the same format: a bold heading, then one numbered row per step, details as sub-bullets.

### Message format (strict)

Every phone message follows this exactly. Don't improvise a different layout.

```
**<Step> · <issue>** · <counts, e.g. 6 tips: 3 keep, 2 drop, 1 unsure>

**Needs you**
1. ✅ [<title>](<link>)
   - Not sure: <what you couldn't settle>
2. ❌ [<title>](<link>)
   - Why: <reason>

**Changed**
3. ✏️ [<title>](<link>)
   - <field>: <old> → <new>

**Keep**
4. ✅ [<title>](<link>)
   - <group> · <source name>

**Reply:** `go` does every call above · `flip 2` · `drop 4` · `1 keep`
```

- **One row = one numbered list item.** Numbers run on through the whole message (not restarting per section), so a reply like `drop 4` is never ambiguous.
- **Every row starts with exactly one emoji: your call.** ✅ yes (keep, add, pick, fix) · ❌ no (drop, skip, leave) · ✏️ keep, with changes. Always make a call, even when unsure: give your best guess and add a `- Not sure: …` sub-bullet saying why. No other emoji to start a row.
- **⚠️ marks a real problem the workflow flagged** (a warning or error in its run, `newsletter-items` step 4), never your own doubts. On the item: a sub-bullet `- ⚠️ <flag>: <what you did about it>`, e.g. `- ⚠️ No read time: set 14 from the video length`. For run-level warnings (no item): one line under the heading, `⚠️ Workflow: <warning>`.
- **Every title is a link** to exactly what would go in the issue (for a drop, the link you looked at). If you weighed two links (tips rule 3), add a sub-bullet `- Other link: [<site>](<url>)`.
- **Details go on indented sub-bullets,** one fact each, never on the title line.
- **Sections in this order,** leaving out empty ones: Needs you (the unsure ones, then drops), Changed (✏️), Keep (✅). Items: put a group sub-heading (`**Umbraco HQ** (5)`) inside Keep. No markdown tables: they're cramped on a phone.
- **Options** (puzzle, preheader): one row per option, your pick first with ✅, the others ❌. Puzzle sub-bullets: `- Answer: <ANSWER>` and `- How: <one-line explanation>`. Preheader sub-bullets: `- Angle: <news|theme|community>` and `- Fits: social <n> lines, Instagram <n>`.
- **Social:** ✅ for ones you'd add, ❌ for the rest, each title linked to the post, sub-bullets `- <platform> · <author>` and `- Why: <reason>`.
- **LinkedIn:** one row, `1. ✅ LinkedIn post · <n> characters`, then the post as it will read in a quote block (`>`) under it.
- **Fixes:** `1. ✅ [<item title>](<item link>)` (✅ fix it, ❌ leave it) with sub-bullets `- Problem: …` and `- Fix: …`.
- **Always end with a bold `Reply:` line** listing the replies you understand, as code spans.
- **The preview link,** once the issue is published, goes as the last line before Reply: `Preview: [umb.fyi/<issue>](https://umb.fyi/<issue>)`.

- **Waiting:** after asking, end your turn. His reply comes back into this session. If it hasn't come by Wednesday 06:45 UK, stop: the 7am top-up will see prep didn't finish and tell him.
- **End:** save the logs to main: `git add .claude/skills/*/references .claude/skills/newsletter-items/history`, commit ("Prep <issue>: logs"), `git push origin HEAD:main`. Only log files, never other changes. If the push fails, say so in one line.

## Keep the scorecard

`references/scorecard.md` records, for each approval step, what was proposed and what Matt approved. It decides which steps run without his OK: steps go automatic on their own once they've earned it, and come back the moment he says one got something wrong (rules in the file). Each skill adds its own row at its approval step. At the start of prep, read it. At the end, check all 7 rows are there for this issue, add any missing one, and update the `Automatic:` line.

## Log Matt's asks

Keep `references/asks.md` as a running log, for learning what prep should do on its own.

- **At the start**, read it. If an ask has come up two or more times with no skill change yet, say so in one line and offer to automate it.
- **During the run**, log every time Matt asks for something the skills didn't do by themselves: a fix, a change, a reorder, a redo, a one-off. Not his normal approvals, picks or "go"s. Add the entry when it's done, so the outcome is real.
- Each entry is a few lines under the issue date: what he asked, what you did, how it turned out, and a suggestion (the skill and step it belongs in, or "one-off" if it doesn't).
- This repo is public. Describe the ask, never paste private data (tips' submitter details, emails, keys).
- Also log asks from a newsletter skill run on its own, outside full prep.
- When a suggestion gets built into a skill, mark the entry `Done: <skill>` so it isn't offered again.

## Rules

- One step at a time, each to its approval. Never batch two skills' approvals into one message, and never treat a "go" for one step as a "go" for the next.
- If a step fails, stop there. Say what's done and what isn't, and which skill to run to pick up from that point. Each skill is safe to re-run: create stops if the issue exists, tips only sees open tips, items skip links already in the issue, and the puzzle, preheader and LinkedIn post ask before replacing what's there.
- If Matt wants to skip a step ("no puzzle this week"), skip it and note it in the summary.
- **Unsure never goes in silently.** An unsure tip, item or social pick goes in only on Matt's answer. If a step has to move on without one (he said "go" but skipped it, or the run is unattended), leave it out and list it in the summary under "Left out, unsure". Unsure tips stay open (not converted, not dismissed), so they come back next week; the tips window's 2-day grace and the workflow's 7-day look-back cover that, and the duplicate checks stop repeats.
- Don't deploy anything during a run. If a skill seems to need a code change, say so and stop that step.
