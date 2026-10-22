---
name: create-newsletter
description: Create the next UMB.FYI newsletter on the live site from the "Newsletter Starter" blueprint, named for its Wednesday and set to go out at 9am UK time. Saves a draft and never publishes. Use when asked to create, start, set up or make this week's or next week's newsletter or issue, or as the first step of newsletter prep.
---

# Create newsletter

Every issue starts as a copy of the "Newsletter Starter" blueprint: the group headings, the signup blocks, the empty puzzle block and a placeholder poll. This skill makes that copy for the next Wednesday, as the backoffice's "Create > Newsletter Starter" does.

All calls go through `.claude/skills/process-tips/scripts/umbfyi.sh`. It talks to the LIVE site. If credentials are missing, stop and tell Matt to set up `~/.umbfyi-tips.env`, or on Claude on the web the environment variables (see the script header).

## Run

1. **Find the newest issue.** `umbfyi.sh newsletters` lists the newest few under Archive, newest first, with each one's `publishDate` and state. Newsletters are named by their date (`YYYY-MM-DD`).
2. **Work out the date.** Get today from `date -u`. The new issue is the coming Wednesday: today if today is a Wednesday (Matt often preps on the morning it goes out), otherwise the next one. Normally that's the newest issue plus 7 days.
   - If an issue for that Wednesday, or any later one, already exists: stop. Say which one, and that there's nothing to create.
   - If the newest issue is more than a week old (a skipped week), say so, and that the new one will be for the coming Wednesday rather than the missed one.
3. **Create it.** `umbfyi.sh create-newsletter <YYYY-MM-DD>`. It copies the blueprint with fresh block ids and lets the site fill in its own defaults (`SetNewsletterDefaultValuesNotificationHandler`): the name is the coming Wednesday (today, if run on a Wednesday, as issues are often prepped that morning), and `publishDate` is 9am Europe/London stored as UTC (`08:00:00` in British Summer Time, `09:00:00` in winter). It sets the newsletter template and saves a draft under Archive. If the site's date doesn't match the one you worked out, it creates nothing and says what the site would have used: tell Matt, don't work around it.
   - Never "fix" the send time to 09:00 in summer. The backoffice shows the raw UTC value, so 08:00 is right then.
4. **Check it.** `umbfyi.sh get-newsletter <new id>`. Confirm the name, the `publishDate`, and that it's a draft. If anything's off, say what, and don't try to fix it by hand.
5. **Never publish.** Publishing syncs the issue to the mailing system, so it's Matt's call. Finish with one line: the new issue's name, when it goes out in UK time, and that it's a draft.

## Notes

- Keys (same on local and live, as Umbraco Deploy keeps them): blueprint `6febf968-81f4-43cf-972a-0a5293a49db9`, Archive `028b21ee-6da5-4e54-b6cd-e73f6c33b85b`, newsletter template `addcb633-ddfc-4539-a6c8-6a9365d0b322`. They live in the script.
- The preheader is left empty. It's written once the items are in.
- The poll and any headings left empty are cleaned up later by `newsletter-items` (its tidy step).
