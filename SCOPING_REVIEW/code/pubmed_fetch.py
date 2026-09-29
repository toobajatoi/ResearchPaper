"""Fetch PubMed titles and abstracts for the 650 ids saved on 2026-09-29."""

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "pubmed" / "search1_ids.json"
OUT = ROOT / "data" / "pubmed" / "search1_summaries.json"


def post(ids):
    data = urllib.parse.urlencode(
        {"db": "pubmed", "id": ",".join(ids), "retmode": "json"}
    ).encode()
    req = urllib.request.Request(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
        data=data,
        headers={"User-Agent": "HMC-scoping-review"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.load(resp)


def main():
    pmids = json.loads(SRC.read_text(encoding="utf-8"))["pmids"]
    records = []
    for start in range(0, len(pmids), 100):
        batch = pmids[start : start + 100]
        data = post(batch)
        result = data["result"]
        for pmid in batch:
            item = result.get(pmid) or {}
            records.append(
                {
                    "pmid": pmid,
                    "title": item.get("title") or "",
                    "authors": "; ".join(
                        author.get("name") or "" for author in item.get("authors") or []
                    ),
                    "source": item.get("source") or "",
                    "pubdate": item.get("pubdate") or "",
                    "doi": item.get("elocationid") or "",
                }
            )
        print(f"fetched {len(records)}", flush=True)
        time.sleep(0.4)
    OUT.write_text(
        json.dumps({"search_date": "2026-09-29", "records": len(records), "items": records}, ensure_ascii=False),
        encoding="utf-8",
    )
    print("saved", len(records))


if __name__ == "__main__":
    main()
