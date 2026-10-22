# Pulse report data: checks

The JSON is the workflow model, camelCase. `period` is the year being reported, `comparisonPeriod` the year before. Each has `from`, `to` and `data` (shape in `PulseReportModel.cs`).

## Headline numbers

The same rows as the "Year in brief" table in last year's report. `P` = `.period.data`, `C` = `.comparisonPeriod.data`.

| Row | Where |
|---|---|
| Security Advisories | `P.securityAdvisories \| length` |
| Breaking Changes | `P.breakingChanges \| length` |
| Community Posts | `P.communityVoices.totalPosts` |
| Community Voices | `P.communityVoices.totalVoices` |
| Events Activity | sum of `P.events.byType` |
| Meetups | `P.events.meetups.total` |
| New Packages | `P.marketplace.newPackagesTotal` |

If a path is missing or the number looks off, check `PulseReportModel.cs` and the task that fills it before guessing. Use one source per number and say which, so the draft never shows two different totals for the same thing.

## Known quirks

Each one has come up before. Count it, show a few examples, and say what it means for the report.

1. **Source is a name, not a URL.** Some newsletter items have a person or org name in Source. Their posts may be counted under the wrong voice, or split across two. Look in `communityVoices.topVoices` for sources that aren't URLs or look like the same person twice.
2. **Unresolved source URLs show up as "voices".** A raw URL (e.g. a blog domain) in the top voices list means the source wasn't matched to a profile. Name them so Matt can add them to profiles and run again.
3. **Package version support is today's, not launch day's.** `marketplace.newPackages.*.byVersionSupport` reflects what packages support now. Fine to use, but the report must say so (Methodology).
4. **"Unknown" package category.** Note the share of new packages in `Unknown`. Last year it was about a third.
5. **New products with no history.** Products in `productReleases` with no match in the comparison period (e.g. Umbraco AI, Automate in 2026). Not an error, but the draft must not show them as growth from zero.
6. **Products missing from release tracking.** Compare product names with what HQ shipped this year. In 2026 Umbraco Compose wasn't tracked. Anything missing must be named in Methodology.
