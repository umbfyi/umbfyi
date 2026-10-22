#!/usr/bin/env python3
"""Group published newsletter items by where they came from and flag the ones no source covers.

Usage: uncovered.py <featured.json> <repo-root> [min-items]

featured.json is `umbfyi.sh featured-all <from>`. Covered means any of:
- a URL or YouTube channel id in src/Umb.Fyi/Hub/Extractors/Implement
- a blog host Umbraco Sphere has posted from since the earliest item in featured.json (Sphere
  aggregates community blogs; its token is read from UMBFYI_SPHERE_TOKEN or appsettings.json)
- dev.to and Medium, which tag feeds cover
YouTube videos are resolved to their channel id by fetching the watch page.
Prints JSON: one entry per uncovered origin with at least min-items items (default 2), most first.
"""
import json, os, re, sys, urllib.request
from collections import defaultdict
from pathlib import Path
import urllib.parse
from urllib.parse import urlparse, parse_qs

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36 Edg/99.0.1150.36"

# Platforms a tag feed already covers, so any author there counts as covered
TAG_FEED_HOSTS = {"dev.to", "medium.com"}
# Hosts that are never a source of their own (social posts, link shorteners, the site itself)
SKIP_HOSTS = {"umb.fyi", "bsky.app", "x.com", "twitter.com", "linkedin.com", "lnkd.in", "umbracocommunity.social",
              "bit.ly", "discord.com", "discord.gg", "forum.umbraco.com", "our.umbraco.com"}

def host_of(url):
    h = urlparse(url).netloc.lower()
    return h[4:] if h.startswith("www.") else h

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", "replace")

def sphere_hosts(since):
    token = os.environ.get("UMBFYI_SPHERE_TOKEN")
    if not token:
        settings = json.load(open(os.path.join(sys.argv[2], "src/Umb.Fyi.Web/appsettings.json"), encoding="utf-8-sig"))
        token = settings["UmbFyi"]["UmbracoSphere"]["Token"]
    hosts, cursor = set(), None
    for _ in range(50):
        url = "https://sphere.umbraco.com/api/v1/blog-posts" + (f"?cursor={urllib.parse.quote(cursor)}" if cursor else "")
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            page = json.load(r)
        posts = page.get("data") or []
        hosts |= {host_of(p["url"]) for p in posts if p.get("url")}
        cursor = (page.get("pagination") or {}).get("nextCursor")
        if not cursor or not (page.get("pagination") or {}).get("hasMore") or not posts or posts[-1].get("publishedAt", "")[:10] < since:
            break
    return hosts

def youtube_channel(url):
    p = urlparse(url)
    vid = parse_qs(p.query).get("v", [None])[0] or (p.path.strip("/").split("/")[-1] if "youtu.be" in p.netloc or "/shorts/" in p.path or "/live/" in p.path else None)
    if not vid:
        return None, None
    try:
        page = fetch(f"https://www.youtube.com/watch?v={vid}")
    except Exception:
        return None, None
    cid = re.search(r'"channelId":"(UC[\w-]{22})"', page)
    name = re.search(r'"ownerChannelName":"([^"]+)"', page)
    return (cid.group(1) if cid else None), (name.group(1) if name else None)

def main():
    items = json.load(open(sys.argv[1]))
    code = "\n".join(p.read_text(encoding="utf-8-sig") for p in Path(sys.argv[2], "src/Umb.Fyi/Hub/Extractors/Implement").glob("*.cs"))
    min_items = int(sys.argv[3]) if len(sys.argv) > 3 else 2

    covered_hosts = {host_of(u) for u in re.findall(r'https?://[^\s"\'{}]+', code)}
    covered_channels = set(re.findall(r'"(UC[\w-]{22})"', code))
    since = min((it.get("newsletterDate") or "9999")[:10] for it in items) if items else "9999"
    covered_hosts |= sphere_hosts(since)

    groups = defaultdict(list)
    for it in items:
        link = it.get("link") or ""
        # Social posts are found by the social sweep, not by sources
        if not link.startswith("http") or it.get("group") == "Social":
            continue
        host = host_of(link)
        if host in SKIP_HOSTS or any(host.endswith("." + s) for s in SKIP_HOSTS):
            continue
        if host in ("youtube.com", "youtu.be", "m.youtube.com"):
            cid, name = youtube_channel(link)
            if cid and cid in covered_channels:
                continue
            key = f"youtube:{cid or 'unknown'}"
            label = f"YouTube: {name or 'unknown channel'}"
        else:
            if host in TAG_FEED_HOSTS or host.endswith(".medium.com") or host in covered_hosts:
                continue
            source = it.get("source") or ""
            key, label = host, (source if source.startswith("http") else f"https://{host}")
        groups[key].append({"title": it.get("title"), "link": link, "group": it.get("group"),
                            "date": (it.get("newsletterDate") or "")[:10], "label": label})

    out = []
    for key, its in groups.items():
        if len(its) < min_items:
            continue
        its.sort(key=lambda x: x["date"], reverse=True)
        out.append({"origin": key, "label": its[0]["label"], "count": len(its),
                    "latest": its[0]["date"], "groups": sorted({i["group"] for i in its if i["group"]}),
                    "examples": [{"title": i["title"], "link": i["link"], "date": i["date"]} for i in its[:3]]})
    out.sort(key=lambda x: (-x["count"], x["origin"]))
    json.dump(out, sys.stdout, indent=1)

if __name__ == "__main__":
    main()
