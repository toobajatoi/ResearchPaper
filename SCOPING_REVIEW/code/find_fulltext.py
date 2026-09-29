"""Find open full text for PubMed records kept for full-text reading."""

import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
ABSTRACTS = ROOT / "data" / "pubmed" / "retained_abstracts.json"
OUT = ROOT / "data" / "fulltext" / "availability.json"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "HMC-scoping-review"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def main():
    abstracts = {
        item["pmid"]: item
        for item in json.loads(ABSTRACTS.read_text(encoding="utf-8"))["items"]
    }
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            if row["decision"] == "retain_for_full_text"
            and row["source"].startswith("PubMed")
        ]
    found = []
    for row in rows:
        pmid = row["identifier"].replace("PMID:", "")
        meta = abstracts.get(pmid, {})
        query = urllib.parse.urlencode(
            {
                "query": f"EXT_ID:{pmid} AND SRC:MED",
                "resultType": "core",
                "format": "json",
                "pageSize": "1",
            }
        )
        url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + query
        try:
            data = get(url)
            result = (data.get("resultList") or {}).get("result") or []
            hit = result[0] if result else {}
        except Exception as exc:
            hit = {"error": type(exc).__name__}
        found.append(
            {
                "pmid": pmid,
                "doi": meta.get("doi") or hit.get("doi") or "",
                "pmcid": hit.get("pmcid") or "",
                "is_oa": hit.get("isOpenAccess") or "",
                "title": row["title"],
            }
        )
        print(pmid, found[-1]["pmcid"], found[-1]["is_oa"], flush=True)
        time.sleep(0.2)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(found, indent=2), encoding="utf-8")
    oa = sum(1 for item in found if item["pmcid"])
    print("pmcid", oa, "of", len(found))


if __name__ == "__main__":
    main()
