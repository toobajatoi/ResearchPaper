"""Ask OpenAlex whether the unread PubMed and HMC records have an open PDF."""

import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
OUT = ROOT / "data" / "fulltext" / "unread_oa_lookup.json"


def lookup(doi):
    filt = urllib.parse.quote(f"doi:{doi}", safe="")
    url = f"https://api.openalex.org/works?filter={filt}&select=id,doi,display_name,open_access,primary_location"
    req = urllib.request.Request(url, headers={"User-Agent": "HMC-scoping-review"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.load(resp)
    results = data.get("results") or []
    if not results:
        return {"doi": doi, "found": False}
    work = results[0]
    oa = work.get("open_access") or {}
    location = work.get("primary_location") or {}
    return {
        "doi": doi,
        "found": True,
        "title": work.get("display_name"),
        "is_oa": oa.get("is_oa"),
        "oa_url": oa.get("oa_url"),
        "pdf_url": (location.get("pdf_url") or ""),
    }


def main():
    rows = []
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["decision"] != "retain_for_full_text":
                continue
            if row["source"] not in {
                "PubMed supplementary Search 1",
                "PubMed supplementary Search 2",
                "HMC journal OAI hand search",
            }:
                continue
            rows.append(row)
    found = []
    for row in rows:
        ident = row["identifier"]
        doi = ident.replace("https://doi.org/", "")
        if not doi.startswith("10."):
            found.append({"identifier": ident, "found": False, "reason": "no doi"})
            continue
        try:
            item = lookup(doi)
        except Exception as exc:
            item = {"doi": doi, "error": str(exc)}
        item["source"] = row["source"]
        item["screening_title"] = row["title"]
        found.append(item)
        print(item.get("doi"), item.get("is_oa"), (item.get("oa_url") or "")[:80], flush=True)
        time.sleep(0.2)
    OUT.write_text(json.dumps(found, indent=2), encoding="utf-8")
    print("checked", len(found))


if __name__ == "__main__":
    main()
