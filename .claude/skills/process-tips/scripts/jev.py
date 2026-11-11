#!/usr/bin/env python3
"""Ask Jev (TypeSafe's fast yes/no model) one question about every item in some JSON files.

Usage: jev.py "<statement>" <items.json> [<items.json> ...] [--min 0.35] [--field jev]

Each file is a JSON array of objects (social posts, tips, newsletter items...).
Jev reads each item's text fields (author, title, text, summary, description,
links, whichever it has) and gives the probability (0 to 1) that the statement
is true of it. Prints all items as one JSON array, highest first, with:

  --field   where the probability goes (default `jev`)
  --min     drop items below this (default: keep everything)

Each item also gets `sourceFile`, the file it came from.

Write the statement as something true of the items you want, e.g.
"This post shares Umbraco news worth adding to a weekly newsletter."

Needs TYPESAFE_API_KEY, from the environment or ~/.umbfyi-tips.env.
Exits 1 if Jev can't be reached, so callers can fall back to reading everything.
"""
import argparse
import concurrent.futures
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

ENDPOINT = "https://api.typesafe.ai/v1/systemone"
TEXT_FIELDS = ["authorName", "author", "title", "text", "summary", "description"]
MAX_STATE = 60000  # Well inside Jev's 32k tokens per question


def api_key():
    key = os.environ.get("TYPESAFE_API_KEY")
    env = pathlib.Path.home() / ".umbfyi-tips.env"
    if not key and env.exists():
        for line in env.read_text().splitlines():
            line = line.strip().removeprefix("export ").strip()
            if line.startswith("TYPESAFE_API_KEY="):
                key = line.split("=", 1)[1].strip().strip("'\"")
    if not key:
        sys.exit("TYPESAFE_API_KEY is not set (environment or ~/.umbfyi-tips.env)")
    return key


def state(item):
    parts = [f"{f}: {item[f]}" for f in TEXT_FIELDS if isinstance(item.get(f), str) and item[f].strip()]
    if item.get("links"):
        parts.append("links: " + " ".join(item["links"]))
    return "\n\n".join(parts)[:MAX_STATE]


def ask(key, statement, item):
    body = json.dumps({
        "state": state(item),
        "model": "jev-latest",
        "questions": {"q": {"type": "noul", "instructions": statement}},
    }).encode()
    req = urllib.request.Request(ENDPOINT, body, {"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    for attempt in range(3):
        try:
            return round(json.load(urllib.request.urlopen(req, timeout=60))["answers"]["q"]["noul"], 2)
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 2:  # Retry only rate limits
                raise


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("statement")
    parser.add_argument("files", nargs="+")
    parser.add_argument("--min", type=float, default=None)
    parser.add_argument("--field", default="jev")
    args = parser.parse_args()

    key = api_key()
    items = []
    for path in args.files:
        for item in json.load(open(path)):
            item["sourceFile"] = os.path.basename(path)
            items.append(item)

    try:
        with concurrent.futures.ThreadPoolExecutor(8) as pool:
            scores = list(pool.map(lambda i: ask(key, args.statement, i), items))
    except Exception as e:
        sys.exit(f"Jev request failed: {e}")

    for item, score in zip(items, scores):
        item[args.field] = score
    items.sort(key=lambda i: i[args.field], reverse=True)
    if args.min is not None:
        items = [i for i in items if i[args.field] >= args.min]
    json.dump(items, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
