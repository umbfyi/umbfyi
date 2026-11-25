---
name: publish-newsletter
description: Publish this week's UMB.FYI newsletter on the live site, which syncs it to the mailing system. Only when Matt explicitly says to publish (e.g. "publish the newsletter", "publish it", "go live"). Never as part of prep, checking or any other skill, and never on Claude's own suggestion.
---

# Publish newsletter

Publishing is what syncs the issue to the mailing system, which sends it at its `publishDate` (the site hides it until then). That's outward-facing, so this runs when Matt says "publish" in his own words. The exception is the early publish: before the send time the site keeps the issue out of listings (only its own address shows it), and each republish just updates the mailing system. So `prep-newsletter` and `newsletter-topup` run steps 2, 4 and 5 themselves (no step 3), within these limits:

- Only the upcoming issue (the one whose `publishDate` is later than now).
- Only before 08:45 UK on send day, and never once `publishDate` has passed.
- Only a complete issue: items in, `tidy` done, preheader set. A half-built issue is never published, as it would go out at 9am if prep stopped there.

Other skills never call it, and never offer to as a next step.

All calls go through `.claude/skills/process-tips/scripts/umbfyi.sh`. It talks to the LIVE site. If credentials are missing, stop and tell Matt to set up `~/.umbfyi-tips.env`, or on Claude on the web the environment variables (see the script header).

## Run

1. **Find the issue.** As in `weekly-cryptic` step 1: `umbfyi.sh newsletters`, and the target is the newsletter whose `publishDate` is still in the future. If Matt named one, use that. None, or more than one: ask which.
2. **Quick check.** `umbfyi.sh get-newsletter <id>`. Note, each in one line: the name, the send time in UK time (`publishDate` is UTC), the state, the preheader (or that it's empty), the number of items, and whether the puzzle is filled. If the send time has already passed, say so up front: publishing now may send it straight away. If `check-newsletter` hasn't been run in this session, offer it, but don't insist.
3. **Wait for go.** Show the lines from step 2 and ask "Publish now?". Matt's earlier "publish" counts as the request, not the go: wait for a clear yes to this.
4. **Publish.** `umbfyi.sh publish-newsletter <id>`. It refuses anything that isn't a newsletter, does nothing if there are no unpublished changes, and checks the state reads back as published.
5. **Finish.** Get "now" from `date -u` again. Then, one line each:
   - Which issue is now published and when it goes out in UK time.
   - Its address: `https://umb.fyi/<name>` (e.g. `https://umb.fyi/2026-11-18`). It shows on the site from the send time.
   - How long the prep took: from the prep run's start time (noted by `prep-newsletter` at its start, or else the first `date -u` of the prep in this session) to now, in minutes. If prep didn't run in this session, leave this line out rather than guess.

   If it failed (for example the API user isn't allowed to publish), say what the error was and that the issue is still unpublished, and suggest publishing from the backoffice.

Never unpublish, schedule or delete. If Matt wants one of those, he does it in the backoffice.
