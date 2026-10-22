---
name: process-tips
description: Process the UMB.FYI tips inbox for the weekly newsletter. Reads open tips from the live site, finds the real article for each, checks it's from this week, checks for duplicates, decides keep or drop, drafts title/description/author/tags, shows one review table, then converts and dismisses in one go once Matt approves. Use when asked to process, triage, review or clear tips, or as part of newsletter prep.
---

# Process tips

Tips arrive from Discord, Mastodon and Bluesky into the `fyiMediaTip` table (Hub > Tips). Each kept tip becomes a media item (`fyiMediaItem`). Each dropped tip is dismissed (soft deleted).

All API calls go through `scripts/umbfyi.sh` (run it with no args for usage). It logs in as an Umbraco API user. If credentials are missing, stop and tell Matt to set up `~/.umbfyi-tips.env`, or on Claude on the web the environment variables (see the script header). Never print or commit the secret.

Shared data lives in this repo's `data/` folder ([umbfyi/umbfyi on GitHub](https://github.com/umbfyi/umbfyi/tree/main/data)), not in the site code or the database:

- `profiles.json`: people and organisations, with the `sources` used for attribution (`umbfyi.sh profiles`). Changes go in as PRs to that repo. Only open one with Matt's OK.
- `tag-map.json`: topic tags (like `umbracoforms` or `codegarden26`) and the patterns that match them. The newsletter workflow applies these later, so this skill doesn't add topic tags.
- `topics.json`: topic pages built from groups of tags. Not used by this skill.
- `README.md`: the format for each file, and how sources should look for each feed type.

Judgement rules live in `references/rules.md`. Read it before every run. It wins over anything general you think you know about the newsletter.

## Run

1. **Load.** `umbfyi.sh tips` for open tips. `umbfyi.sh tags` for the tag list. `umbfyi.sh profiles` for known authors and their sources. `umbfyi.sh recent <today-30d> <today>` and `umbfyi.sh featured-all <today-90d>` for recent media items and newsletter items to dedupe against.
2. **Work out the window.** The last issue's Wednesday, minus the grace in rule 1. State the window in the table header so Matt can see it.
3. **For each tip** (fan out with subagents if there are more than about 8; each gets the rules file):
   - Find the real link, then decide whether to link the content or the post (rule 3).
   - Fetch the page. Get title, author, publish date and summary.
   - Check: too old (rule 1), duplicate (rule 2, use `umbfyi.sh featured` and `umbfyi.sh search`), keep or drop (rule 4).
   - If keeping, draft the media item fields (rules 5 to 8).
   - Note a confidence: `sure` or `unsure`. Anything `unsure` gets a one-line reason.
4. **Show one table.** Write it as a markdown file in the scratchpad and print it. Columns: `#`, decision (keep / drop / unsure), reason, title, author, source, date, tags, link. Put the description on a line under each kept row. Sort drops to the bottom.
5. **Wait for Matt.** He may edit rows, flip decisions or say "go". Unsure rows need a decision from him before anything is written. Do nothing to the live site until he approves.
6. **Apply, all in one go.** For each keep: write the JSON body to the scratchpad, run `umbfyi.sh create`, then `umbfyi.sh dismiss <tip-id>`. For each drop: `umbfyi.sh dismiss`. Create before dismiss, so a failure never loses a tip. Stop on the first error and report what was and wasn't done.
7. **Learn.** If Matt changed any decision or rewrote any field, say which rule it suggests and offer to update `references/rules.md`. Don't edit it without his OK.

Media item JSON body:

```json
{ "link": "", "title": "", "description": "", "author": "", "source": "", "date": "2026-10-19T00:00:00", "tags": ["community", "blog"] }
```

## Learn from history

Use this to re-derive `references/rules.md` from what Matt actually did. Run it once when the API first goes live, then whenever the rules feel off.

1. `umbfyi.sh tips-all <date-a-year-ago>` gives every tip. Handled ones have `deletedTimestamp` above 0.
2. Pair each handled tip with what was featured (`umbfyi.sh featured` by link and by title). Matched means kept. No match means dropped. Both get dismissed, so the timestamp alone doesn't say which. Don't use media items for this: tips older than 6 months have lost theirs, so they'd all look dropped.
3. For kept ones: compare the tip message to the final title, source and tags as featured. (Newsletter items don't carry author or the original description, so learn those only from tips under 6 months old, via `umbfyi.sh search`.) For dropped ones: fetch the link and work out why (old, duplicate, off-topic, marketing).
4. Write the patterns you find as a proposed diff to `references/rules.md`, with a few real examples per rule. Show Matt. Apply only what he agrees with.
