---
name: weekly-cryptic
description: Add this week's minute cryptic to the UMB.FYI newsletter. Finds the upcoming draft newsletter on the live site, runs the minute-cryptic skill to write and verify a clue, then fills in the newsletter's empty puzzle block once Matt approves. Never publishes. Use when asked to add, set or do this week's puzzle or cryptic, or as part of newsletter prep.
---

# Weekly cryptic

Every newsletter is created from the "Newsletter Starter" blueprint, which ends with a 🧩 "Puzzle" group heading and an empty Minute Cryptic block (`minuteCrypticBlock`), just before the final signup block. This skill fills that block. An empty block, and its heading, is hidden in the email and skipped on https://umb.fyi/puzzles, so a skipped week needs no clean-up.

All site calls go through `.claude/skills/process-tips/scripts/umbfyi.sh`. It talks to the LIVE site. Reads need no sign-off; the one write (step 5) happens only after Matt's go in step 4. Never use `umbraco-developer-mcp` or the local `umbraco-mcp` for this.

Known keys (same on local and live, as Umbraco Deploy keeps them):

- Archive page (parent of every newsletter): `028b21ee-6da5-4e54-b6cd-e73f6c33b85b`
- Minute Cryptic element type: `122f1a69-fa4c-44f3-ab12-f4f023d30706`
- Newsletter Group element type: `c00d9369-6b0e-439b-8847-61e0d1067e83`
- Newsletter block settings type: `2647f8c8-acc6-4753-8be4-83c0fb4d4830`
- Newsletter block list property: `content`

If a key doesn't match, look it up with `umbfyi.sh get-newsletter` on a recent newsletter rather than guessing.

## Run

1. **Find the next issue first.** `umbfyi.sh newsletters` lists the newest few under Archive, newest first, each with its `publishDate` and `state`. Newsletters are named by date (`YYYY-MM-DD`) and go out on Wednesdays. The target is the newsletter whose `publishDate` is still in the future. Don't go by published state: Matt often publishes early, because publishing is what syncs the issue to the newsletter system, and the site hides anything before its `publishDate`. Note whether it is already published.
   - Compare the full date and time, not just the date. Matt often runs this on Wednesday morning, before the issue goes out. `publishDate` is a UTC instant: 9am UK is stored as `08:00` in summer time and `09:00` in winter, and the backoffice shows that raw UTC value. Get "now" from `date -u`, never from local time.
   - Show Matt the send time in UK time (e.g. "goes out today at 9am"). If it's less than an hour away, say so up front: the puzzle has to be filled and the issue republished before then. Then `umbfyi.sh get-newsletter <id>` and find the block with `type` `puzzle`.
   - No newsletter with a future `publishDate`: stop. Offer to run the `create-newsletter` skill first. Don't write a clue with nowhere to put it.
   - More than one newsletter with a future `publishDate`: ask which one.
   - The block's `clue` is already filled in: show what's there and ask whether to replace it.
   - No Minute Cryptic block (a newsletter made before the blueprint had one): the script can't add blocks, so this needs the hosted `umbraco-editor-mcp`. If it isn't connected (as on Claude on the web), stop and tell Matt to add the 🧩 Puzzle heading and a Minute Cryptic block in the backoffice, then run this again. If it is, offer to add one. If Matt agrees, carry on with steps 2 to 4, then in place of step 5 use `add-blocklist-block` to add a group block (`groupEmoji` 🧩, `groupTitle` Puzzle, `groupAlias` puzzle) and then the puzzle block straight after it, both before the last signup block, both with the block settings type and `settingsValues: [{"alias": "itemDivider", "value": []}]` (the tool insists on at least one). `inspect-blocks` doesn't list blocks in page order, so find the last signup block from the published page instead: on `https://umb.fyi/<name>` the block ids appear in order as `id="umbfyi-item-<contentKey>"`, and the last one before `form-newsletter-foot` is it. Add the group `before` that signup, then the puzzle `after` the group. The puzzle block's `values` are the eight fields. Then go on to step 6.
2. **Get past answers.** `umbfyi.sh puzzle-answers` lists every past answer, newest first, as a JSON array. It reads every page of https://umb.fyi/puzzles and needs no login. If it fails or comes back empty when there should be puzzles, say so and ask Matt before going on, as a repeated answer would slip through.
3. **Write the clue.** Run the `minute-cryptic` skill with the past answers as its avoid list. It writes and verifies the clues and shows the top 3. Matt picks one, and it hands back the clue as JSON.
4. **Map it to the eight fields** (see "Fields" below), then **show the change.** One short block: the newsletter's name, then the eight fields (clue, enumeration, definition, indicator, device, fodder, answer, explanation). Wait for Matt's go.
5. **Fill the block.** Write the eight fields to `puzzle.json` in the scratchpad as one object keyed by alias (`clue`, `enumeration`, `definition`, `indicator`, `device`, `fodder`, `answer`, `explanation`). Then `umbfyi.sh set-puzzle <id> puzzle.json`. It finds the one puzzle block, shows the old and new fields, saves a draft and checks every field reads back exactly. Add `--dry-run` to see the change without saving.
6. **Check it.** If `set-puzzle` stops with an error, tell Matt what it says, and what was and wasn't saved.
7. **Never publish.** Never publish, schedule or unpublish the newsletter. `set-puzzle` saves the change as a draft. If the newsletter was already published (step 1), tell Matt to publish it again so the puzzle syncs to the newsletter system. Finish with one line: which newsletter now has which clue, and whether it needs republishing.

## Fields

The Minute Cryptic block has eight fields. Fill them from the `minute-cryptic` JSON:

- `clue`: the JSON `clue` without the enumeration in brackets at the end.
- `enumeration`, `answer`, `explanation`: as they are.
- `definition`: as it is. For a double definition, `definition` and `definition2` in clue order, joined with ` / `.
- `device`: the CMS wording: `anagram`, `hidden`, `reversal`, `hidden_reversal` → `hidden reversal`, `charade`, `container`, `initials` → `first letters`, `deletion` → `dropped letters`, `double_definition` → `double definition`. For a two-device clue, the main device, then the part's: `container / anagram`.
- `indicator`: as it is, or `""` for a plain charade or double definition. For a two-device clue, the main indicator, then the part's: `holding / wild`. A charade has no main indicator, so it's just the part's.
- `fodder`: the clue words the wordplay works on, in clue order, separate pieces joined with ` / `. Anagram: each `fodder` word. Hidden, reversal, first letters: the `fodder` span. Charade: each part's `text`. Container: `outer` and `inner` `text`, in clue order. Deletion: the `fodder` `text`, plus `drop` `text` if it's an object. `""` for a double definition.

## Rules

- Copy the definition, indicator and fodder words exactly as they appear in the clue. The puzzles page finds and underlines them by matching the text.
- Don't put the answer anywhere except the `answer` and `explanation` fields. The email only shows the clue and its length.
- If any step fails, stop and say what was and wasn't done.
