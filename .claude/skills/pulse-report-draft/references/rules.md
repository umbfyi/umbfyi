# Pulse Check rules

## Docs

Drive folder: `0AKHvWRlo7ywPUk9PVA`.

| Report | Doc ID | State |
|---|---|---|
| 2024 \| 2025 | `1jGu6lL6q4HetZVUW2vxpaJ03vUSo1ZbUJnYBpYaFJS0` | published |
| 2025 \| 2026 | `18VnwRmKMxOBXqcdyfBZWtbba4RV9qHjOAbFXbqPsX4A` | published |

Add each year's final doc here once it's out.

## Tone

- Soft and story-like. The "pulse" and "rhythm" image runs through it: beat, tempo, quickening, steady.
- Hedge every reading of the data: "suggests", "hints at", "seems", "may". State numbers as fact, read meaning gently.
- Each section opens with one framing line, then compares with last year, then reads what it means.
- Name people only in Community Voices, and only from the data.
- No hype, no blame. A drop is "quieter" or "eased", not "fell sharply".
- British spelling (organisers, modernisation).

## Length

- About 2,500 to 2,800 words in all. Last year's length is the guide.
- At most four paragraphs per section.
- One takeaway box per section (except Preface, Methodology, Acknowledgements, Disclaimer). One sentence, starting "Takeaway:".

## Formatting

Copying last year's doc keeps all of this. Only reapply it to new text.

- A4. Body: Lato, weight 300, 12pt, #434343.
- H1: " NN." in Lato 300, then the name in Lato 400, 25pt, #1b264f. Page break before each. Pink bar image under each.
- Use weight 400 for emphasis, not `bold: true`. "Bold" in the old doc is Lato 400.
- Tables: navy #1b264f header row, #f3f3f3 stripes.
- Takeaway: a 1x1 table, grey fill, 3pt left border.
- The navy cover is a behind-text image the Docs API can't see or add. It survives a copy. If it's ever lost, Matt pastes it by hand.

## Section map

Keep all 13, in this order. "Data" is where in the JSON (`P` = `.period.data`, `C` = `.comparisonPeriod.data`).

| # | Section | Data | Table / chart |
|---|---|---|---|
| 01 | Preface | none. Update the edition number ("second edition", "third edition") and what's new this year. Signed "— Matt Brailsford, UMB.FYI". | |
| 02 | Year in brief | the five agreed themes | Metric table (Security Advisories, Breaking Changes, Community Posts, Events Activity, New Packages: last year, this year, change). Chart "Pulse Meters Snapshot". |
| 03 | Tag pulse: HQ vs community | `tags.segments`, `tags.crossSegment`, `topTags`, `topTagsComparatives`, `tagSourceDiversity` | chart |
| 04 | Events & meetups | `events.byMonth`, `byType`, `meetups`, `ripples` | chart |
| 05 | Security & stability | `securityAdvisories`, `securityAdvisoriesSummary`, `breakingChanges`, `breakingChangesSummary` | Advisories by version table. Chart "Security Advisories by Version". |
| 06 | Product release cadence | `productReleases` | Product table (Total, Features = majors + minors, Maintenance = patches, RCs & previews). Chart "Product Release Focus". |
| 07 | Marketplace | `marketplace` | chart |
| 08 | Community voices | `communityVoices` | New vs returning table. Chart "New vs Returning Voices". |
| 09 | The watchlist | last year's watchlist + this year's data | Open by checking last year's predictions. |
| 10 | Recommendations | all of it | Three H3s: For site owners, For package authors, For community organisers. |
| 11 | Methodology | periods from `period` / `comparisonPeriod` | Name every data quirk that shaped a number (see `pulse-report-data` checks). |
| 12 | Acknowledgements | none | Light refresh only. |
| 13 | Disclaimer | none | Keep as is. |

## Data rules

- Use one number per fact across the whole doc. If two sections need the same total, take it from the same field.
- Outside facts (e.g. DevRel's meetup attendance figure) only if Matt gives them. Say where they came from in the text.
- New products have no last year. Say "arrived in <month>", not "up from 0".
- Package version support is today's, not launch day's. Say so in Methodology.
