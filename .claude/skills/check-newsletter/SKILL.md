---
name: check-newsletter
description: Look over this week's UMB.FYI newsletter draft on the live site before Matt publishes it. Read-only: checks the name and send time, preheader fit, puzzle, items (missing fields, broken links, repeats, past events, tag counts) and layout, then reports one checklist. Use when asked to check, review, QA or look over the newsletter before publishing, or as the last step of newsletter prep.
---

# Check newsletter

A final look over the draft before Matt publishes. **Read-only: never change anything.** Report what's wrong and which skill or step would fix it; Matt decides.

Calls: `.claude/skills/process-tips/scripts/umbfyi.sh` (`newsletters`, `get-newsletter`, `og-measure`, `featured`). All on the LIVE site, all reads.

## Run

1. **Find the issue.** As in `weekly-cryptic` step 1: the newsletter whose `publishDate` is still in the future. `umbfyi.sh get-newsletter <id>` gives its fields and every block in page order. Note whether it's published already (then anything fixed needs a republish).
2. **Check, in this order.** For each, pass or a one-line problem.
   - **Name and send time.** The name is its Wednesday (`YYYY-MM-DD`); `publishDate` is 9am UK on that day, stored as UTC (`08:00:00` in British Summer Time, `09:00:00` in winter). Say how long until it goes out.
   - **Preheader.** Set, in the `A, B, C and much more...` form, and `umbfyi.sh og-measure` gives 4 lines or fewer on the social image (`image1200x627`), 7 or fewer on Instagram (`image1080`), and no word alone on a social line. Fix: `newsletter-preheader`.
   - **Puzzle.** The minute cryptic block is filled, or Matt skipped it this week (an empty one is hidden, so that's fine, just say so). Fix: `weekly-cryptic`.
   - **Placeholders.** No poll still saying `[CHANGE ME]`, no heading with nothing under it. Fix: `umbfyi.sh tidy`.
   - **Signup blocks.** The first one is 3 to 6 items in, but judge by length, not count: it should sit above the fold, so after long items (HQ posts with long summaries) it goes nearer 3 than 6. Tidy now judges this by length too, so it should be right; if it still looks too low, say how many items higher it should go (a drag in the backoffice). The last block in the issue is a signup block. Fix: `umbfyi.sh tidy`.
   - **Items.** Each has a title, link and source. Posts and videos have a real summary and a read time above 0; social posts and forum release posts have no summary (a forum write-up has one); packages have a one-sentence summary. No summary speaks in the first person ("we", "our", "I", "my"): UMB.FYI tells readers about other people's news, so it names who it is. Titles stay as written. No item has more than 3 tags. No link appears twice.
   - **Repeats.** No item's link was in the last issue (`umbfyi.sh featured <link>`). `featured` also matches this issue itself, so ignore results whose `newsletterDate` is this issue's. Events and training sessions still upcoming are fine: events usually run in two issues.
   - **Events.** Every event (and deadline) is after the send time and no later than the Friday after it.
   - **Links.** Fetch every item link. Anything that's gone (404, 410, a domain that doesn't resolve) is a problem. Sites that block automated requests (LinkedIn, Meetup and others often do: 403, 429, 999) are "couldn't check", not broken.
3. **Report.** One checklist: ✅ for each passing check on one line, then each problem as a bullet with the item's title (not its id) and the fix. End with one line: ready to publish, or how many things to fix first. Don't fix anything, even small things, unless Matt then asks.
