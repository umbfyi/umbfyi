---
name: newsletter-close
description: Close the open decisions from this week's UMB.FYI phone runs, after the newsletter has gone out. Dismisses the unsure tips the Tuesday prep and Wednesday top-up would drop but left open for Matt to flip, since no flip by the send means he agreed. Run by the Wednesday 09:15 UTC scheduled task, or when Matt asks to close the week's open tips.
---

# Close the week

The phone runs (`prep-newsletter` phone mode, `newsletter-topup`) apply their own calls, but an unsure tip they'd drop stays open, so Matt can still `flip` it and have it go in. He can flip until 08:45 UK on send day. After the send, no flip means the drop stands, and this closes them.

Everything is on the LIVE site, through `.claude/skills/process-tips/scripts/umbfyi.sh`. Quiet by design: no message to Matt unless something is blocked.

## Run

1. **Pull and note the time.** `git pull -q`, `date -u`. If it's before 09:00 UK on a Wednesday, stop: the send hasn't happened, so Matt can still flip.
2. **Find the issue.** The newest newsletter whose `publishDate` has passed (`umbfyi.sh newsletters`). Its name is `<issue>`.
3. **Close.** Read `.claude/skills/newsletter-items/history/<issue>-open-tips.json`. Missing or empty: nothing to do, stop quietly. Otherwise get the open tips (`umbfyi.sh tips`), and for each listed tip that's still open, `umbfyi.sh dismiss <id>`. One no longer open (Matt flipped it, or it was handled) is skipped. Then write `[]` to the file.
4. **Save.** `git add .claude/skills/newsletter-items/history`, commit ("Close <issue>: open tips"), `git push origin HEAD:main`. Only that folder.
5. **Finish.** No message to Matt when it worked. If a dismiss, the site or the push failed, one line in your chat reply: `⚠️ Close · <issue>: <what failed>: <what it means>` (e.g. "2 tips still open, they'll come back in next week's tips").
