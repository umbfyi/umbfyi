---
name: social-sweep
description: Sweep Bluesky and Mastodon for Umbraco news the UMB.FYI tips inbox missed this week. Finds recent Umbraco posts, filters out noise and anything already in the issue, tips or past issues, and shows a short "worth a look" list; Matt's picks are added to the newsletter. LinkedIn can't be swept, so it reminds Matt to check that by hand. Use when asked to sweep or check social, look for anything missed, or as part of newsletter prep.
---

# Social sweep

Tips only catch posts someone tags the UMB.FYI bot in, so good news on social can slip past. This sweeps the platforms that can be searched and shows what might be worth adding.

- **Bluesky:** `umbfyi.sh bluesky-sweep <days>`. Uses the site bot's signed-in session (Bluesky's public API refuses search). Returns posts matching "umbraco".
- **Mastodon:** `python3 -I .claude/skills/social-sweep/scripts/mastodon_sweep.py <since-iso>`. Public, no login: the umbracocommunity.social local timeline plus the #umbraco hashtag timeline.
- **Discord:** not swept. The bot can't read channel history without extra Discord permissions, and Discord links aren't used anyway (see the tips rules).
- **LinkedIn:** can't be swept: no search API, and scraping isn't allowed. Matt checks it by hand.

Both return the same shape: `url`, `author`, `authorName`, `text`, `createdAt`, `isReply`, `links`, `likes`, `reposts`, `replies` (Mastodon also `isRepost`). Scripts: `.claude/skills/process-tips/scripts/umbfyi.sh` (LIVE site).

## Run

1. **The window.** From the last issue's send time (its `publishDate`) to now. Days for Bluesky = whole days since then, rounded up.
2. **Fetch both.** Save each to the scratchpad. If Bluesky returns 503 (rate limit), say so and carry on with Mastodon.
3. **Drop the noise.**
   - Replies, reposts and boosts.
   - UMB.FYI's own accounts (`umb.fyi`, `umbfyi`, and Matt's own posts about UMB.FYI).
   - Bots and automated feeds: outage and status monitors, RSS auto-posters, job boards.
   - Job adverts, sales pitches and ads with nothing new in them.
   - The same post on both platforms, or the same link posted twice: keep one, preferring the version with the better link (rule 3 of the tips rules).
4. **Drop what's covered.** Check each remaining post, and each link in it:
   - Already in this week's issue (`.claude/skills/process-tips/scripts/umbfyi.sh get-newsletter <id>`), if items are in yet. If the items aren't in yet, compare against the workflow's results instead (`items.json`, or `items-raw.json`, from `newsletter-items`).
   - Already a tip this week, handled or not (`umbfyi.sh tips-all <window start>`).
   - Already a media item (`umbfyi.sh search`) or in a past issue (`umbfyi.sh featured`).
5. **Judge.** For what's left, use the tips rules (`.claude/skills/process-tips/references/rules.md`): which link to use (rule 3), and keep or drop (rule 4). Only news-type posts are worth it: releases, launches, new posts and videos, announcements, events, programmes opening. Not chat, opinions, or "had a great time at...".
6. **Show the list.** At most 10, best first. For each: platform, author, a one-line summary, the link you'd use, which group it would go in, and why it's worth a look. Then one line: "Nothing obvious on Bluesky or Mastodon" if empty, and always "LinkedIn: check by hand."
7. **Add Matt's picks.** Draft each pick as a newsletter item, following the `newsletter-items` rules (title, summary, source, emoji, category, date, read time, tags), and show them. Once Matt approves:
   - **In prep** (the items aren't in yet): add them to `items.json`, so they go into the review table and in with everything else.
   - **On its own** (the items are in): send them with `umbfyi.sh add-items <newsletter-id> <file>`. If it returns `422` with `missingGroups` (tidy already removed that heading), tell Matt which heading, and offer another group.
   - Never publish.
8. **Learn.** If Matt picks something you ranked low, or skips something you ranked high, say what it suggests about what's worth flagging.
