---
name: prep-newsletter
description: Prep this week's UMB.FYI newsletter end to end on the live site, in one go. Processes the tips inbox, creates the draft from the blueprint, runs the newsletter workflow, sweeps Bluesky, Mastodon and LinkedIn for anything tips missed, adds the reviewed items, sets the minute cryptic, writes the preheader, and checks the draft, stopping for Matt's approval at each step. Never publishes. Use when asked to prep, set up, build or do this week's newsletter, or "do the newsletter".
---

# Prep newsletter

Runs the five newsletter skills in order, as one session. Each skill keeps its own rules and its own approval step; this skill only sequences them, skips what's already done, and sums up at the end. Load each skill with the Skill tool when its turn comes and follow it exactly.

All five talk to the LIVE site. Nothing is ever published: the issue stays a draft, and publishing (which syncs it to the mailing system) is Matt's job.

## Run

1. **Tips.** Run `process-tips` first, as Matt does. If the inbox is empty, say so in one line and move on. The workflow reads the media items that kept tips become, so this step must finish (approved and applied) before step 3 starts.
2. **The issue.** Run `create-newsletter`. If this week's issue already exists, that's fine: note its id and carry on with it. If it goes out today (the run started on send day), say so up front with the time left, and again more firmly if it's less than an hour away.
3. **Start the workflow.** Run `newsletter-items` up to and including its step 3: the workflow is now running in the background. Its tips check (its step 2) will pass, since step 1 here just cleared them.
4. **Puzzle, while the workflow runs.** Run `weekly-cryptic` now, rather than waiting. The workflow takes several minutes, and the puzzle needs Matt's pick anyway. If the puzzle is already filled, skip it unless Matt wants a new one. If the workflow finishes mid-puzzle, finish the puzzle first.
5. **Items.** Carry on with `newsletter-items` from its step 4: save the results and review them (its steps 4 and 5, which write `items.json`).
   - Then run `social-sweep`. Its picks, once Matt approves them, go into `items.json`, so they appear in the review table and go in with everything else. It covers Bluesky, Mastodon and LinkedIn.
   - Then carry on from `newsletter-items` step 6: show the table, wait for Matt's go, add the items, tidy, check. Tidy goes last on purpose: once the puzzle and items are in, no more blocks are coming.
6. **Preheader.** Run `newsletter-preheader`, now that the items are in.
7. **Check.** Run `check-newsletter` on the finished draft. If it finds problems, list them with their fixes and ask Matt which to fix; run only those.
8. **Sum up.** One short message:
   - The issue's name and when it goes out (UK time).
   - What each step did, one line each (e.g. "Tips: 4 kept, 2 dropped", "Sweep: 2 added from Bluesky", "Items: 31 added, 2 skipped, Deadlines heading added", "Puzzle: CACHE").
   - Anything still open: unsure rows Matt deferred, workflow warnings not resolved.
   - The preheader as saved, and the check result (ready, or what's still to fix).
   - What's left for Matt: look over the draft in the backoffice, and publish (in the backoffice, or by telling Claude to publish, which runs `publish-newsletter`).
   - Any rule or tag corrections offered during the run that Matt hasn't answered yet.

## Rules

- One step at a time, each to its approval. Never batch two skills' approvals into one message, and never treat a "go" for one step as a "go" for the next.
- If a step fails, stop there. Say what's done and what isn't, and which skill to run to pick up from that point. Each skill is safe to re-run: create stops if the issue exists, tips only sees open tips, items skip links already in the issue, and the puzzle and preheader ask before replacing what's there.
- If Matt wants to skip a step ("no puzzle this week"), skip it and note it in the summary.
- Don't deploy anything during a run. If a skill seems to need a code change, say so and stop that step.
