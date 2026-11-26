"""Build the course product-photo catalog from Wikimedia Commons (free licences only).

Usage (from the repo root): python -X utf8 22-catalog-search/materials/src/fetch_catalog.py
Writes 22-catalog-search/materials/data/catalog/*.jpg (320 px thumbnails) and catalog.csv with the
licence, author and source page that the Commons API reports for each file. One file at a time,
with a pause, and a descriptive User-Agent (Commons rate-limits bulk downloads).
"""
import csv, importlib.util, re, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("fc", ROOT / "scripts" / "fetch-commons.py")
fc = importlib.util.module_from_spec(spec); spec.loader.exec_module(fc)

_call = fc.call
def call_retry(params, tries=6):
    for k in range(tries):
        try:
            return _call(params)
        except Exception as e:
            wait = 30 * (2 ** k)
            print(f"API error {e}; waiting {wait}s", flush=True); time.sleep(wait)
    raise SystemExit("Commons API keeps refusing; try again later")
fc.call = call_retry

OUT = ROOT / "22-catalog-search" / "materials" / "data" / "catalog"
CATS = {  # 中文類別 → Commons 搜尋字
    "耳機": "headphones product photo",
    "行動電源": "power bank",
    "智慧手錶": "smartwatch",
    "掃地機器人": "robotic vacuum cleaner",
    "電熱水壺": "electric kettle",
    "筆電": "laptop computer",
    "背包": "backpack",
    "馬克杯": "coffee mug",
}
PER_CAT = 5
rows = []
for i, (zh, q) in enumerate(CATS.items()):
    time.sleep(5)
    data = fc.call({"action": "query", "list": "search", "srsearch": f"{q} filetype:bitmap",
                    "srnamespace": 6, "srlimit": 30})
    titles = [r["title"] for r in data["query"]["search"]]
    got = 0
    for it in fc.info(titles, 320):
        if got >= PER_CAT:
            break
        if not fc.FREE.match(it["license"] or "") or it["mime"] not in ("image/jpeg", "image/png"):
            continue
        if not it["w"] or it["w"] < 300:
            continue
        name = f"c{i}_{got}.jpg"
        req = urllib.request.Request(it["thumb"], headers={"User-Agent": fc.UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                (OUT / name).write_bytes(r.read())
        except Exception as e:
            print("skip", it["title"], e); time.sleep(5); continue
        rows.append({"file": name, "category": zh, "title": it["title"], "license": it["license"],
                     "author": it["artist"], "source": it["page"]})
        got += 1
        print(zh, name, it["license"], it["title"][:60], flush=True)
        time.sleep(4)
    if got < PER_CAT:
        print(f"WARNING: only {got} for {zh}")
with open(OUT.parent / "catalog.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows), "images")
