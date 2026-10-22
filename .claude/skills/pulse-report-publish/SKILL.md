---
name: pulse-report-publish
description: Put the finished UMB.FYI Pulse Check report on the website. Uploads the PDF to the "Pulse Reports" media folder on the live site and adds a link to it at the top of the list on the /pulse page. Saves a draft and publishes only on Matt's go. Use when asked to publish, upload, put live or add the Pulse Check or pulse report to the site, or after the pulse-report-draft skill once the doc is final.
---

# Pulse report publish

The /pulse page lists every Pulse Check as a link to its PDF, newest first. Each PDF is an Article media item in the "Pulse Reports" media folder.

Live site, so this is outward-facing. Reads need no sign-off. The upload and the page edit wait for Matt's go in step 4. Publishing the page waits for a second go in step 6.

Tools: the PDF upload goes through `.claude/skills/process-tips/scripts/umbfyi.sh upload-pdf` (the Editor MCP can't upload a local file). Everything else uses the `umbraco-editor-mcp` tools.

| Thing | ID |
|---|---|
| Pulse page (/pulse) | `3921c7c6-2288-471f-af0e-c6a5ddf6797c` |
| Pulse Reports media folder | `d6bd4328-a019-4732-975c-69d40a49e49f` |

## Run

1. **Check the doc is final.** Ask Matt for the final Google Doc. Confirm the review is done and the "AI-assisted draft — pending review" line at the top is gone (the Disclaimer section stays and covers the AI use). If not final, stop.
2. **Get the PDF.** Export the doc with the Google Drive `download_file_content` tool, `exportMimeType: application/pdf`. This is the same file as Google Docs' File → Download → PDF (the 2025-2026 export came out byte for byte the same as the PDF on the site). The result is too big for chat, so it lands in a tool-results file: decode it with `jq -r .content <file> | base64 -d > <scratchpad>/umbfyi-pulse-check-YYYY-YYYY.pdf`, matching past years' file names. Check `file` says it's a PDF and the size is close to last year's (about 680 KB). If the export fails, ask Matt to download it by hand into the repo's `exports/` folder (git-ignored; the shell can't read `~/Downloads`).
3. **Check what's there.** `list-media-children` on the media folder and `get-page` on the Pulse page. If this year's report is already uploaded or linked, say so and stop. Past years for the naming:
   - Media name: `UMB.FYI Pulse Check 2025 2026`
   - Link text: `UMB.FYI Pulse Check 2025-2026`
4. **Show the plan and wait.** One short list: the media name, the file, and the new link line as it will read on the page. Wait for Matt's go.
5. **Upload and link.**
   - `umbfyi.sh upload-pdf "UMB.FYI Pulse Check YYYY YYYY" <scratchpad>/umbfyi-pulse-check-YYYY-YYYY.pdf` prints the new media id. Check it with `get-media`: the URL should end in `.pdf`.
   - Add the new link as the first `<li>` in the list under "Latest Pulse Check" in the page's `bodyText`, copying the 2025-2026 line exactly: `<li><p><a href="/{localLink:<media-id>}" title="UMB.FYI Pulse Check YYYY YYYY" type="media">UMB.FYI Pulse Check YYYY-YYYY</a></p></li>`. Leave every other line as it is.
   - Save with `edit-page` (draft only). Call `get-property-value-template` for `Umbraco.RichText` first to get the value shape right, and send the full markup.
6. **Check and publish.** `get-page` again and show Matt the list as it now reads. Publish with `save-and-publish` only when he says go.
7. **Finish.** Give Matt the page link (https://umb.fyi/pulse) and the PDF link. Add the final doc's ID to the table in `.claude/skills/pulse-report-draft/references/rules.md` as "published".

If an upload went wrong, say so and leave the media item for Matt to delete. Never delete anything on the live site yourself.
