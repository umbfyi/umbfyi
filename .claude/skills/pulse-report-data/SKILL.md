---
name: pulse-report-data
description: Get the data for the yearly UMB.FYI Pulse Check report. Runs the state-of-umbraco workflow on the live site, saves the JSON, checks it for known quirks and compares the headline numbers with last year's report. Read-only on the site. Use when asked to run the pulse report workflow, get or refresh the pulse report data, or as the first step of writing the Pulse Check.
---

# Pulse report data

This does what the Pulse Report dashboard does in the backoffice (Settings → Pulse Report): run the `state-of-umbraco` workflow and keep its JSON. The difference is that the data gets checked before anyone writes from it.

All calls go through `.claude/skills/process-tips/scripts/umbfyi.sh` (run it with no args for usage). It talks to the LIVE site. The workflow only reads published newsletters, so running it needs no sign-off. If credentials are missing, stop and tell Matt to set up `~/.umbfyi-tips.env`, or on Claude on the web the environment variables (see the script header).

The workflow's own docs live in the old v13 repo at `../UMB.FYI.v13/Workflow_Documentation.md`. The code is in `src/Umb.Fyi/Workflows/Implement/PulseReport/` in the Umbraco Cloud repo, checked out next to this one at `../UMB.FYI.v17`. If that folder isn't there (as on Claude on the web), skip steps 2 and 3, and say so in one line.

## Run

1. **Check it's a good day.** Never on a Wednesday (newsletter day, see the memory on deploys). Get the day from `date`. On a Wednesday, stop and suggest another day.
2. **Check for anything new the code doesn't know.** Some lists in the workflow (products, festivals, event types, tag merges, newsletter groups) are hand-written, so this year's new things can be missed. Follow `references/coverage.md` and show its one table. If Matt wants changes, make them in the code and stop here: they need shipping before the run (next step). If nothing's missing, say so in one line and carry on.
3. **Check live has the latest code.** `git status` and `git log origin/master..master` on the PulseReport folder. If there are unsaved or unpushed changes under `src/Umb.Fyi/Workflows/Implement/PulseReport/`, live is running older code. Say so in one line and ask Matt whether to carry on or ship first. Pushing master deploys to live straight away, so never push without his go.
4. **Pick the period.** The workflow always ends the period today (UTC) and compares it with the 12 months before. Say both ranges in DD-MM-YYYY. If Matt wants a different end date, stop: that needs a code change in `DefinePeriodsTask`.
5. **Run the workflow.** `umbfyi.sh workflow-create state-of-umbraco` (note `workflowId`), then `umbfyi.sh workflow-start <id>`. Poll `umbfyi.sh workflow-status <id>` every 30 seconds in a single background Bash loop until `status` is no longer `Pending` or `Running`. Give up after 30 minutes and tell Matt.
   - The run lives only in the site's memory. A deploy or restart mid-run loses it: if `workflow-status` starts returning 404, say so and offer to start again.
   - `Failed`: show the failing task and its message from the status, then stop.
   - `SucceededWithWarnings` or `PartiallyFailed`: carry on, but list the warnings in step 8.
6. **Save it.** `umbfyi.sh workflow-model <id>` to `pulse-report-YYYY-MM-DD.json` in the scratchpad, and the final status to `pulse-report-status.json`. Never edit either. Give Matt the full path of the JSON.
7. **Check for known quirks.** Read `references/quirks.md` and run each check in it. For each, note how many items it touches and a few examples.
8. **Show one summary.** A short table of headline numbers, this period against the comparison period, using the same rows as last year's "Year in brief" table (see `references/quirks.md`, "Headline numbers"). Under it: the run's warnings, then each quirk found with its count. Stop there. Fixing data is Matt's call, usually by fixing the newsletter item on the site and running again.

## After

If Matt asks for the report itself, hand over to the `pulse-report-draft` skill with the JSON path.
