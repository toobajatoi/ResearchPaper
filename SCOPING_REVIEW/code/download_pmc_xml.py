"""Download Europe PMC full text for records that have a PMCID."""

import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AVAIL = ROOT / "data" / "fulltext" / "availability.json"
OUT = ROOT / "data" / "fulltext" / "pmc"
OUT.mkdir(parents=True, exist_ok=True)


def fetch(pmcid):
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
    req = urllib.request.Request(url, headers={"User-Agent": "HMC-scoping-review"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def main():
    rows = json.loads(AVAIL.read_text(encoding="utf-8"))
    saved = 0
    for row in rows:
        pmcid = row.get("pmcid") or ""
        if not pmcid:
            continue
        dest = OUT / f"{pmcid}.xml"
        if dest.exists() and dest.stat().st_size > 1000:
            saved += 1
            continue
        try:
            data = fetch(pmcid)
            dest.write_bytes(data)
            saved += 1
            print(pmcid, len(data), flush=True)
        except Exception as exc:
            print("FAIL", pmcid, type(exc).__name__, exc, flush=True)
        time.sleep(0.25)
    print("saved", saved)


if __name__ == "__main__":
    main()
