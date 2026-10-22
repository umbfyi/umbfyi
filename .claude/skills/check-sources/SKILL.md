---
name: check-sources
description: Check the health of UMB.FYI's content sources (the Hangfire extractors that pull blogs, videos, podcasts, events and packages into the Hub) on the live site. Reads the source-status endpoint, works out which sources are broken, which are just quiet and which are fine, investigates each problem at the real URL, and reports one table with likely causes and fixes. Read-only on the site; drafts code fixes only when Matt asks. Use when asked to check, monitor or health-check the sources, extractors, processors or feeds, when asked whether anything is broken, or weekly before newsletter prep.
---

# Check sources

The site code lives in the Umbraco Cloud repo, checked out next to this one at `../UMB.FYI.v17`. All `src/` paths below are inside it, and builds, git and commits happen there. If that folder isn't there (as on Claude on the web), do the read-only checks, skip any code steps, and say so in one line.

The sources are the Hangfire jobs in `src/Umb.Fyi/Hub/Composition/HangfireComposer.cs`. Each one is an extractor class in `src/Umb.Fyi/Hub/Extractors/Implement/<job id>.cs` (bases in `src/Umb.Fyi/Hub/Extractors/`). Every run is saved to `fyiExtractorRun` with its item count, newest item date, warnings and error. Hangfire marks most failures as a success (a 404 just gives an empty result), so these records are the real signal.

**Read-only on the site.** Never trigger, pause or delete jobs, and never change site data. Code fixes are drafted in the repo only when Matt says so. Never commit or push without asking, and never suggest deploying on a Wednesday (newsletter day: pushing master deploys straight to live).

Call: `.claude/skills/process-tips/scripts/umbfyi.sh source-status [days]` (LIVE site, default 30 days, max 60). It returns one row per Hangfire recurring job:

- `id`, `cron`, `lastExecution`, `nextExecution`, `lastJobState`, `jobError`: from Hangfire.
- `status`: `ok`, `warning` (last run found nothing or had warnings), `failing` (last run threw, or Hangfire has an error) or `no-runs` (no run recorded in the window; normal for `MediaProcessor` and `MediaCleanupJob`, which aren't extractors).
- `lastRun`: `startedAt`, `itemCount`, `newestItemDate`, `warnings` (newline separated), `error`.
- `lastRunWithItems`, `newestItemDate` (over the window), `runs`, `failedRuns`, `runsWithWarnings`, `runsWithNoItems`, `averageItemCount`.

Known quiet sources Matt has already seen are in `references/known-quiet.md`. Read it first.

## Run

1. **Fetch.** Save `source-status` to the scratchpad. If it fails, say so and stop.
2. **Check the pipeline first.** These break everything at once, so they come first in the report.
   - `MediaProcessor` (saves fetched items, every minute): `lastExecution` more than 10 minutes ago, or `lastJobState` is `Failed`, means nothing new is being saved.
   - Any job whose `lastExecution` is more than twice its interval ago (hourly: 2 hours; `0 */6 * * *`: 12 hours) means Hangfire has stalled. Note the site may have just restarted.
3. **Sort every extractor** into one of these:
   - **Broken.** `error` set, `jobError` set, or a warning that says the source is gone: 404, 410, a host that doesn't resolve, "did not return an RSS/Atom feed", a GraphQL response with no data, a missing token.
   - **Flaky.** The last run is fine, but `failedRuns` or `runsWithWarnings` is more than about a quarter of `runs`. Usually rate limits (429) or timeouts.
   - **Suspicious.** No warnings, but `itemCount` is 0 or well below `averageItemCount`. Investigate: either the source is just quiet or a scraper has stopped matching the page.
   - **Fine.** Found items and has no warnings.
4. **Investigate each broken, flaky or suspicious source.** Open its extractor file to find the URL, query or page selectors. Then check the real thing:
   - Feeds: fetch the URL (with a browser-like user agent; the site uses an Edge one). If it's gone, look for where it moved: the site's home page `<link rel="alternate">`, the platform's current feed URL format, or a redirect.
   - Feeds that work: read the newest item's date. If it's older than the extractor's `MinPubDate` window (default 1 year, some use 3 months), the source is **quiet, not broken**. Say how long since its last item.
   - Scrapers (`*ScraperExtractor`): fetch the page and check the selectors in the code still match. A layout change shows as zero matches.
   - APIs: call the endpoint. An empty list can be normal (the training API between course schedules).
   - GitHub GraphQL: run the extractor's query with `gh api graphql` and its variables. GitHub reports bad queries as `errors` with a 200 response, which the extractor sees as "no data".
   - Sites that block automated requests (403, 429, 999) are "couldn't check", not broken.
   A source listed in `references/known-quiet.md` that is still quiet in the same way just gets a ✅ line marked "known quiet".
5. **Report.** In Matt's chat style (short, plain words, no jargon):
   - One line first: how many sources are fine, and how many need a look.
   - Then one table for anything that isn't fine: source (plain name, e.g. "Medium" not the class name), status (broken / flaky / quiet / couldn't check), what's wrong, suggested fix.
   - Then one ✅ line listing the fine sources by plain name.
   - Fixes are concrete: the new URL, the selector to change, "remove this source", or "renew the GitHub token". Say which file changes.
6. **Fix, only if Matt asks.** Edit the extractor, following the patterns already in the file and its base class. Build with `dotnet build src/Umb.Fyi/Umb.Fyi.csproj`. For a removed source, take it out of `HangfireComposer.cs` and add it to the `RecurringJob.RemoveIfExists` list there (the existing pattern), then delete the class. Show Matt the diff, and commit only on his go.
7. **Remember quiet sources.** If Matt says a quiet source is fine to keep, add it to `references/known-quiet.md` with today's date (DD-MM-YYYY) and its last item date.
