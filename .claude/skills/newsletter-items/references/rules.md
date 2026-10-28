# Newsletter item review rules

**Starter rules, not yet confirmed by Matt.** Written from the workflow code and the 21-10-2026 issue, before any real run. Run "Learn from history" in SKILL.md, and update these as Matt corrects real runs.

The workflow already fetches the last 7 days of news and the next 10 days of events, removes dead links and cancelled events, writes summaries, and assigns category, emoji, tags and read time. Don't redo that work. Fix what it flags (section 0), then look for what it gets wrong.

## 0. Workflow flags

The workflow flags problems but keeps the item. Fix or decide every flag before the general review. Match on the start of the log message:

| Flag (message starts with) | What it means | What to do |
| --- | --- | --- |
| `Duplicate link found in previous newsletter` | Already sent last week. | **Drop**, reason "in last issue". Except a training session that's still upcoming: keep (section 11). |
| `No author found in markup or profiles` | Author unknown, so the summary may say "the author" or name the site. | Find the author on the page (byline, `meta name="author"`, JSON-LD). Make sure the summary names them, and that `source` is their own site or profile. If they're a regular, say so: they could be added to `profiles.json` (`umbfyi.sh profiles`), with Matt's OK. |
| `Failed to extract content` | Couldn't read the page body, so there's no proper summary (it fell back to the feed's description, which may be empty or a teaser). | Fetch the page and write the summary yourself in house style (section 1). If the page can't be read at all, mark **unsure**. |
| `Failed to summarize` / `Simple summarization applied` | No AI summary. | Write the summary yourself, as above. |
| `Could not extract consumption time` / `Failed to extract consumption time` | No read time. Usually YouTube. | Videos and podcasts: the length in whole minutes, rounded up (YouTube page `lengthSeconds` or `itemprop="duration"`). Articles: about 1 minute per 230 words of body text. Can't tell: leave 0 and say so. |
| `Content score too low` | The workflow thinks it's thin or off-topic. | Look at it. Usually **drop**; mark **unsure** if it looks fine to you. |
| `Failed to score` | No score. | Ignore, but give it the normal review. |
| `URL temporarily failed` / `HTTP error processing` / `Timeout processing` | The link didn't load during the run. | Try it again. Loads: keep. Still broken: **drop**, reason "broken link". |
| `contains TBD/TBC placeholder description` | Event details not set yet. | Check the event page for a venue or time. Found: update the summary. Not found: keep as is. |
| `Failed to check TBD status` | Couldn't check. | Check the event page as above. |
| `Failed to process tags` | No tags. | Pick tags from `umbfyi.sh tags` (section 7). |

Any other flag: say what it is and mark the item **unsure**.

Not every miss is flagged. When no read-time extractor exists for a site, the workflow skips the item quietly and leaves 0 minutes. Only HQ, Community and video items get AI summaries, so others keep whatever the feed gave. So, flagged or not, check every item:

- Blog posts, articles and videos (HQ, Community, Watch & Listen, Training, Miscellaneous, a festival's posts) need a real summary and a read time above 0. Empty, cut-off or teaser summary: write one as for `Failed to extract content`. Read time 0: work it out as for `Could not extract consumption time`. Note it in the table as "⚠️ not flagged".
- Events, packages and social posts keep a read time of 0. Social posts keep no description (section 9).

## 1. Fix light, don't rewrite

- Published issues keep the workflow's summaries mostly as written. Only change a summary when it is wrong, broken or unreadable: cut off mid-sentence, in the wrong language, about the wrong page (a cookie banner, a login wall, a 404 page), or plainly marketing copy.
- Don't change wording just for style.
- When you write a summary yourself (section 0), match the house style: 2 or 3 sentences, about 50 to 60 words, third person, naming the author ("In this post, Jane Doe explores..."), saying what the post covers and why it's useful. Plain words, no hype.
- No em dashes in anything you write.
- Use people's current names. The workflow can pick up an old one from a page or byline. Known changes: Shannon Deminick is now Shannon Thompson.

## 2. Category

- Every item needs a category with a heading in the newsletter. `Uncategorized` items: pick the right group or drop.
- HQ is Umbraco HQ's own blog posts, RFCs and announcements. Community is everyone else's blog posts.
- Video and podcast items go in Watch & Listen, even when they're from HQ.
- If Matt has added a one-off heading this week (like a conference or "24 Days"), items about it go there. Use its `groupAlias` as the category.
- Social posts go under Social, even from HQ accounts. Only blog posts and real editorial content go in the named sections.
- Security advisories and security heads-ups get the ⚠️ emoji, not the workflow's 📰.

## 3. Titles

- Strip site names and separators the page title carries: " | Umbraco", " - DEV Community", " | by Name | Medium".
- Packages: the title is the package name as listed on the Marketplace. Leave it.
- Events: leave the title as the event page has it.

## 4. Duplicates

- The workflow only checks against the last issue. Also check `umbfyi.sh featured <link or title>` for anything that looks familiar, and compare items against each other in this batch (same article at two links, a blog post and its cross-post).
- Duplicate: drop, reason "duplicate of [title] ([issue date])".
- **Same post from two sources.** People often post to their own blog and cross-post to dev.to (or Medium, Hashnode, LinkedIn), and both feeds can come through in the same batch, or one this week and one last week. Exact link or title checks miss this, so:
  - Within the batch, compare items by the same author with similar titles (cross-posts often tweak the title or drop a subtitle), and similar summaries.
  - Read each page's `<link rel="canonical">` and `og:url`. A dev.to, Medium or Hashnode copy often points at the original.
  - Check the other copy against past issues too (`umbfyi.sh featured` with a chunk of the title, and the author's name).
  - Keep the original on the author's own site. Drop the cross-post, reason "cross-post of [title]". If the original was already featured, drop both.
- **Same news on Discord and another platform** (Bluesky, Mastodon, LinkedIn, the forum): keep the other platform's item and drop the Discord one. Never link to Discord: readers can't easily open it. If an item's only link is a Discord message, find a public version (the author's other profiles, `umbfyi.sh profiles`) or what it points at; failing that, mark it **unsure**.

## 4a. Skrift

Skrift (skrift.io) is a monthly online magazine. Never feature its articles one by one. It always gets one item per issue, linking to the issue itself:

- Title `Skrift Issue #<n>`, link `https://skrift.io/issues/#<n>`, source `https://skrift.io`, emoji 📰, category `Community`.
- Description in this exact form: `Featuring guest posts by <Author> on "<Article title>" and <Author> on "<Article title>"` (one article: `Featuring guest post by <Author> on "<Article title>"`; more than two: commas, then "and" before the last).
- Read time: the articles' read times added together.
- Tags: `skrift`, plus up to two topic tags if the articles share a clear topic.
- Drop every individual skrift.io article item, reason "Skrift: covered by the issue item". If this issue hasn't been featured yet (`umbfyi.sh featured "Skrift Issue #<n>"`), add the issue item in their place, with the article details from skrift.io. Make sure you have the right issue number.

## 5. Events

- Show events from the send time up to and including the Friday of the following week (the workflow fetches about 10 days ahead). Earlier or later: drop.
- If the title doesn't make clear which meetup group it is, put the group's name in front: `<Group> - <Event title>`. The group name is on the meetup group's page (the item's `source`). "UmbraCymru - October Meetup" and "Manchester and North West Umbraco Meetup - Lightning Talks" are right; a bare "October Meetup" or "Lightning Talks" isn't.
- If the event can be attended online (online only, or hybrid), add the `virtual` tag.
- Summary should be the date, time, time zone and venue (or "Online"), as the workflow writes it. A "TBD" or "TBC" venue is fine if that's what the event page says.
- Check every event's page, flagged or not. The workflow only drops events whose page says "this event has been cancelled" (or "was cancelled"), and only if the page loaded; it doesn't catch postponed or rescheduled events, or a missing location.
  - Cancelled or postponed: **drop**, reason "cancelled" or "postponed".
  - Moved to a new date: update the date and summary, and recheck it's still in the window.
  - Always compare the date, time and venue with the page, even when nothing looks wrong. The workflow's event data can be stale: on 28-10-2026 UmbraCymru came through as 29-10 at Method4, but the page said 28-10 at Aspire Systems. The page wins.
  - No venue and not marked online in the summary: add the venue from the page, or "Online". Can't find one: mark **unsure**.
  - Page won't load: mark **unsure**.
- The workflow removes cancelled events without saying so. Compare `umbfyi.sh events <from> <to>` for the window against the workflow's events and list any it dropped in the table header ("removed by workflow: ..."), so Matt can see them. Only bring one back if its page shows it's still on.

## 6. Drop

- Not about Umbraco or the Umbraco community.
- Job adverts, sales pages, and press releases with no real content.
- Broken links the workflow let through with a warning. Check the link; drop if it doesn't load.

## 7. Tags

Tags come from `data/tag-map.json` in the [umbfyi/umbfyi repo](https://github.com/umbfyi/umbfyi/tree/main/data). Each tag there has regex patterns, and the workflow gives an item the first 3 tags whose patterns match anywhere in its title, summary or full body text. So the usual mistake is a tag for something the post only mentions in passing (a post about upgrades that says "forms" once gets `umbracoforms`). This is the biggest single fix. There's no neat rule, so tag by example:

- For each item, look up each proposed tag in `references/tags.md` and compare the item with that tag's past examples. Keep a tag only if the item clearly belongs alongside them. Then ask what tags its nearest past examples had, and add any that fit.
- Check `references/tag-corrections.md` first. A past correction for a similar item beats everything else.
- Never more than 3 tags (the server rejects more). Usually 1 or 2. Fewer good tags beat more loose ones. Many packages and events have none, and that's fine.
- Use tags from the tag map (all listed in `references/tags.md`, with their patterns). One-off tags outside the map are allowed for something specific that matters that week, like a conference, campaign or release (past ones are under "other" in `references/tags.md`; reuse one if it fits). Propose any new one-off tag in the table, marked **new**, and only use it once Matt agrees. If it's something that will keep coming up, suggest adding it to `tag-map.json` with patterns instead (a PR to umbfyi/umbfyi, with Matt's OK), so the workflow assigns it from then on.
- If the same wrong tag keeps coming up from a loose pattern, say which pattern in the table. Fixing it in `tag-map.json` (a PR to umbfyi/umbfyi, with Matt's OK) stops it at the source.
- Watch the pairs: a specific product tag usually comes with its broader one where past items show that (e.g. `umbracoai` with `ai`), but not always. Follow the examples, not a habit.
- `umbracocms` only goes on actual product posts (HQ releases, advisories, product updates). Not on community posts that just use or mention the CMS.
- Lowercase, no spaces.
- When you're not sure, say so in the table row. Don't guess quietly.

## 8. Packages

- Description: one short sentence only. Cut everything after the first sentence, and shorten that if it runs long. "Live frontend previews for Umbraco 17/18 Block List blocks in the backoffice." is the right length.
- If one developer or company has two or more packages in the batch, give them the same `cluster` (the developer's or company's name, from the package page or the shared name prefix like `Esatto.` or `DigitalWonderlab.`). The server puts each cluster together at the bottom of Packages. Don't cluster on a shared prefix alone when it's a generic one like `Umbraco.Community.`; check the package owner.
- The same package more than once (different versions): keep only the highest version. Drop the rest, reason "older version of [package]".
- Limbo packages (`Limbo.`, from packages.limbo.works) go at the bottom of Packages: they're mostly automated version-release announcements. Give them the cluster `Limbo`. The server only moves a cluster down when it has two or more items, so with a single Limbo package, say in the table that Matt needs to drag it to the bottom by hand.

## 9. Social

- Social posts have no description. Clear the summary.

## 10. Festivals and big events

When a festival or big event (Spark, Codegarden, US Fest, UMBRAAD, UK Conference, Umbraco in the City, Umbraco India) falls inside the event window (section 5: from the send time to the Friday of the following week), it gets its own section at the very top of the issue. These events run Wednesday to Friday, so that's always two issues: the week before, and the week of (even if it's on the send day itself). It's the main event's date that counts. A pre-party, hackathon or run in the window on its own doesn't start a section. Outside the window, no section: its posts and events stay in their usual groups.

- What goes in it: all its events (pre-party, hackathon, the event itself, after party, runs) and the posts and social posts about it. They come out of Events, Community, Social and so on. The server puts the events first, soonest first, then the posts, newest first.
- The heading: reuse the alias, title and emoji from the last time that event had a section (`umbfyi.sh featured-all <date>` shows past groups; `umbfyi.sh get-newsletter <id>` on that issue shows the emoji). Known ones: `spark` "Umbraco Spark" ⚡, `codegarden` "Codegarden" 🌷, `umbraad` "UMBRAAD" ⌨️, `uk-conf` "UK Conference" 🎉. For a new event, pick an emoji that fits it and say so in the table.
- Items keep their own emoji (📆 for events, 💬 for social).
- Tag them with the event's tag (e.g. `codegarden26`, `umbracospark`, `ukconf`), as well as the usual tags.
- Propose the section in the review table, and create it only once Matt agrees.

## 10a. 24 Days in December

24 Days in Umbraco (24days.in) publishes an article a day through December. While it runs, its articles get their own section at the very top, like a festival: alias `24days`, title "24 Days", emoji 🎁 (`umbfyi.sh add-group <id> 24days "24 Days" "🎁"`, with Matt's OK, as for festivals).

- Each issue takes that week's articles (usually about 7). Category `24days`, emoji 📰, source `https://24days.in/umbraco-cms/`.
- They're ordinary posts otherwise: a normal summary naming the author, a read time, and topic tags.
- Check `umbfyi.sh featured` so an article isn't repeated from last week.

## 10b. Forum

Release announcements and notable posts on the Umbraco forum (forum.umbraco.com) go under the Forum heading (category `forum`), not Community or Social. Past examples: "God Mode v17 now available", "GitHub Action for Umbraco Cloud Deployments Released".

- Source: the poster's forum profile (`https://forum.umbraco.com/u/<user>`).
- A short summary of what was released or announced, and tags as usual (`packages` for a package release).
- Ordinary questions and support threads don't go in.
- Forum posts now come in automatically (the Announcements category feed), so expect most weeks to have some. The source comes through as the category page (`https://forum.umbraco.com/c/announcements/31`); replace it with the poster's profile as above.
- **A new package in both Forum and Packages** (the Marketplace item): keep the Marketplace one and drop the forum post, reason "duplicate of [package] (Packages)". The forum is for what the Marketplace misses: package updates, tools that aren't packages, and write-ups.

## 11. Training

- Training sessions come from the Umbraco training site, and the same session often turns up more than once: the same course and date under slightly different links (`/enroll` on the end, a `-0` added to the slug, a different `?id=`). Keep one per session, using the cleanest link.
- A session shown last week can be shown again while it's still upcoming, so the workflow's "in last issue" flag doesn't mean drop for training (section 0).
- Drop sessions whose date is already past, or later than the event window (section 5).
- If the same course runs on two dates in the window, keep both, and add the date to each title so they can be told apart: "Load Balancing and Azure (February 5th 2026)".
