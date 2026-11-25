---
name: newsletter-topup
description: Wednesday morning top-up for the UMB.FYI newsletter, run by the early-morning scheduled task (6am UK in winter, 7am in summer). Finds what's new since Tuesday's prep (tips, workflow items, social posts), checks the issue, and sends Matt one short phone message with the preview link. His reply "yes" adds the new items and republishes, "drop 2 4" adds the rest, "no" adds nothing. No reply means the issue goes out as Tuesday's prep left it. Use only from the scheduled task, or when Matt asks for the morning top-up.
---

# Newsletter top-up

Tuesday evening's prep (`prep-newsletter`, phone mode) builds the issue. News keeps coming overnight, so this runs early on send day, picks up only what's new, and asks Matt one question from his phone.

Everything is on the LIVE site, through `.claude/skills/process-tips/scripts/umbfyi.sh`. Read the phone-mode rules in `prep-newsletter` ("Phone mode") first: they apply here too.

## Run

1. **Note the time.** `TZ=Europe/London date +%H:%M` and `date -u`. The schedule fires once, at 06:00 UTC: 6am UK in winter, 7am in British Summer Time. If it's already 08:45 UK or later (a late or manual run), message Matt that it's too late to top up safely, and stop.
2. **Find the issue.** As in `weekly-cryptic` step 1: the newsletter with a `publishDate` later today. None: message Matt "No issue for today, nothing done" and stop. Note whether it's published: Tuesday's prep publishes it once it's complete.
3. **Did Tuesday's prep finish?** `.claude/skills/newsletter-items/history/<issue>.json` must exist (pull first: `git pull -q`). If it doesn't, Tuesday's prep didn't get as far as the items. Message Matt one line saying which step it stopped at, if you can tell from the issue (no items, no preheader...), and that you've done nothing. Stop.
4. **Find what's new.** Tuesday's record lists every item prep saw (kept, dropped or unsure); none of those is new.
   - **Tips:** `umbfyi.sh tips`. Judge each as `process-tips` does (steps 2 and 3, its rules), but write nothing yet.
   - **Items:** run the workflow as in `newsletter-items` steps 3 and 4. New items are those whose link isn't in the record's `items`. Review only those (step 5 and its rules). Tips you'd keep aren't media items yet, so draft them as items too, the way the workflow would (title, summary, source, emoji, group, date, read time, tags).
   - **Social:** `social-sweep` steps 2 to 5, with the window from Tuesday 18:00 UTC (when prep started, before its own sweep) to now. Its step 4 checks drop what Tuesday already covered. Only posts you'd add.
   - Drop anything already in the issue. Anything `unsure` is left out (it rolls to next week) and listed.
5. **Check.** Run `check-newsletter` on the draft as it is now. Keep only the problems.
6. **Message Matt.** One message, in this shape, and nothing else:

   ```
   UMB.FYI <issue>: <n> new since last night.

   1. <title> (<group>, <source name>)
   2. ...

   Left out, unsure: <title> (<reason>); ...
   Check: ready. | Check: <problem, one line each>
   Preview: https://umb.fyi/<issue>

   Reply yes to add them, drop 2 4 to add the rest, or no to add none. No reply by 8:45 and it goes out as it is.
   ```

   If the issue isn't published (Tuesday's prep didn't get that far), say so in place of the preview line: "Not published yet: reply publish to send it as it is", and treat `yes` or `drop` as also publishing it, if it's complete (`publish-newsletter` limits).

   Nothing new: "UMB.FYI <issue>: nothing new since last night. Check: ready. Preview: <link>". No question then, unless there's a check problem to fix: then "Reply fix to fix it."  Leave out lines that would be empty.
7. **Wait for his reply.** When it comes, get the UK time first. After 08:45: don't act. Say "Too late to change it safely. It goes out as it is." and stop.
   - `yes`, or `drop <numbers>`: for kept tips, create the media item and dismiss the tip (`process-tips` step 6). Add the items (`newsletter-items` step 7, then `tidy` and its step 9 checks). Fix any check problems that `edit-item` or `move-block` can fix. Then republish (below).
   - `no`: add nothing, and leave the new tips open (they roll to next week). Nothing to republish.
   - `fix`: fix what you can, then republish.
   - Anything else (a change, a question): do or answer it, republish if anything changed, then ask again.
8. **Republish.** `publish-newsletter` steps 2, 4 and 5, no "Publish now?", within its limits. If a check problem is still open, say so in the same message.
9. **Save the logs.** Save this morning's own record, like `newsletter-items` step 11 but with this run's files and Tuesday's record as `--seen`, to `history/<issue>-topup.json` (Tuesday's record stays as it was). Add a `topup` row to `.claude/skills/prep-newsletter/references/scorecard.md`: proposed `<n> new, <u> unsure`, result `clean` if he said yes, else what he dropped or `no`. Add any asks to `asks.md`. Commit and push (see "Phone mode" in `prep-newsletter`).
10. **Finish.** One line to Matt: republished, the preview link, how many items went in this morning.

If no reply comes, the run just ends. Nothing is added, and the issue goes out at 9am as Tuesday's prep left it.
