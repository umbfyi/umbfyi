---
name: newsletter-topup
description: Wednesday morning top-up for the UMB.FYI newsletter, run by the early-morning scheduled task (6am UK in winter, 7am in summer). Finds what's new since Tuesday's prep (tips, workflow items, social posts), checks the issue, applies its own calls and republishes, then sends Matt one short phone message: either "nothing needs you" with the preview link, or only the things it was unsure of. Everything is already done its way; "flip 2" changes one, and no reply means Matt agrees. Use only from the scheduled task, or when Matt asks for the morning top-up.
---

# Newsletter top-up

Tuesday evening's prep (`prep-newsletter`, phone mode) builds the issue. News keeps coming overnight, so this runs early on send day, picks up only what's new, adds what it's sure of, and only asks Matt about the rest.

Everything is on the LIVE site, through `.claude/skills/process-tips/scripts/umbfyi.sh`. Read the phone-mode rules in `prep-newsletter` ("Phone mode") first: they apply here too.

## Run

1. **Note the time.** `TZ=Europe/London date +%H:%M` and `date -u`. The schedule fires once, at 06:00 UTC: 6am UK in winter, 7am in British Summer Time. If it's already 08:45 UK or later (a late or manual run), message Matt that it's too late to top up safely, and stop.
2. **Find the issue.** As in `weekly-cryptic` step 1: the newsletter with a `publishDate` later today. None: message Matt "No issue for today, nothing done" and stop. Note whether it's published: Tuesday's prep publishes it once it's complete.
3. **Did Tuesday's prep finish?** `.claude/skills/newsletter-items/history/<issue>.json` must exist (pull first: `git pull -q`). If it doesn't, Tuesday's prep didn't get as far as the items. Message Matt one line saying which step it stopped at, if you can tell from the issue (no items, no preheader...), and that you've done nothing. Stop.
4. **Find what's new.** Tuesday's record lists every item prep saw (kept, dropped or unsure); none of those is new.
   - **Tips:** `umbfyi.sh tips`. Judge each as `process-tips` does (steps 2 and 3, its rules), but write nothing yet.
   - **Items:** run the workflow as in `newsletter-items` steps 3 and 4. New items are those whose link isn't in the record's `items`. Review only those (step 5 and its rules). Tips you'd keep aren't media items yet, so draft them as items too, the way the workflow would (title, summary, source, emoji, group, date, read time, tags).
   - **Social:** `social-sweep` steps 2 to 5, with the window from Tuesday 18:00 UTC (when prep started, before its own sweep) to now. Its step 4 checks drop what Tuesday already covered. Only posts you'd add.
   - Drop anything already in the issue. Anything unsure still gets your best call, applied in step 6 and shown with a `Not sure:` line.
5. **Check.** Run `check-newsletter` on the draft as it is now. Keep only the problems.
6. **Apply your calls.** Matt only wants to hear about what needs his approval, and no reply means he agrees with your call. So straight away, for sure and unsure ones alike: kept tips become media items and are dismissed (`process-tips` step 6), the new items you'd add go in (`newsletter-items` step 7, then `tidy` and its step 9 checks), and fix the check problems that are clear (a cancelled event comes out with `remove-block`, a changed venue with `edit-item`). Then note what to show Matt: the unsure ones, and fixes that were a judgement call. If `topup` is on the scorecard's `Ask:` line, show everything new. Dropped tips are dismissed as usual: a `flip` builds the item from your own draft.
7. **Republish** if anything changed: `publish-newsletter` steps 2, 4 and 5, no "Publish now?", within its limits.
8. **Message Matt.** One message, in your chat reply (see "Where the message goes" in phone mode), and nothing else. It follows the strict "Message format" in `prep-newsletter`.

   Nothing to show:

   ```
   **Top-up · <issue>** · nothing needs you

   Preview: [umb.fyi/<issue>](https://umb.fyi/<issue>)
   ```

   Something to show:

   ```
   **Top-up · <issue>** · <n> to check, already done my way

   1. ✅ [<title>](<link>)
      - Not sure: <what you couldn't settle>
   2. ✅ [<item title>](<item link>)
      - Problem: <…>
      - Fix: <…>

   Preview: [umb.fyi/<issue>](https://umb.fyi/<issue>)

   **Reply:** `flip 2` to change one, before 8:45. No reply and it goes out as it is.
   ```

   If the issue isn't published (Tuesday's prep didn't get that far), it's a ⚠️ line instead of the preview: "⚠️ Not published yet: reply publish to send it as it is", and treat `yes` as also publishing it, if it's complete (`publish-newsletter` limits).

   **When his reply comes,** get the UK time first. From 08:45 on, nothing happens on its own any more: say "Too close to the send to change it on a reply. Tell me exactly what to change and I'll check with you first." From then on, each change needs his yes for that change (after the send it only updates the web version).
   - `flip <numbers>`: do the opposite of your call for those rows (a ✅ comes out with `remove-block`, a ❌ goes in, a fix is undone), republish, then one line: done, with the preview link.
   - `ok`: nothing to do.
   - "That's wrong" about something you added by yourself: take it out with `remove-block` (or fix it), republish, and put `topup` on the scorecard's `Ask:` line (scorecard rules).
   - Anything else: do or answer it, republish if anything changed.
9. **Save the logs.** Save this morning's own record, like `newsletter-items` step 11 but with this run's files and Tuesday's record as `--seen`, to `history/<issue>-topup.json` (Tuesday's record stays as it was). Add a `topup` row to `.claude/skills/prep-newsletter/references/scorecard.md`: proposed `<n> new, <u> unsure`, result `auto` if nothing was flipped (or `wrong` if he said it got one wrong), else what he flipped. Add any asks to `asks.md`. Commit and push (see "Phone mode" in `prep-newsletter`). Do this just before sending the message in step 8 (no reply may ever come), and again after his reply if anything changed.

If no reply comes, the run just ends: everything is already in as you called it.
