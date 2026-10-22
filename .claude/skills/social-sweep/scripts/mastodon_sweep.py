"""Recent Umbraco posts on Mastodon, for the newsletter's social sweep.

Reads two public timelines on umbracocommunity.social (no login needed): the server's own local
timeline (Umbraco community members) and the #umbraco hashtag timeline (which includes posts from
other servers that the community server knows about). Prints one JSON array, newest first, in the
same shape as the Bluesky sweep endpoint.

Usage: python3 -I mastodon_sweep.py <since-iso-datetime> [server]
"""

import html
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

MAX_PAGES = 10


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "UMB.FYI social sweep"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def timeline(base, since):
    """Page back through a timeline until posts are older than `since`."""
    max_id = None
    for _ in range(MAX_PAGES):
        url = base + ("&" if "?" in base else "?") + "limit=40" + (f"&max_id={max_id}" if max_id else "")
        page = fetch(url)
        if not page:
            return
        for status in page:
            yield status
        max_id = page[-1]["id"]
        if parse_time(page[-1]["created_at"]) < since:
            return


def parse_time(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def to_text(content):
    content = re.sub(r"<br\s*/?>|</p>", "\n", content)
    return html.unescape(re.sub(r"<[^>]+>", "", content)).strip()


def links_of(status):
    # Links in the post, minus mentions and hashtags, plus the link preview card.
    links = []
    for attrs in re.findall(r"<a ([^>]*)>", status["content"]):
        href = re.search(r'href="([^"]+)"', attrs)
        if href and "mention" not in attrs and "hashtag" not in attrs:
            links.append(href.group(1))
    if status.get("card") and status["card"].get("url"):
        links.append(status["card"]["url"])
    return list(dict.fromkeys(html.unescape(x) for x in links))


def main(since_arg, server="umbracocommunity.social"):
    since = parse_time(since_arg)
    if since.tzinfo is None:
        since = since.replace(tzinfo=timezone.utc)

    seen = {}
    sources = [
        f"https://{server}/api/v1/timelines/public?local=true",
        f"https://{server}/api/v1/timelines/tag/umbraco",
    ]
    for source in sources:
        for status in timeline(source, since):
            if parse_time(status["created_at"]) < since or status["uri"] in seen:
                continue
            seen[status["uri"]] = {
                "url": status["url"] or status["uri"],
                "author": status["account"]["acct"],
                "authorName": status["account"].get("display_name"),
                "text": to_text(status["content"]),
                "createdAt": status["created_at"],
                "isReply": status.get("in_reply_to_id") is not None,
                "isRepost": status.get("reblog") is not None,
                "links": links_of(status),
                "likes": status.get("favourites_count", 0),
                "reposts": status.get("reblogs_count", 0),
                "replies": status.get("replies_count", 0),
            }

    posts = sorted(seen.values(), key=lambda x: x["createdAt"], reverse=True)
    json.dump(posts, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(*sys.argv[1:])
