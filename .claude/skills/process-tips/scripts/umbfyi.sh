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
#   umbfyi.sh puzzle-answers              every past minute cryptic answer, newest first, from umb.fyi/puzzles (public, no login)
#   umbfyi.sh workflow-create [alias]     create a workflow run (default newsletter-generator), prints its JSON (workflowId)
#   umbfyi.sh workflow-start <id>         start a created run
#   umbfyi.sh workflow-status <id>        a run's full state (status, stages, tasks)
#   umbfyi.sh workflow-model <id>         a run's output model (mediaItems)
#   umbfyi.sh add-items <newsletter-id> <json-file>   add items as blocks after their group headings (saves a draft)
#   umbfyi.sh add-group <newsletter-id> <alias> <title> [emoji]   add a festival section heading at the top (saves a draft)
#   umbfyi.sh create-newsletter <date>    create the newsletter for a Wednesday (YYYY-MM-DD) from the Newsletter Starter blueprint (draft)
#   umbfyi.sh og-measure "<text>"         how a preheader wraps in the social images (lines, gap below logo, line texts)
#   umbfyi.sh bluesky-sweep [days] [query]   recent Bluesky posts matching a search (default: umbraco, 7 days)
#   umbfyi.sh linkedin-sweep [days]       recent LinkedIn posts mentioning Umbraco, collected by Umbraco Sphere (default 7 days)
#   umbfyi.sh tidy <newsletter-id>        remove placeholder poll and empty headings, place signup blocks (saves a draft)
#   umbfyi.sh upload-pdf <name> <file>    upload a PDF to the Pulse Reports media folder as an Article, prints its id
#   umbfyi.sh source-status [days]        health of each scheduled source over the last N days (default 30, max 60)
#   umbfyi.sh newsletters [n]             the newest n newsletters under Archive (default 4): id, name, state, publishDate, preheader
#   umbfyi.sh get-newsletter <id>         one newsletter with its blocks in page order (type, contentKey, values)
#   umbfyi.sh set-preheader <id> "<text>" [--dry-run]   save the preheader (saves a draft)
#   umbfyi.sh set-linkedin <id> <text-file> [--dry-run]   save the LinkedIn post from a text file (saves a draft)
#   umbfyi.sh set-puzzle <id> <json-file> [--dry-run]   fill the Minute Cryptic block from {clue, enumeration, ...} (saves a draft)
#   umbfyi.sh publish-newsletter <id> [--dry-run]       publish a newsletter (syncs it to the mailing system). Only on Matt's word.

set -euo pipefail

if [[ ${1:-} == profiles ]]; then
  curl -sf https://raw.githubusercontent.com/umbfyi/umbfyi/HEAD/data/profiles.json
  exit
fi

# The puzzles page shows 10 puzzles a page (?p=2 and on), each answer in a hidden
# <p data-part="answer"><span class="font-bold">ANSWER</span>. Reads pages until one has none.
if [[ ${1:-} == puzzle-answers ]]; then
  for (( p = 1; p <= 100; p++ )); do
    page=$(curl -sf "https://umb.fyi/puzzles?p=$p" | grep -o 'data-part="answer"[^>]*><span class="font-bold">[^<]*' | sed 's/.*>//') || true
    [[ -n $page ]] || break
    echo "$page"
  done | jq -R . | jq -s .
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

doc() { curl -s --fail-with-body "$MGMT/document/$1" -H "Authorization: Bearer $(token)"; }

# Block element types in a newsletter's content property, by key.
BLOCK_TYPES='{"c00d9369-6b0e-439b-8847-61e0d1067e83":"group","808cbd76-e16f-44cb-93ca-f2b207771514":"item",
  "f78699d6-a74b-41d5-b0b7-7d3d1e5efe6a":"signup","122f1a69-fa4c-44f3-ab12-f4f023d30706":"puzzle","6a7044a5-3466-489f-b09d-f62d921f2541":"poll"}'

# The newsletter fields the skills need, from a full document. publishDate is the send time (UTC), not when it was last published.
summary() {
  jq '{id, name: .variants[0].name, state: .variants[0].state,
    publishDate: ((.values[] | select(.alias == "publishDate") | .value) // null),
    preheader: ((.values[] | select(.alias == "preheader") | .value) // null),
    linkedInPost: ((.values[] | select(.alias == "linkedInPost") | .value) // null)}'
}

# Newest first by name (names are dates). The collection view leaves out values, so each one is read in full.
newsletters() {
  local n=${1:-4} id
  for id in $(curl -s --fail-with-body "$MGMT/collection/document/$NEWSLETTER_ARCHIVE?orderBy=name&orderDirection=Descending&skip=0&take=$n" \
      -H "Authorization: Bearer $(token)" | jq -r '.items[].id'); do
    doc "$id" | summary
  done | jq -s .
}

get_newsletter() {
  local d
  d=$(doc "$1")
  jq --argjson types "$BLOCK_TYPES" --argjson s "$(summary <<<"$d")" '
    (.values[] | select(.alias == "content") | .value) as $c
    | ($c.contentData | map({key: .key, value: .}) | from_entries) as $byKey
    | $s + {blocks: [$c.layout["Umbraco.BlockList"] | to_entries[] | $byKey[.value.contentKey] as $b
        | {n: (.key + 1), type: ($types[$b.contentTypeKey] // $b.contentTypeKey), contentKey: $b.key,
           values: ($b.values | map({key: .alias, value: .value}) | from_entries)}]}' <<<"$d"
}

# Same save the backoffice makes: send the whole document back with one change. Saves a draft, never publishes.
save_document() {
  local id=$1 json=$2 body
  body=$(jq '{template, values: [.values[] | {alias, culture, segment, value}], variants: [.variants[] | {culture, segment, name}]}' <<<"$json")
  curl -s --fail-with-body -X PUT "$MGMT/document/$id" -H "Authorization: Bearer $(token)" \
    -H "Content-Type: application/json" --data-binary "$body" >/dev/null
}

set_preheader() {
  local id=${1:-} text=${2:-} dry=${3:-} before after saved
  [[ -n $id && $# -ge 2 ]] || { echo 'Usage: set-preheader <id> "<text>" [--dry-run]' >&2; exit 1; }
  before=$(doc "$id")
  after=$(jq --arg t "$text" 'if any(.values[]; .alias == "preheader")
    then .values |= map(if .alias == "preheader" then .value = $t else . end)
    else .values += [{alias: "preheader", culture: null, segment: null, value: $t}] end' <<<"$before")
  jq -n --argjson b "$(summary <<<"$before")" --arg t "$text" '{name: $b.name, state: $b.state, before: $b.preheader, after: $t}'
  [[ $dry == --dry-run ]] && { echo "Dry run: nothing saved." >&2; return; }
  save_document "$id" "$after"
  saved=$(doc "$id" | summary | jq -r '.preheader // ""')
  [[ $saved == "$text" ]] || { echo "Saved, but the preheader reads back as: $saved" >&2; exit 1; }
  echo "Saved as a draft."
}

# The LinkedIn post is several lines, so it comes from a file. Make.com reads it from the published page
# ({url}?altTemplate=LinkedIn) when the issue is sent.
set_linkedin() {
  local id=${1:-} file=${2:-} dry=${3:-} text before after saved
  [[ -n $id && -f $file ]] || { echo "Usage: set-linkedin <id> <text-file> [--dry-run]" >&2; exit 1; }
  text=$(cat "$file")
  before=$(doc "$id")
  after=$(jq --arg t "$text" 'if any(.values[]; .alias == "linkedInPost")
    then .values |= map(if .alias == "linkedInPost" then .value = $t else . end)
    else .values += [{alias: "linkedInPost", culture: null, segment: null, value: $t}] end' <<<"$before")
  jq -n --argjson b "$(summary <<<"$before")" --arg t "$text" '{name: $b.name, state: $b.state, before: $b.linkedInPost, after: $t}'
  [[ $dry == --dry-run ]] && { echo "Dry run: nothing saved." >&2; return; }
  save_document "$id" "$after"
  saved=$(doc "$id" | summary | jq -r '.linkedInPost // ""')
  [[ $saved == "$text" ]] || { echo "Saved, but the LinkedIn post reads back differently: $saved" >&2; exit 1; }
  echo "Saved as a draft."
}

# Fills the one Minute Cryptic block. Only the eight puzzle fields are accepted; any not in the file are left as they are.
set_puzzle() {
  local id=$1 file=$2 dry=${3:-} before after key saved
  [[ -n $id && -f $file ]] || { echo "Usage: set-puzzle <id> <json-file> [--dry-run]" >&2; exit 1; }
  jq -e 'type == "object" and (keys - ["clue","enumeration","definition","indicator","device","fodder","answer","explanation"] | length == 0)' "$file" >/dev/null \
    || { echo "The file must be an object with only: clue, enumeration, definition, indicator, device, fodder, answer, explanation" >&2; exit 1; }
  before=$(doc "$id")
  key=$(jq -r '[.values[] | select(.alias == "content") | .value.contentData[] | select(.contentTypeKey == "122f1a69-fa4c-44f3-ab12-f4f023d30706") | .key]
    | if length == 1 then .[0] else error("expected one puzzle block, found \(length)") end' <<<"$before") || exit 1
  after=$(jq --arg k "$key" --slurpfile f "$file" '
    def editor($a): if $a == "explanation" then "Umbraco.TextArea" else "Umbraco.TextBox" end;
    (.values[] | select(.alias == "content") | .value.contentData[] | select(.key == $k) | .values) |=
      (reduce ($f[0] | to_entries[]) as $e (.;
        if any(.[]; .alias == $e.key) then map(if .alias == $e.key then .value = $e.value else . end)
        else . + [{editorAlias: editor($e.key), culture: null, segment: null, alias: $e.key, value: $e.value}] end))' <<<"$before")
  jq -n --argjson b "$(summary <<<"$before")" --arg k "$key" --argjson old "$(jq --arg k "$key" '[.values[] | select(.alias == "content") | .value.contentData[] | select(.key == $k) | .values[] | {key: .alias, value}] | from_entries' <<<"$before")" \
    --slurpfile f "$file" '{name: $b.name, state: $b.state, puzzleBlock: $k, before: $old, after: ($old + $f[0])}'
  [[ $dry == --dry-run ]] && { echo "Dry run: nothing saved." >&2; return; }
  save_document "$id" "$after"
  saved=$(doc "$id" | jq --arg k "$key" '[.values[] | select(.alias == "content") | .value.contentData[] | select(.key == $k) | .values[] | {key: .alias, value}] | from_entries')
  jq -e --slurpfile f "$file" --argjson s "$saved" -n '$f[0] | to_entries | all(.value == $s[.key])' >/dev/null \
    || { echo "Saved, but the puzzle reads back differently: $saved" >&2; exit 1; }
  echo "Saved as a draft."
}

NEWSLETTER_TYPE=119ae1bc-9453-455a-ab66-f53c5455a50d

# Same call as the backoffice's Publish button. Refuses anything that isn't a newsletter, or one with nothing new to publish.
publish_newsletter() {
  local id=${1:-} dry=${2:-} before s state
  [[ -n $id ]] || { echo "Usage: publish-newsletter <id> [--dry-run]" >&2; exit 1; }
  before=$(doc "$id")
  [[ $(jq -r .documentType.id <<<"$before") == "$NEWSLETTER_TYPE" ]] || { echo "Not a newsletter. Nothing published." >&2; exit 1; }
  s=$(summary <<<"$before")
  echo "$s"
  state=$(jq -r .state <<<"$s")
  [[ $state == Published ]] && { echo "Already published with no unpublished changes. Nothing to do." >&2; return; }
  [[ $dry == --dry-run ]] && { echo "Dry run: nothing published." >&2; return; }
  curl -s --fail-with-body -X PUT "$MGMT/document/$id/publish" -H "Authorization: Bearer $(token)" \
    -H "Content-Type: application/json" -d '{"publishSchedules":[{"culture":null}]}' >/dev/null
  state=$(doc "$id" | summary | jq -r .state)
  [[ $state == Published ]] || { echo "Publish sent, but the state reads back as: $state" >&2; exit 1; }
  echo "Published."
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
  linkedin-sweep) call GET "/social-sweep/linkedin" -G --data-urlencode "days=${1:-7}" ;;
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
  newsletters) newsletters "${1:-4}" ;;
  get-newsletter) get_newsletter "${1:?Usage: get-newsletter <id>}" ;;
  set-preheader) set_preheader "$@" ;;
  set-linkedin) set_linkedin "${1:-}" "${2:-}" "${3:-}" ;;
  set-puzzle) set_puzzle "${1:-}" "${2:-}" "${3:-}" ;;
  publish-newsletter) publish_newsletter "${1:-}" "${2:-}" ;;
  *) sed -n '2,41p' "$0"; exit 1 ;;
esac
