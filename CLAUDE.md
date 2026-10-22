# UMB.FYI

UMB.FYI is a weekly Umbraco community newsletter and site (https://umb.fyi), run by Matt. This repo is its public side: shared data files, plus the Claude skills used to prep each issue. The site itself is an Umbraco 17 site on Umbraco Cloud, in a separate private repo.

## This repo is public

Anything committed here is visible to anyone. Never commit secrets, API keys, tokens, client secrets or private data (subscriber details, unpublished reports, CRM data). Credentials come from the environment only (see below).

## Layout

- `data/`: `profiles.json`, `tag-map.json`, `topics.json`. Read by the live site. Format in `data/README.md`, schemas in `schemas/`. Validate with `npm run validate:profiles` / `validate:topics`. Outside contributions come in as PRs.
- `.claude/skills/`: the newsletter and Pulse Check skills. Start from `prep-newsletter` for a full week's prep.
- `.mcp.json`: the hosted Umbraco MCP servers for the LIVE site. Kept for exploring the site when building features. Skills don't use them.

## The site code

The Umbraco Cloud repo is checked out next to this one at `../UMB.FYI.v17`. Code paths in skills (`src/...`) are relative to it, and builds, git and commits for site code happen there. It isn't there on Claude on the web: skip code steps and say so.

Pushing `master` in `../UMB.FYI.v17` deploys straight to live and restarts the site. Never push without Matt's go, and never on a Wednesday (newsletter day) unless he says so.

## Talking to the live site

Skills read and write the live site through `.claude/skills/process-tips/scripts/umbfyi.sh` (run it with no args for the commands). It logs in as an Umbraco API user from `UMBFYI_BASE_URL`, `UMBFYI_CLIENT_ID` and `UMBFYI_CLIENT_SECRET`, set in the environment or in `~/.umbfyi-tips.env`. If they're missing, stop and ask Matt.

- Everything is LIVE. Never test writes on a published issue. Saves go to a draft.
- Never publish anything unless Matt says "publish" in his own words. Then use the `publish-newsletter` skill.
- Never delete anything on the live site.

## Newsletter facts

- Issues go out on Wednesdays at 9am UK time and are named by date (`YYYY-MM-DD`).
- `publishDate` is stored as UTC: `08:00` in British Summer Time, `09:00` in winter. Both are correct. The backoffice shows the raw UTC value, so 08:00 in summer is not a bug. Never "fix" it.
- Always get "now" from `date -u` and say times to Matt in UK time.

## How Matt likes replies

Smart but not technical. Short sentences, plain words, no jargon (if a technical word is unavoidable, add a short plain-English tag). Lead with the answer in a line or two, then bullet points, one idea each. If Matt needs to do something, say it as a direct instruction. No preamble, no narrating the process, no em dashes. Dates as DD-MM-YYYY.
