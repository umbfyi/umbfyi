---
name: weekly-cryptic
description: Add this week's minute cryptic to the UMB.FYI newsletter. Finds the upcoming draft newsletter on the live site, runs the minute-cryptic skill to write and verify a clue, then fills in the newsletter's empty puzzle block once Matt approves. Never publishes. Use when asked to add, set or do this week's puzzle or cryptic, or as part of newsletter prep.
---

# Weekly cryptic

Every newsletter is created from the "Newsletter Starter" blueprint, which ends with a 🧩 "Puzzle" group heading and an empty Minute Cryptic block (`minuteCrypticBlock`), just before the final signup block. This skill fills that block. An empty block, and its heading, is hidden in the email and skipped on https://umb.fyi/puzzles, so a skipped week needs no clean-up.

All site calls use the hosted `umbraco-editor-mcp` server. It talks to the LIVE site. Reads need no sign-off; the one write (step 4) happens only after Matt's go in step 3. Never use `umbraco-developer-mcp` or the local `umbraco-mcp` for this.

Known keys (same on local and live, as Umbraco Deploy keeps them):

- Archive page (parent of every newsletter): `028b21ee-6da5-4e54-b6cd-e73f6c33b85b`
- Minute Cryptic element type: `122f1a69-fa4c-44f3-ab12-f4f023d30706`
- Newsletter Group element type: `c00d9369-6b0e-439b-8847-61e0d1067e83`
- Newsletter block settings type: `2647f8c8-acc6-4753-8be4-83c0fb4d4830`
- Newsletter block list property: `content`

If a key doesn't match, look it up with `inspect-blocks` on a recent newsletter rather than guessing.

## Run

1. **Find the next issue first.** `list-children` under Archive. It returns oldest first, 20 at a time, with a `total`; jump to the last page with the cursor `base64('{"s":<total-20>,"t":20}')` (no padding) instead of paging through. Newsletters are named by date (`YYYY-MM-DD`) and go out on Wednesdays. The target is the newsletter whose `publishDate` field is still in the future. Don't go by published state: Matt often publishes early, because publishing is what syncs the issue to the newsletter system, and the site hides anything before its `publishDate`. `get-page` the newest few newsletters, read `publishDate`, and pick the one after now. Note whether it is already published.
   - Compare the full date and time, not just the date. Matt often runs this on Wednesday morning, before the issue goes out. `publishDate` is a UTC instant: 9am UK is stored as `08:00` in summer time and `09:00` in winter, and the backoffice shows that raw UTC value. Get "now" from `date -u`, never from local time.
   - Show Matt the send time in UK time (e.g. "goes out today at 9am"). If it's less than an hour away, say so up front: the puzzle has to be filled and the issue republished before then. Then `inspect-blocks` on it (`propertyAlias: "content"`) and find the Minute Cryptic block.
   - No newsletter with a future `publishDate`: stop. Offer to run the `create-newsletter` skill first. Don't write a clue with nowhere to put it.
   - More than one newsletter with a future `publishDate`: ask which one.
   - The block's `clue` is already filled in: show what's there and ask whether to replace it.
   - No Minute Cryptic block (a newsletter made before the blueprint had one): offer to add one. If Matt agrees, carry on with steps 2 and 3, then in place of step 4 use `add-blocklist-block` to add a group block (`groupEmoji` 🧩, `groupTitle` Puzzle, `groupAlias` puzzle) and then the puzzle block straight after it, both before the last signup block, both with the block settings type and `settingsValues: [{"alias": "itemDivider", "value": []}]` (the tool insists on at least one). `inspect-blocks` doesn't list blocks in page order, so find the last signup block from the published page instead: on `https://umb.fyi/<name>` the block ids appear in order as `id="umbfyi-item-<contentKey>"`, and the last one before `form-newsletter-foot` is it. Add the group `before` that signup, then the puzzle `after` the group. The puzzle block's `values` are the eight fields. Then go on to step 5.
2. **Write the clue.** Run the `minute-cryptic` skill. It checks past answers, writes and verifies the clues, and shows the top 3. Matt picks one, and it hands back the CMS fields block.
3. **Show the change.** One short block: the newsletter's name, then the eight fields (clue, enumeration, definition, indicator, device, fodder, answer, explanation). Wait for Matt's go.
4. **Fill the block.** One `edit-block` call: `id` = the newsletter, `propertyAlias: "content"`, `contentKey` = the puzzle block, `values` = the eight fields, using the aliases above. Leave `indicator` empty for a plain charade.
5. **Check it.** `inspect-blocks` again and confirm every field saved exactly. If `edit-block` reports `validation.valid: false`, tell Matt what it says.
6. **Never publish.** Never publish, schedule or unpublish the newsletter. `edit-block` saves the change as a draft. If the newsletter was already published (step 1), tell Matt to publish it again so the puzzle syncs to the newsletter system. Finish with one line: which newsletter now has which clue, and whether it needs republishing.

## Rules

- Copy the definition, indicator and fodder words exactly as they appear in the clue. The puzzles page finds and underlines them by matching the text.
- Separate two indicators or two devices with ` / `, in the same order, so each indicator pairs with its device.
- Don't put the answer anywhere except the `answer` and `explanation` fields. The email only shows the clue and its length.
- If any step fails, stop and say what was and wasn't done.
