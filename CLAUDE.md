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

During any newsletter work, log each thing Matt asks for that the skills didn't do by themselves in `.claude/skills/prep-newsletter/references/asks.md` (format in `prep-newsletter`), with the outcome and which skill it belongs in.

Skills read and write the live site through `.claude/skills/process-tips/scripts/umbfyi.sh` (run it with no args for the commands). It logs in as an Umbraco API user from `UMBFYI_BASE_URL`, `UMBFYI_CLIENT_ID` and `UMBFYI_CLIENT_SECRET`, set in the environment or in `~/.umbfyi-tips.env`. If they're missing, stop and ask Matt.

`.claude/skills/process-tips/scripts/jev.py` asks Jev (TypeSafe's fast yes/no model) one question about every item in a JSON file, for cheap first-pass filtering. It reads `TYPESAFE_API_KEY` from the environment or `~/.umbfyi-tips.env`.

- Everything is LIVE. Never test writes on a published issue. Saves go to a draft.
- Publishing the upcoming issue early is safe: the site keeps it out of listings until its `publishDate`, and each republish before then just updates the mailing system. So `prep-newsletter` (once the issue is complete) and `newsletter-topup` publish and republish it themselves, and send Matt the preview link (`https://umb.fyi/<issue>`). Limits on doing this unasked: only the upcoming issue, only before 08:45 UK on send day, never a half-built issue (no items, or no preheader).
- After the send (and from 08:45 UK on send day), fixing an issue is still fine: edits, moves, removing blocks and republishing update the web version, and the mailing system ignores changes after `publishDate`. But every change then needs Matt's yes for that change, every time, with the `publish-newsletter` skill for the republish.
- Never delete anything on the live site, except blocks inside a newsletter with `umbfyi.sh remove-block` (a cancelled event, a late drop, a mistake). Before the send, that's part of normal prep. After it, only on Matt's yes for that block; the script then needs `--after-send`.

## Newsletter facts

- Issues go out on Wednesdays at 9am UK time and are named by date (`YYYY-MM-DD`).
- `publishDate` is stored as UTC: `08:00` in British Summer Time, `09:00` in winter. Both are correct. The backoffice shows the raw UTC value, so 08:00 in summer is not a bug. Never "fix" it.
- Always get "now" from `date -u` and say times to Matt in UK time.

## How Matt likes replies

Smart but not technical. Short sentences, plain words, no jargon (if a technical word is unavoidable, add a short plain-English tag). Lead with the answer in a line or two, then bullet points, one idea each. If Matt needs to do something, say it as a direct instruction. No preamble, no narrating the process, no em dashes. Dates as DD-MM-YYYY.
