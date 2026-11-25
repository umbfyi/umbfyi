#!/usr/bin/env python3
"""Save a trimmed record of one week's items: what the workflow found, what Claude proposed, what went out.

Usage:
  python3 -I save_history.py <issue YYYY-MM-DD> <items-raw.json> <items.json> <newsletter.json> [--seen <record>] > history/<issue>.json

  items-raw.json   the workflow's results, unedited (newsletter-items step 4)
  items.json       Claude's review: kept items with fixes, drops left out, unsure ones marked "unsure": "<reason>"
  newsletter.json  `umbfyi.sh get-newsletter <id>` once the items are in and any fixes are done

  --seen <record>  an earlier record for this issue (the morning top-up passes Tuesday's): items already in it
                   are left out, so the new record covers only the top-up's own items

This repo is public, so the record holds only link, title, group, tags, and which fields changed.
No summaries, no drop reasons, no workflow logs.
"""
import json
import re
import sys
from datetime import datetime, timezone

FIELDS = {  # workflow / items.json field -> newsletter block field
    "title": "itemTitle",
    "summary": "itemDescription",
    "source": "itemSource",
    "emoji": "itemEmoji",
    "consumptionTimeMinutes": "itemConsumptionTimeMinutes",
    "contentTags": "itemTags",
}


def load_items(path):
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, dict):
        for key in ("mediaItems", "items"):
            if isinstance(data.get(key), list):
                return data[key]
        raise SystemExit(f"{path}: no item list found")
    return data


def key(link):
    return (link or "").strip().rstrip("/").lower()


def group(name):
    return re.sub(r"[^a-z0-9]", "", (name or "").lower())


def norm(field, value):
    if field == "contentTags":
        return sorted(t.lower() for t in (value or []))
    if field == "consumptionTimeMinutes":
        return int(value or 0)
    return (value or "").strip()


def changed(a, b, b_is_block=False):
    out = [f for f, block in FIELDS.items()
           if norm(f, a.get(f)) != norm(f, b.get(block if b_is_block else f))]
    if group(a.get("category")) != group(b.get("group" if b_is_block else "category")):
        out.append("group")
    return out


def main():
    args = sys.argv[1:]
    seen = set()
    if "--seen" in args:
        i = args.index("--seen")
        with open(args[i + 1]) as f:
            seen = {key(r.get("link")) for r in json.load(f).get("items", [])}
        del args[i:i + 2]
    if len(args) != 4:
        sys.exit(__doc__)
    issue, raw_path, review_path, nl_path = args
    raw = {key(i.get("link")): i for i in load_items(raw_path)}
    review = {key(i.get("link")): i for i in load_items(review_path)}
    with open(nl_path) as f:
        nl = json.load(f)

    final, current = {}, None
    for b in nl.get("blocks", []):
        if b.get("type") == "group":
            current = b["values"].get("groupAlias")
        elif b.get("type") == "item":
            v = dict(b["values"], group=current)
            if key(v.get("itemLink")) not in seen:
                final[key(v.get("itemLink"))] = v

    rows = []
    for k in list(raw) + [k for k in review if k not in raw] + [k for k in final if k not in raw and k not in review]:
        w, p, s = raw.get(k), review.get(k), final.get(k)
        origin = "workflow" if w else "added in review" if p else "added after"
        if p is None:
            proposed = "drop" if w else None
        elif p.get("unsure"):
            proposed = "unsure"
        elif w and changed(w, p):
            proposed = "changed"
        else:
            proposed = "keep"
        first = p or w or {}
        rows.append({
            "link": (first.get("link") or (s or {}).get("itemLink")),
            "title": (s or {}).get("itemTitle") or first.get("title"),
            "origin": origin,
            "workflowGroup": w.get("category") if w else None,
            "workflowTags": w.get("contentTags") if w else None,
            "proposed": proposed,
            "claudeChanged": changed(w, p) if w and p else [],
            "final": "in" if s else "out",
            "finalGroup": s.get("group") if s else None,
            "finalTags": s.get("itemTags") if s else None,
            "mattChanged": changed(p, s, True) if p and s else [],
        })

    def agreed(r):
        if r["proposed"] in ("keep", "changed"):
            return r["final"] == "in" and not r["mattChanged"]
        if r["proposed"] == "drop":
            return r["final"] == "out"
        return False  # unsure, or added after review

    summary = {
        "workflow": len(raw),
        "proposed": {d: sum(r["proposed"] == d for r in rows) for d in ("keep", "changed", "drop", "unsure")},
        "inIssue": sum(r["final"] == "in" for r in rows),
        "mattFlippedOrEdited": sum(not agreed(r) and r["proposed"] != "unsure" for r in rows),
    }
    saved_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    json.dump({"issue": issue, "savedAt": saved_at, "summary": summary, "items": rows},
              sys.stdout, indent=1, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
