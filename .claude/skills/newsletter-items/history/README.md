# Items history

One file per issue (`YYYY-MM-DD.json`), written by `newsletter-items` step 11 with `scripts/save_history.py`. Each says, per item: what the workflow found, what Claude proposed (keep, changed, drop, unsure), and what went out, with which fields Claude and Matt changed.

This repo is public, so the files hold only links, titles, groups and tags. No summaries, no drop reasons, no workflow logs.

## Open tips

`<issue>-open-tips.json` lists unsure tips a phone run would drop but left open, so Matt could still `flip` them: `[{"id", "link", "title"}]`, nothing about who sent them. The `newsletter-close` run after the send (Wednesday 09:15 UTC) dismisses any still open (no flip means he agreed) and empties the file.
