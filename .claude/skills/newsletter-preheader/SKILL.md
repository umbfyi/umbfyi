---
name: newsletter-preheader
description: Write the preheader for this week's UMB.FYI newsletter on the live site. Picks three strong items from the issue (HQ and security news first), writes "Item 1, Item 2, Item 3 and much more...", checks it fits the social images by measuring the real line wrap, and saves it once Matt picks one. Never publishes. Use when asked for the preheader, the subject line text, the social image text, or as the last step of newsletter prep.
---

# Newsletter preheader

The preheader is the short line shown after the email subject, and it's also the text drawn on the issue's social images (LinkedIn and other social, and Instagram). It's always three of the issue's items and a fixed ending: `<Item 1>, <Item 2>, <Item 3> and much more...`

Calls: the hosted `umbraco-editor-mcp` to read the issue and save the preheader (LIVE site), and `.claude/skills/process-tips/scripts/umbfyi.sh og-measure "<text>"` to check the fit. Reads and measuring need no sign-off; the one write (step 6) happens only after Matt picks.

## Run

1. **Find the issue.** As in `weekly-cryptic` step 1: the newsletter under Archive whose `publishDate` is still in the future. Note whether it's already published, and whether it already has a preheader (show it, and ask whether to replace it).
2. **Read the items.** `inspect-blocks` on the issue (`propertyAlias: "content"`). Note each item's group, title and link. If the issue has few or no items yet, stop: the preheader comes last, once the items are in.
3. **Pick three.** Strongest first. In rough order:
   - Security advisories and patches (HQ). Always in, and usually first. Several in one week become one phrase: "Umbraco CMS, Forms & AI Security Advisories".
   - A festival or big event with its own section this week (Codegarden, Spark, US Fest, UK Conference...). Can lead in its week.
   - Other HQ news: releases, product updates, big announcements, price updates, new teams or programmes. A uProfile counts, but ranks below real news.
   - The most notable community items: something new launched, a package or tool many will care about, a standout post or video, a community programme opening.
   - Spread them out: not three from the same group if there's a good choice elsewhere. Skip events other than festivals, packages (unless it's a big one), and social posts unless it's genuinely the news of the week.
4. **Write it.** Shorten each item to a short headline, usually 2 to 6 words, keeping the key name: "Examine 4 Out Now", "Ben Szymanski uProfile", "Annual Price Update 2027", "Codegarden 26 roundups & videos". Title-style capitals, no full stops, no em dashes. Join with commas and end with ` and much more...` exactly (no space before the dots). Write three versions: different picks or different wording.
5. **Check the fit.** Run `umbfyi.sh og-measure "<text>"` on each version. It measures the actual wrap in each image size, with the same font and layout the images are drawn with. Character counts are a poor guide, so always measure.
   - **Social (`image1200x627`): 4 lines at most.** Hard rule.
   - **Instagram (`image1080`): 7 lines at most.** At 8 the text runs into the logo (`gapBelowLogo` under about 100 is too close).
   - **No single word alone on a line** in the social image (`singleWordLines`). On Instagram it's better avoided ("more..." alone on the last line is the usual case), but not required.
   - If a version breaks a hard rule, shorten a phrase and measure again. Only show versions that pass.
6. **Show and save.** Show the three versions, each with its line counts (`social 4 lines, Instagram 6 lines`) and any soft issue. Recommend one, in one line. Once Matt picks (or edits one, which you measure again before saving), save it with `edit-page` on the issue: property `preheader`, the text as the value. Then `get-page` and confirm it saved exactly.
7. **Never publish.** If the issue was already published (step 1), tell Matt to publish it again so the new preheader reaches the mailing system and the images. Finish with one line: the saved preheader, and whether it needs republishing.

## Past preheaders

For style. All fit 4 lines on the social image.

- `2026-07-08`: Security Advisory July 7 2026, UMBRAAD Videos now on YouTube, Dutch Umbraco Alliance Festival Announced and much more...
- `2026-07-15`: Launching Umbraco Automate, Migrating from v13 to v17, UmbraCymru Umbraco AI Hackathon and much more...
- `2026-08-12`: Codegarden 2026 Videos Online, Gia Matikainen uProfile, Unlocking the Power of Umbraco's Commercial Products and much more...
- `2026-08-19`: Umbraco CMS, Forms & AI Security Advisories, Umbraco India Festival, Umbraco Automate for Developers or Marketeers and much more...
- `2026-08-26`: Umbraco India Festival, Introducing Umbraco Copilot Workspace, Examine 4 Out Now and much more...
- `2026-09-02`: Umbraco Achieves B Corp Certification, Automated Umbraco Log Monitoring, Extending the Delivery API's Content Response and much more...
- `2026-09-30`: Umbraco Q3 Product Update, Umbraco US Festival 2026, Decision based Automation with Jev and much more...
- `2026-10-07`: Security Advisory Oct 6, 26, Annual Price Update 2027, The Umbraco MCP Benchmark and much more...
- `2026-10-14`: Umbraco UK Conference, UMB.FYI Pulse Check Report, uSync AI support and much more...
- `2026-10-21`: Package Team & Core Collaborators Team Applications Open, Upgrade or Rewrite, Umbraco Community Hour and much more...
