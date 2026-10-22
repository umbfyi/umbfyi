---
name: find-sources
description: Find new content sources UMB.FYI should be pulling in automatically. Looks at what made it into recent newsletters but came from no source (so only got in through tips or by hand), checks the web for new Umbraco blogs, channels and podcasts, and suggests each with how to add it. Read-only on the site; changes code only when Matt picks a source. Use when asked to find, suggest or discover new sources, feeds or blogs, asked what sources are missing, or for the monthly or quarterly source review.
---

# Find sources

The site code lives in the Umbraco Cloud repo, checked out next to this one at `../UMB.FYI.v17`. All `src/` paths below are inside it, and builds, git and commits happen there. If that folder isn't there (as on Claude on the web), do the read-only checks, skip any code steps, and say so in one line.

Most UMB.FYI items arrive through sources (the Hangfire extractors in `src/Umb.Fyi/Hub/Extractors/Implement`, scheduled in `src/Umb.Fyi/Hub/Composition/HangfireComposer.cs`). Anything that only reaches the newsletter because someone tipped it, or Matt added it by hand, is a gap. This finds those gaps, plus new places worth following, and suggests how to add each.

**Read-only on the site.** Code changes only for the sources Matt picks. Never commit or push without asking, and never suggest deploying on a Wednesday (newsletter day: pushing master deploys straight to live).

What counts as covered:

- **Extractor URLs and channels.** Any URL or YouTube channel id in an extractor file.
- **dev.to and Medium.** Their Umbraco tag feeds cover every author there.
- **Umbraco Sphere** (`UmbracoSphereBlogPostsExtractor`). It brings in most community blogs from one feed. A blog Sphere already carries is covered, even though no extractor names it.
- **Social posts.** The `social-sweep` skill covers these, so they're never a source gap.

Sources Matt has already turned down are in `references/declined.md`. Read it first and don't suggest them again unless something big changed (say why).

## Run

1. **Window.** Default: the last 6 months. Matt can ask for a different one.
2. **Find the gaps.** Save `.claude/skills/process-tips/scripts/umbfyi.sh featured-all <window start>` to the scratchpad. Then run `python3 -I .claude/skills/find-sources/scripts/uncovered.py <featured.json> ../UMB.FYI.v17 2` from the repo root. It prints each origin with 2 or more items in the window that nothing covers, with counts, dates and examples. It reads Sphere with the token in `src/Umb.Fyi.Web/appsettings.json` (or `UMBFYI_SPHERE_TOKEN`). Never print the token.
3. **Look further.** Search the web for Umbraco content made in the last 3 months that isn't covered: blogs, YouTube channels, podcasts, newsletters, package lists, user groups that post regularly. Good places: YouTube search for "Umbraco" sorted by date, podcast directories, the Umbraco forum's blog and video threads, umbraco.com community pages, Sphere-like aggregators. Check each against what's covered (the extractor files and step 2's Sphere check). Keep only ones with at least 2 Umbraco pieces in the last 3 months.
4. **Check each candidate.**
   - **One-off sites** (a conference, a festival, a single event's page): drop them. Events come through Umbracalendar; one-off sites never post again.
   - **Blogs:** find the feed (`<link rel="alternate">` on the home page, then `/rss`, `/feed`, `/rss.xml`, `/atom.xml`). Note how often it posts and what share is about Umbraco. Is there an Umbraco tag or category feed?
   - **YouTube:** get the channel id (`"channelId":"UC..."` in the channel or a video page). Note how often it uploads and what share is about Umbraco.
   - **Podcasts:** find the RSS feed and the date of the latest episode.
   - **Package lists:** find the feed.
   - Drop anything with no new content in 3 months.
5. **Say how to add each one.** Use the existing patterns:
   - **Blog:** recommend getting it into Sphere (Sphere is run by Umbraco HQ, so that's for Matt to raise), so every Sphere user gets it. If Matt wants it now, the fallback is a `MultiRssMediaExtractorBase` list with `FilterKeywords => ["umbraco"]` for mixed blogs. None exists yet, so this means a new extractor and job.
   - **YouTube channel:** add the channel id to `UmbracoCommunityYoutubeExtractor` (it already keeps only videos mentioning Umbraco). Use `UmbracoYoutubeExtractor` only for Umbraco HQ channels.
   - **Podcast:** a new `SimpleRssMediaExtractor` like `CandidContribRssExtractor`, plus a job every 6 hours in `HangfireComposer.cs`.
   - **Package feed:** add the URL to `UmbracoCommunityPackageFeedsExtractor`.
   - **Anything else:** say what kind of extractor it needs and roughly how big a job it is.
6. **Report.** In Matt's chat style (short, plain words, no jargon):
   - One line first: how many sources are worth adding.
   - One table, best first: source (plain name with link), type, evidence (e.g. "5 items in issues since 22-04-2026, last 01-07-2026" or "4 Umbraco videos since July"), how to add it.
   - One line listing what was dropped and why, grouped (e.g. "3 one-off event sites, 2 inactive blogs").
7. **Add, only for the ones Matt picks.** Edit the code following the patterns above. For a new job, add it to `HangfireComposer.cs` under the right heading. Build with `dotnet build src/Umb.Fyi/Umb.Fyi.csproj`. Fetch the feed once to check it parses and has Umbraco items. Show Matt the diff, and commit only on his go. After it deploys, `check-sources` will show the new source's first runs.
8. **Remember the no's.** For each source Matt turns down, add it to `references/declined.md` with today's date (DD-MM-YYYY) and his reason.
