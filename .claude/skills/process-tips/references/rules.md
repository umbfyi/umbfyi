# Tip processing rules

Learned from 311 tips handled between October 2025 and October 2026 (about 240 kept, 70 dropped), checked against past newsletters and media items, and confirmed by Matt on 21-10-2026. Re-run "Learn from history" in SKILL.md when these feel off.

## 1. Too old (resurfaced content)

- The newsletter goes out on Wednesdays. The window is: published on or after the Wednesday of the previous issue, minus 2 days grace.
- Use the article's own publish date (page metadata, `article:published_time`, JSON-LD `datePublished`, visible byline date). Not the tip date, not a "last updated" date. This date is only for this check. The media item date is the tip date (rule 7).
- Older than the window: **drop**, reason "old". Even if it's good.
- Exception: a genuinely new update to an old post (e.g. a dated "Update, DD-MM-YYYY" note with real new content). Flag it, don't decide.
- No date findable: flag as "unsure", don't guess.

## 2. Duplicates

Many past drops were things already featured from a feed (package releases, blog feeds). Check hard.

- There are two places to check, and both matter:
  - **Past newsletters** (`umbfyi.sh featured`). The true history. Anything here was already sent to readers.
  - **Media items** (`umbfyi.sh search`). Only the last 6 months, then they're deleted. Catches things already queued for the next issue, including feed imports.
- A miss in media items proves nothing for older content. Always check past newsletters too.
- Search both by the canonical link, then by a distinctive chunk of the title.
- **Packages:** search by the package name (e.g. `Initials.Autolink`, `Articulate`). Package feeds import releases under the package name, so a social post or blog announcing the same release is a duplicate.
- Also compare against the other open tips in the same batch. Same article, different links: tracking params, `www`, trailing slash, Medium `?source=`, LinkedIn re-shares.
- **Same post, different platform.** Many people post to their own blog and cross-post to dev.to, Medium, LinkedIn articles or Hashnode. A link or exact-title search won't always catch this, so also:
  - Read the page's `<link rel="canonical">` and `og:url`. Cross-posts on dev.to, Medium and Hashnode often point at the original. Search for that URL too.
  - Look for the same author in recent newsletters (`umbfyi.sh featured-all <date>`) and recent media items (`umbfyi.sh recent`), and compare titles loosely. Cross-posts often tweak the title or drop a subtitle.
  - Use the author's other sources in `umbfyi.sh profiles` to know where else they post.
- Already featured or already a media item: **drop**, reason "duplicate of [title] ([issue date])".
- Already a media item, but that one is the cross-post and the tip is the original (e.g. the dev.to copy came in from a feed, the tip is their own blog): flag it as **unsure**. Matt decides whether to swap the existing item's link to the original.
- Several open tips for the same thing: keep one (the cleanest link), drop the rest.
- **Same post on Discord and somewhere else.** People often share the same news on Discord and on Bluesky, Mastodon, LinkedIn or the forum. Never keep the Discord one: keep the other platform's post (or a media item already queued from it) and drop the Discord tip, reason "also posted on [platform]". Discord links aren't friendly for readers.

## 3. Which link to use

This is the hardest call. Getting to the content is step one; deciding whether to link the content or the post is step two.

**Step one: find what the post points at.**

- For a social post: open it and find the link in it. Discord links can't be opened (they need a login), so use the tip `message` text instead. It holds the post's text.
- The tip should already be the root of the thread, but check. If the post is a reply, or has no link of its own, walk up to the root post and look for the link there.
  - Bluesky tips are saved as the thread root.
  - Mastodon tips are saved as the post that was replied to, which may not be the root. Check for a parent.
  - Discord tips are saved as the thread's first message, or the message that was replied to.
- If the post links to another social post (a quote or repost), follow it.
- Expand short links (`lnkd.in`, `bit.ly`).

**Step two: link the content, or the post?**

- **Editorial content** (a blog post, article, write-up, video): link the content directly. E.g. a Bluesky post sharing an example.co.uk blog post links to the blog post.
- **The post explains it better than where it points**: link the post, and let readers click through. This is the common case for announcements. E.g. "OC.PowerSort has been updated" linking to a NuGet page, a new site launch, a store refresh, a package or tool linking to GitHub. The NuGet or GitHub page says less than the post does.
- **No outside link**: the post is the content. Link the post.
- In the past, 30 of 31 kept social items linked to the post itself, so lean towards the post unless the destination is clearly editorial.
- Not sure which explains it better: mark **unsure** and show both links in the table.
- A Discord chat message is never linked as the item (readers can't open it). Use what it points at. If it points at nothing, look for the same post on the author's other platforms (their sources in `umbfyi.sh profiles`, or their Bluesky, Mastodon, LinkedIn or forum profile) and link that. Only drop it if there's no public version.

**Clean-up:**

- Strip tracking params (`utm_*`, `source=`, `ref=`, `fbclid`, `si=`, `trk`, `rcm`).
- Prefer the original over re-shares (LinkedIn, Medium mirrors of a personal blog, dev.to cross-posts). Use the author's own site when both exist.

## 4. Keep or drop

Audience: people already using Umbraco. Developers, agencies, editors, active community. Not people evaluating Umbraco.

**Keep:**

- Technical guides, how-tos, code-heavy posts.
- Package releases, tool updates and real product updates. This includes vendor product news (e.g. uSkinned Site Builder releases, new starter kits) even when it's promotional.
- Event announcements and recaps, community features, personal stories from the ecosystem.
- HQ posts (`umbraco.com`, `community.umbraco.com`, Umbraco social accounts, Umbraco YouTube). Lean towards keeping.
- Comparisons that help the audience choose tools around Umbraco.

**Drop:**

- Sales and buyer-facing marketing: "How much does an upgrade cost?", "Why modern enterprises are switching to Umbraco", "Future-ready DXP", "How Umbraco Cloud keeps your site fast and secure". One agency went 0 for 7 in the history, all of this kind.
- Vague, generic, SEO-driven posts with no real insight.
- Not about Umbraco at all (e.g. general tech opinion posts).
- Noise: empty "@UMB.FYI tip" messages with nothing to point at, links to UMB.FYI itself (the site, an issue, the Chrome extension), test tips, bare home pages like `docs.umbraco.com`.
- Spam.

**Bulk sends from one company:**

- Agencies sometimes tip several posts at once (one sent 6 in one day, and 6 again another day). Keep at most one or two: the most hands-on, specific and technical (e.g. "Building an AI Content Generator App Plugin for Umbraco 17", "Test-Driven Development & Clean Architecture in Umbraco"). Drop the rest, reason "bulk send, kept [title]".
- Even technical-sounding posts in a bulk send get dropped if a better one from the same batch is kept.

**Signals that don't matter:**

- Votes. Tips with more than one vote were kept 6 times and dropped 5 times. Don't use them.

When torn, flag it. A wrong keep is cheap (Matt sees it in the table). A wrong drop is invisible.

## 5. Title

- **Articles and videos:** the article's own title as written. Don't rewrite it, don't add the site name. Fix only obvious junk: a trailing " | Site name" or " - Medium", HTML entities.
- **Social posts:** write a short, plain headline saying what happened. Examples from the history:
  - "OC.PowerSort has been updated"
  - "The Umbraco Community Store gets a facelift"
  - "UmbHost GreenStack MCP and Skills"
  - "Dutch Umbraco Alliance Roundup"
  - "umbPublisher - Umbraco Obsidian plugin updated"

## 6. Description

Not much effort goes here. The newsletter workflow cleans and summarises descriptions later.

- **Articles:** the author's own summary (meta description or intro). If there isn't one, the title is fine.
- **Social posts:** copy the post text as it is.
- Remove "Continue reading", "Read more", "Sent from my iPhone", HTML and image markup.

## 7. Author, source, date, tags

- **Author:** usually left empty (64 of 87 recent items). The newsletter workflow fills it in from the page. Fill it only when it's obvious and the page is a person's own blog.
- **Source:** see rule 8. Always fill it in.
- **Date:** the tip date (true for 76 of 87 recent items). Events use the event date.
- **Tags:** only tags already in use (`umbfyi.sh tags`). Every item starts with `hq` (from Umbraco HQ or an HQ account) or `community` (everyone else). These are type tags. Topic tags (like `codegarden26` or `upgrades`) are added later by the newsletter workflow, so don't add them.

Tag sets seen in the history:

| Content | Tags |
| --- | --- |
| Blog post or article | `community,blog` or `hq,blog` |
| Mastodon post (incl. `umbracocommunity.social`, `cultiv.social`) | `community,social,mastodon` |
| LinkedIn post | `community,social,linkedin` |
| Bluesky post | `community,social,bluesky` |
| Marketplace package | `community,package,marketplace` |
| Other package release | `community,package` |
| YouTube video | `community,youtube` or `hq,youtube` |
| Forum post | `community,forum` |
| Event | `community,event`, plus `meetup` for meetups |

## 8. Source

The source is the root of where the post came from. UMB.FYI uses it to attribute posts to people and organisations (Pulse Check, community voices, author lookup), so it has to be right and consistent.

- **Check the profiles first.** `umbfyi.sh profiles` lists known people and organisations. Each one has `sources`. If the link starts with one of them, or the author clearly matches a profile, use that `sources` entry exactly as written. Exact matches are what make attribution work.
- **Then copy what came before.** If an earlier item from the same site or account exists (`umbfyi.sh featured` or `umbfyi.sh search` by domain), use its source exactly, trailing slash and all. Past items are mixed (e.g. `https://umbraco.com/blog/` vs `https://www.example.co.uk/blog`), so consistency with the same site beats any general rule.
- **Blog post:** the root URL of their blog section, e.g. `https://www.example.co.uk/blog`, `https://example.dev/posts`. Not the article URL and not the site home page, unless the blog is the home page. If the blog has an RSS feed, use the channel's `<link>` value. That's what feed imports use, so a tip and a feed item from the same blog end up with the same source.
- **Hashnode:** the blog URL, e.g. `https://<name>.hashnode.dev`.
- **Social post (LinkedIn, Bluesky, Mastodon, X):** the profile URL of the account that posted it.
  - LinkedIn: `https://www.linkedin.com/in/<name>/` (company pages: `https://www.linkedin.com/company/<name>/`)
  - Bluesky: `https://bsky.app/profile/<handle>`
  - Mastodon: `https://<server>/@<name>`
- **Linked content from a social post:** the source of the content, not the social account. A Bluesky post sharing an example.co.uk blog post gets `https://www.example.co.uk/blog`.
- **Platforms with author pages:** the author's page. dev.to: `https://dev.to/<name>`. Medium: `https://medium.com/@<name>` or `https://<name>.medium.com`. GitHub: `https://github.com/<owner>`. YouTube: the channel URL (`https://www.youtube.com/channel/<id>`).
- **Events:** the organiser's page (e.g. the Meetup group URL, or the festival site).
- Never leave it empty. The newsletter workflow will guess it from the link if it's empty, and its guess is often wrong (e.g. it misses `/blogs`).
- If the author isn't in the profiles list but posts regularly, say so in the table. Offer to draft a `profiles.json` entry (format in the data repo README). Don't open a PR without Matt's OK.
- Profile matching also works by prefix: a profile source of `https://mydomain.com/blog` matches any link under it. So a source that's the blog section root is what makes this work.
