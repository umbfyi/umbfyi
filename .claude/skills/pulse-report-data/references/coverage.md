# What the workflow only knows from code

Tags, sources and package categories are read from the data, so new ones are counted with no changes. These lists are written by hand in the code. Anything new this year that isn't on them is missed or lumped in as "other".

All paths are under `src/Umb.Fyi/Workflows/Implement/PulseReport/`.

| List | Where | What it drives | Missed if not listed |
|---|---|---|---|
| Products | `PulseReportConstants.UmbracoProducts` | release counts (NuGet / GitHub / npm), advisories and breaking changes per product | a whole product's releases. Order matters: `umbraco-cms` must stay last |
| Festivals | `PulseReportConstants.Festivals` | event ripples | the festival's ripple counts |
| Event types | `PulseReportConstants.EventTypeTagsRegex` | events by type | the type, counted as a plain event |
| Tag merges | `Tasks/MergeTagsTask.cs` | joins yearly tags (`cg26`, `codegarden26` → `codegarden`) | the event split across one tag per year |
| Newsletter groups | `Tasks/CalculateCommunityVoicesTask.cs` (medium), `Tasks/CalculateTagTotalsTask.cs` (blocklist, `hq`) | community voices by medium, HQ vs community split | a new group counted as "other" |
| Emoji | `Tasks/CalculateCommunityVoicesTask.cs` (📺 youtube, 🎧 podcast) | watch-and-listen split | a new format counted as "other" |

## How to check

Get what was actually sent, both years: `umbfyi.sh featured-all <comparison-from>` (the period starts are today minus one and two years). Split the items into the two periods by date. Then:

1. **New tags.** Tags used this period but not the one before. For each, ask: is it a product, a festival, an event type, or a yearly event tag? If so, is it on the matching list (test the tag against each list's regex, don't eyeball it)? Ordinary topic tags (e.g. `migrations`) need nothing.
2. **Products.** HQ items (group `hq`, or source `umbraco`) whose title names an Umbraco product that isn't in `UmbracoProducts`. Also check products that are listed but have no NuGet, GitHub or npm source set, as they get no release counts (Compose in 2026).
3. **Festivals.** Festival section headings in the newsletter (`groupAlias` other than the usual groups) and festival-like tags. Test each against the `Festivals` regexes. Then check the URLs: ripples only count from the festival's own item, found by its Source matching one of the entry's `Urls`. Find each festival's main item this period (`umbfyi.sh featured "<name>"`) and check its Source is listed, or matches the entry's `UrlPattern`. A rebrand keeps one entry with every old and new URL, so both years land on the same row. The UK Conference (`ukconf`, rebrand of UK Festival) moves to a new year subdomain each year; its `UrlPattern` covers any `YYYY.umbracofoundation.co.uk`.
4. **Yearly tags.** Tags ending in a year or number (`cg26`, `codegarden26`, `df26`) that `MergeTagsTask` won't merge.
5. **Groups and emoji.** Group aliases and watch-and-listen emoji this period that the mediums code doesn't name.

## Report

One table: the new thing, which list it's missing from, what it would change in the report, and a suggested code line (copy the style of the entries next to it). Matt decides what goes in. Code changes then need committing and shipping before the run, and never on a Wednesday.
