"""Record whether each full-text-queue record has an open copy.

Does not change screening decisions.
"""

import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
OUT = ROOT / "data" / "fulltext" / "queue_oa_lookup.json"


def batched(items, size):
    for start in range(0, len(items), size):
        yield items[start : start + size]


def lookup_dois(dois):
    filt = urllib.parse.quote("doi:" + "|".join(dois), safe="")
    url = (
        "https://api.openalex.org/works?filter="
        + filt
        + "&select=id,doi,display_name,open_access,primary_location&per-page=50"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "HMC-scoping-review (mailto:research@local)"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.load(resp)
    found = {}
    for work in data.get("results") or []:
        doi = (work.get("doi") or "").lower().replace("https://doi.org/", "")
        oa = work.get("open_access") or {}
        location = work.get("primary_location") or {}
        found[doi] = {
            "is_oa": oa.get("is_oa"),
            "oa_url": oa.get("oa_url") or "",
            "pdf_url": location.get("pdf_url") or "",
            "landing": (location.get("landing_page_url") or ""),
        }
    return found


def doi_of(identifier):
    text = identifier.strip()
    lower = text.lower()
    if "10." not in lower:
        return ""
    if lower.startswith("pmid"):
        return ""
    text = text.replace("https://doi.org/", "").replace("http://doi.org/", "")
    if text.lower().startswith("doi:"):
        text = text[4:]
    return text.split("?")[0].rstrip("/").lower()


def main():
    rows = []
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["decision"] == "retain_for_full_text":
                rows.append(row)
    dois = []
    for row in rows:
        doi = doi_of(row["identifier"])
        if doi.startswith("10."):
            dois.append(doi)
    found = {}
    for batch in batched(dois, 25):
        try:
            found.update(lookup_dois(batch))
            print("batch", len(batch), "found", len(found), flush=True)
        except Exception as exc:
            print("batch error", exc, flush=True)
        time.sleep(0.3)
    payload = []
    for row in rows:
        doi = doi_of(row["identifier"])
        item = {
            "identifier": row["identifier"],
            "title": row["title"],
            "source": row["source"],
            "doi": doi,
        }
        item.update(found.get(doi, {}))
        payload.append(item)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    oa = sum(1 for item in payload if item.get("is_oa"))
    print("queue", len(payload), "with doi", len(dois), "oa", oa)


if __name__ == "__main__":
    main()
