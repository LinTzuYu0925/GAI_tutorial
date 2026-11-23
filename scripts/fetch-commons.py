"""Search Wikimedia Commons and download licensed photos for slides.

Usage:
  python -X utf8 scripts/fetch-commons.py search "printed circuit board macro" [n]
  python -X utf8 scripts/fetch-commons.py get "File:Name.jpg" <deck>/public/out.jpg [width]

`search` lists bitmap files with licence and size. `get` downloads a thumbnail
(default 800 px wide) and prints a ready-made row for research/sources.md with the
licence, author and source page taken from the Commons API (extmetadata), so the
licence on the slide is the one Commons states, not one written from memory.
Only free licences are accepted by `get` (CC0, public domain, CC BY, CC BY-SA).
"""
import json
import re
import sys
import urllib.parse
import urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = "course-slide-builder/1.0 (educational slides; python urllib)"
FREE = re.compile(r"^(cc0|public domain|pd|cc by(-sa)? [0-9.]+)", re.I)


def call(params):
    params = {**params, "format": "json"}
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def strip(html):
    return re.sub(r"<[^>]+>", "", html or "").strip()


def info(titles, width=800):
    data = call({"action": "query", "titles": "|".join(titles), "prop": "imageinfo",
                 "iiprop": "url|size|extmetadata|mime", "iiurlwidth": width})
    out = []
    for p in data["query"]["pages"].values():
        if "imageinfo" not in p:
            continue
        ii = p["imageinfo"][0]
        md = ii.get("extmetadata", {})
        out.append({
            "title": p["title"], "mime": ii.get("mime"), "w": ii.get("width"), "h": ii.get("height"),
            "thumb": ii.get("thumburl"), "page": ii.get("descriptionurl"),
            "license": strip(md.get("LicenseShortName", {}).get("value")),
            "artist": strip(md.get("Artist", {}).get("value"))[:80],
            "desc": strip(md.get("ImageDescription", {}).get("value"))[:120],
        })
    return out


def search(q, n=12):
    data = call({"action": "query", "list": "search", "srsearch": f"{q} filetype:bitmap",
                 "srnamespace": 6, "srlimit": n})
    titles = [r["title"] for r in data["query"]["search"]]
    for it in info(titles) if titles else []:
        print(f"{it['title']}\n   {it['license']} | {it['w']}x{it['h']} | {it['artist']} | {it['desc']}")


def get(title, dest, width=800):
    it = info([title], int(width))
    if not it:
        sys.exit(f"not found: {title}")
    it = it[0]
    if not FREE.match(it["license"] or ""):
        sys.exit(f"refused: licence '{it['license']}' is not on the free list")
    req = urllib.request.Request(it["thumb"], headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
        f.write(r.read())
    print(f"saved {dest}")
    print(f"| Sx | {it['desc'] or it['title']} | {it['artist']}，{it['license']}，經 Wikimedia Commons：{it['page']} | 已確認（Commons API 授權欄位） | YYYY-MM-DD |")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "search":
        search(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 12)
    elif cmd == "get":
        get(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else 800)
