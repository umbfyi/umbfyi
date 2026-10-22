---
name: pulse-report-draft
description: Write the draft of the yearly UMB.FYI Pulse Check report as a Google Doc. Copies last year's report so the look carries over, then rewrites each of the 13 sections from the new pulse report JSON, section by section with Matt. Never shares or publishes. Use when asked to write, draft or start the Pulse Check or pulse report, or after the pulse-report-data skill.
---

# Pulse report draft

The Pulse Check is a yearly report (out around October) built from the `state-of-umbraco` workflow data. Each year should look and read like the last one, with content that follows the new data.

Read before every run:
- `references/rules.md`: tone, length, formatting and the section map. It wins over anything general you think you know.
- `references/example-2025-2026.md`: the 2025|2026 text. Use it as the voice to match, not as text to reuse.

## Run

1. **Get the data.** Ask for the JSON path. If there isn't one from this session, run the `pulse-report-data` skill first. Don't write from data that hasn't been through its checks.
2. **Find last year's report.** In the Drive folder `0AKHvWRlo7ywPUk9PVA`, the newest published "UMB.FYI Pulse Check - YYYY | YYYY" doc (not a draft). Known IDs are in `references/rules.md`. Confirm the one you pick with Matt.
3. **Copy it.** Copy that doc into the same folder as "UMB.FYI Pulse Check - <from year> | <to year> - Draft v1". Copying keeps the cover image, pink bars, fonts and table styles, which the Docs API can't recreate. Give Matt the link.
4. **Read last year's numbers.** Pull every number and claim from the copy, so each section can say how things moved ("up from 17 to 23"). Where last year's report and the `comparisonPeriod` data disagree, use the data and note it once in Methodology (both years are recalculated each run).
5. **Plan the story.** Before writing, list in chat the five "Year in brief" themes you'd pick, one line each, with the number behind each. Wait for Matt to agree or change them. The themes drive every other section.
6. **Write section by section.** Follow the section map in `references/rules.md`. For each section: replace the body text, update its table, update the takeaway box. Keep the heading, styles and layout as they are. Do two or three sections per turn, give Matt the link and a one-line summary of each, and wait before going on.
7. **Charts.** The chart images can't be made through the Docs API. Leave last year's images in place (the Docs tools can't add comments either). Write `charts.md` in the scratchpad: one small table per chart, named by its caption, with the new numbers it should show. Give Matt the full path at the end.
8. **Finish.** Put "AI-assisted draft — pending review" at the top of the doc. Check the word count (target in `references/rules.md`). Then list for Matt: charts to redo, any numbers you weren't sure of, and the cover year to check.

Never share the doc, change its permissions, or send it to anyone. That's Matt's call.

Once Matt says the doc is final, the `pulse-report-publish` skill puts it on the website.
