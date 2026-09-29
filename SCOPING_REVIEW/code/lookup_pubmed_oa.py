"""Check OpenAlex for an open PDF of the unread PubMed full-text queue."""

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "fulltext" / "pubmed_unread_oa.json"
PMIDS = [
    "42648233",
    "42463863",
    "42269974",
    "41548427",
    "40810905",
    "40694494",
    "40562106",
    "40286349",
    "38428201",
    "35976080",
    "42507678",
    "42277102",
    "35071147",
]


def main():
    rows = []
    for pmid in PMIDS:
        filt = urllib.parse.quote(f"pmid:{pmid}", safe="")
        url = (
            "https://api.openalex.org/works?filter="
            + filt
            + "&select=id,doi,display_name,open_access,ids"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "HMC-scoping-review"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.load(resp)
        results = data.get("results") or []
        if not results:
            rows.append({"pmid": pmid, "found": False})
        else:
            work = results[0]
            oa = work.get("open_access") or {}
            rows.append(
                {
                    "pmid": pmid,
                    "found": True,
                    "doi": work.get("doi"),
                    "title": work.get("display_name"),
                    "is_oa": oa.get("is_oa"),
                    "oa_url": oa.get("oa_url"),
                    "pmcid": (work.get("ids") or {}).get("pmcid"),
                }
            )
        print(rows[-1]["pmid"], rows[-1].get("is_oa"), rows[-1].get("pmcid"), flush=True)
        time.sleep(0.25)
    OUT.write_text(json.dumps(rows, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
