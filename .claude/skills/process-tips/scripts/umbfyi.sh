#!/usr/bin/env bash
# Thin wrapper around the UMB.FYI management API for the newsletter skills (process-tips, newsletter items).
# Authenticates as an Umbraco API user (client credentials) and caches the token for its lifetime.
#
# Credentials come from the environment, or from ~/.umbfyi-tips.env if present:
#   UMBFYI_BASE_URL       e.g. https://umb.fyi (no trailing slash)
#   UMBFYI_CLIENT_ID      must start with "umbraco-back-office-"
#   UMBFYI_CLIENT_SECRET
#
# Usage:
#   umbfyi.sh tips [from-iso-date]        open tips, newest first
#   umbfyi.sh tips-all [from-iso-date]    open + dismissed tips (for learning from history)
#   umbfyi.sh search <text>               media items whose link or title contains <text> (last 6 months only)
#   umbfyi.sh featured <text> [from]      published newsletter items whose link or title contains <text> (full history)
#   umbfyi.sh featured-all <from>         every published newsletter item since <from>
#   umbfyi.sh recent <from> <to>          news media items between two ISO dates
#   umbfyi.sh events <from> <to>          event media items between two ISO dates
#   umbfyi.sh tags                        all media tags in use
#   umbfyi.sh create <json-file>          create a media item from a JSON body
#   umbfyi.sh dismiss <tip-id>            soft delete a tip
#   umbfyi.sh profiles                    known people/orgs and their source URLs (public, no login)
#   umbfyi.sh workflow-create [alias]     create a workflow run (default newsletter-generator), prints its JSON (workflowId)
#   umbfyi.sh workflow-start <id>         start a created run
#   umbfyi.sh workflow-status <id>        a run's full state (status, stages, tasks)
#   umbfyi.sh workflow-model <id>         a run's output model (mediaItems)
#   umbfyi.sh add-items <newsletter-id> <json-file>   add items as blocks after their group headings (saves a draft)
#   umbfyi.sh add-group <newsletter-id> <alias> <title> [emoji]   add a festival section heading at the top (saves a draft)
#   umbfyi.sh create-newsletter <date>    create the newsletter for a Wednesday (YYYY-MM-DD) from the Newsletter Starter blueprint (draft)
#   umbfyi.sh og-measure "<text>"         how a preheader wraps in the social images (lines, gap below logo, line texts)
#   umbfyi.sh bluesky-sweep [days] [query]   recent Bluesky posts matching a search (default: umbraco, 7 days)
#   umbfyi.sh tidy <newsletter-id>        remove placeholder poll and empty headings, place signup blocks (saves a draft)
#   umbfyi.sh upload-pdf <name> <file>    upload a PDF to the Pulse Reports media folder as an Article, prints its id
#   umbfyi.sh source-status [days]        health of each scheduled source over the last N days (default 30, max 60)

set -euo pipefail

if [[ ${1:-} == profiles ]]; then
  curl -sf https://raw.githubusercontent.com/umbfyi/umbfyi/HEAD/data/profiles.json
  exit
fi

[[ -f "$HOME/.umbfyi-tips.env" ]] && source "$HOME/.umbfyi-tips.env"
: "${UMBFYI_BASE_URL:?UMBFYI_BASE_URL not set}"
: "${UMBFYI_CLIENT_ID:?UMBFYI_CLIENT_ID not set}"
: "${UMBFYI_CLIENT_SECRET:?UMBFYI_CLIENT_SECRET not set}"

MGMT="$UMBFYI_BASE_URL/umbraco/management/api/v1"
API="$MGMT/umb-fyi"
TOKEN_CACHE="${TMPDIR:-/tmp}/umbfyi-tips-token"

token() {
  if [[ -f "$TOKEN_CACHE" ]] && (( $(date +%s) < $(cut -d' ' -f1 "$TOKEN_CACHE") )); then
    cut -d' ' -f2 "$TOKEN_CACHE"
    return
  fi
  local res
  res=$(curl -sf -X POST "$UMBFYI_BASE_URL/umbraco/management/api/v1/security/back-office/token" \
    --data-urlencode grant_type=client_credentials \
    --data-urlencode "client_id=$UMBFYI_CLIENT_ID" \
    --data-urlencode "client_secret=$UMBFYI_CLIENT_SECRET")
  local access expires
  access=$(jq -r .access_token <<<"$res")
  expires=$(jq -r .expires_in <<<"$res")
  (umask 077; echo "$(( $(date +%s) + expires - 60 )) $access" > "$TOKEN_CACHE")
  echo "$access"
}

call() {
  local method=$1 path=$2; shift 2
  curl -s --fail-with-body -X "$method" "$API$path" -H "Authorization: Bearer $(token)" "$@"
}

wf() {
  local method=$1 path=$2; shift 2
  curl -s --fail-with-body -X "$method" "$UMBFYI_BASE_URL/api/workflows$path" -H "Authorization: Bearer $(token)" "$@"
}

# Newsletter Starter blueprint, the Archive page newsletters live under, and the newsletter template.
# Keys are the same on local and live (Umbraco Deploy keeps them).
NEWSLETTER_BLUEPRINT=6febf968-81f4-43cf-972a-0a5293a49db9
NEWSLETTER_ARCHIVE=028b21ee-6da5-4e54-b6cd-e73f6c33b85b
NEWSLETTER_TEMPLATE=addcb633-ddfc-4539-a6c8-6a9365d0b322

# Same two calls the backoffice makes: the scaffold gives every block a fresh key and runs the site's
# own defaults (SetNewsletterDefaultValuesNotificationHandler: name = the coming Wednesday, today on a Wednesday,
# publishDate = 9am Europe/London stored as UTC), then the page is created from it. The expected
# date is checked against the scaffold's name so nothing is created for the wrong week. The
# scaffold has no template, so set the newsletter one.
create_newsletter() {
  local date=$1 scaffold name body headers id
  [[ $date =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || { echo "Usage: create-newsletter YYYY-MM-DD" >&2; exit 1; }
  scaffold=$(curl -s --fail-with-body "$MGMT/document-blueprint/$NEWSLETTER_BLUEPRINT/scaffold" -H "Authorization: Bearer $(token)")
  name=$(jq -r '.variants[0].name' <<<"$scaffold")
  [[ $name == "$date" ]] || { echo "The site would create $name, not $date. Nothing created." >&2; exit 1; }
  body=$(jq --arg parent "$NEWSLETTER_ARCHIVE" --arg template "$NEWSLETTER_TEMPLATE" '{
    parent: {id: $parent}, documentType: {id: .documentType.id}, template: {id: $template},
    values: [.values[] | {alias, culture, segment, value}],
    variants: [.variants[] | {culture, segment, name}]}' <<<"$scaffold")
  headers=$(curl -s --fail-with-body -D - -o /dev/null -X POST "$MGMT/document" -H "Authorization: Bearer $(token)" \
    -H "Content-Type: application/json" --data-binary "$body")
  id=$(grep -i '^umb-generated-resource:' <<<"$headers" | awk '{print $2}' | tr -d '\r')
  [[ -n $id ]] || { echo "Create failed" >&2; exit 1; }
  jq -n --arg id "$id" --argjson s "$scaffold" '{id: $id, name: $s.variants[0].name,
    publishDate: ($s.values[] | select(.alias == "publishDate") | .value)}'
}

# Pulse Reports media folder and the Article media type (used for PDFs).
PULSE_REPORTS_FOLDER=d6bd4328-a019-4732-975c-69d40a49e49f
ARTICLE_MEDIA_TYPE=a43e3414-9599-4230-a7d3-943a21b20122

# Same two calls the backoffice makes: upload the file as a temporary file, then create the media item from it.
upload_pdf() {
  local name=$1 file=$2 tmp body headers id
  [[ -n $name && -f $file ]] || { echo "Usage: upload-pdf <name> <file.pdf>" >&2; exit 1; }
  tmp=$(uuidgen | tr '[:upper:]' '[:lower:]')
  curl -s --fail-with-body -X POST "$MGMT/temporary-file" -H "Authorization: Bearer $(token)" \
    -F "Id=$tmp" -F "File=@$file;type=application/pdf" >/dev/null
  body=$(jq -n --arg parent "$PULSE_REPORTS_FOLDER" --arg type "$ARTICLE_MEDIA_TYPE" --arg tmp "$tmp" --arg name "$name" '{
    parent: {id: $parent}, mediaType: {id: $type},
    values: [{alias: "umbracoFile", culture: null, segment: null, value: {temporaryFileId: $tmp}}],
    variants: [{culture: null, segment: null, name: $name}]}')
  headers=$(curl -s --fail-with-body -D - -o /dev/null -X POST "$MGMT/media" -H "Authorization: Bearer $(token)" \
    -H "Content-Type: application/json" --data-binary "$body")
  id=$(grep -i '^umb-generated-resource:' <<<"$headers" | awk '{print $2}' | tr -d '\r')
  [[ -n $id ]] || { echo "Upload failed" >&2; exit 1; }
  echo "$id"
}

cmd=${1:-}; shift || true
case "$cmd" in
  tips)     call GET "/tips${1:+?from=$1}" ;;
  tips-all) call GET "/tips?includeDeleted=true${1:+&from=$1}" ;;
  search)   call GET "/media-items/search" -G --data-urlencode "q=$1" ;;
  featured) call GET "/newsletter-items" -G --data-urlencode "q=$1" ${2:+--data-urlencode "from=$2"} ;;
  featured-all) call GET "/newsletter-items?from=$1" ;;
  recent)   call GET "/media-items?type=news&from=$1&to=$2" ;;
  events)   call GET "/media-items?type=events&from=$1&to=$2" ;;
  tags)     call GET "/media-tags" ;;
  create)   call POST "/media-items" -H "Content-Type: application/json" --data-binary "@$1" ;;
  dismiss)  call POST "/tip/$1/dismiss" ;;
  add-items) call POST "/newsletter/$1/items" -H "Content-Type: application/json" --data-binary "@$2" ;;
  tidy)     call POST "/newsletter/$1/tidy" ;;
  bluesky-sweep) call GET "/social-sweep/bluesky" -G --data-urlencode "days=${1:-7}" --data-urlencode "q=${2:-umbraco}" ;;
  source-status) call GET "/source-status${1:+?days=$1}" ;;
  og-measure) call GET "/og-measure" -G --data-urlencode "text=$1" ;;
  create-newsletter) create_newsletter "${1:-}" ;;
  upload-pdf) upload_pdf "${1:-}" "${2:-}" ;;
  add-group) call POST "/newsletter/$1/groups" -H "Content-Type: application/json" \
               -d "$(jq -n --arg a "$2" --arg t "$3" --arg e "${4:-}" '{alias:$a, title:$t, emoji:$e}')" ;;
  # The workflow API sits outside the management API, at /api/workflows, but takes the same token.
  workflow-create) wf POST "" -H "Content-Type: application/json" \
                     -d "$(jq -n --arg a "${1:-newsletter-generator}" '{workflowAlias:$a}')" ;;
  workflow-start)  wf POST "/$1/start" ;;
  workflow-status) wf GET "/$1" ;;
  workflow-model)  wf GET "/$1/model" ;;
  *) sed -n '2,33p' "$0"; exit 1 ;;
esac
