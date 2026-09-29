"""Check whether HMC articles are in Europe PMC."""

import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"


def doi_of(identifier):
    for part in identifier.split("|"):
        part = part.strip()
        if part.startswith("info:doi/"):
            return part.replace("info:doi/", "")
    return ""


def main():
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            if row["source"].startswith("HMC") and row["decision"] == "retain_for_full_text"
        ]
    results = []
    for row in rows:
        doi = doi_of(row["identifier"])
        query = urllib.parse.urlencode(
            {"query": f'DOI:"{doi}"', "resultType": "core", "format": "json", "pageSize": "1"}
        )
        url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + query
        req = urllib.request.Request(url, headers={"User-Agent": "HMC-scoping-review"})
        try:
            data = json.load(urllib.request.urlopen(req, timeout=60))
            hit = ((data.get("resultList") or {}).get("result") or [{}])[0]
            results.append(
                {
                    "n": row["record_number"],
                    "doi": doi,
                    "title": row["title"][:80],
                    "pmcid": hit.get("pmcid"),
                    "oa": hit.get("isOpenAccess"),
                    "in_epmc": bool(hit.get("id")),
                }
            )
        except Exception as exc:
            results.append({"n": row["record_number"], "doi": doi, "error": type(exc).__name__})
        print(results[-1], flush=True)
        time.sleep(0.2)
    out = ROOT / "data" / "fulltext" / "hmc_epmc.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
