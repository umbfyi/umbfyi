---
name: newsletter-linkedin
description: Write the LinkedIn post for this week's UMB.FYI newsletter on the live site. Drafts a short post from the issue's top items, shows it to Matt, and saves it to the issue's "LinkedIn Post" field (Social tab) once he approves. Make.com posts it to the UMB.FYI LinkedIn page when the issue is sent. Never publishes. Use when asked for the LinkedIn post or LinkedIn text, or as part of newsletter prep, after the preheader.
---

# Newsletter LinkedIn post

When an issue is sent, Make.com reads `{issue url}?altTemplate=LinkedIn` and posts the result to the UMB.FYI LinkedIn page. That view uses the issue's **LinkedIn Post** field (Social tab). If the field is empty, it builds a plain post from the preheader, so a post always goes out. This skill writes a better one.

Calls: `.claude/skills/process-tips/scripts/umbfyi.sh` on the LIVE site: `newsletters` and `get-newsletter` to read the issue, and `set-linkedin` to save. Reads need no sign-off; the one write (step 4) happens only after Matt approves.

## Run

1. **Find the issue.** As in `weekly-cryptic` step 1: the newsletter under Archive whose `publishDate` is still in the future. Note whether it's already published, and whether it already has a LinkedIn post (show it, and ask whether to replace it). It needs its items and preheader first: if the preheader is empty, run `newsletter-preheader` first.
2. **Pick the items.** `umbfyi.sh get-newsletter <id>`. Start from the three preheader picks, then add one or two more strong items from other groups, picked the same way as the preheader (HQ and security news first, then festivals, then notable community items). Four or five in all.
3. **Write it.** In this shape:

   ```
   📰 UMB.FYI <YYYY-MM-DD>: <hook: one sentence on the biggest story of the week>

   This week:
   • <item>
   • <item>
   • <item>
   • <item>

   ...and much more in this week's issue: https://umb.fyi/archive/<YYYY-MM-DD>

   Get UMB.FYI in your inbox every Wednesday: https://umb.fyi

   #umbraco #umbfyi
   ```

   - The opening `📰 UMB.FYI <YYYY-MM-DD>:` and the two hashtags match the issue's other social posts. Keep them exactly.
   - 📰 is the only emoji. Bullets are plain `•`.
   - The hook is all most people see before "...see more" (about 200 characters), so it must carry the week's best news on its own. Plain and factual, not salesy.
   - Each item is a short phrase, 3 to 10 words, with the key name in it. Fuller than the preheader is fine: there's no image to fit.
   - People's names go in as plain text. LinkedIn tags can't be added this way.
   - No em dashes, no exclamation marks, nothing over 1,300 characters.
   - Brackets and symbols are fine: the view escapes them for LinkedIn.
4. **Show and save.** Show the post as it will read, with its character count. Once Matt approves (or edits it), write it to a file in the scratchpad and save it with `umbfyi.sh set-linkedin <id> <file>`. It shows the old and new text, saves a draft and checks it reads back exactly. Add `--dry-run` to see the change without saving.
5. **Never publish.** If the issue was already published (step 1), tell Matt to publish it again, or Make.com will post the old text. Finish with one line: saved, and whether it needs republishing.
