"""Replace availability DOIs and PMCIDs with PubMed esummary article ids.

The abstract fetch stored the last ArticleId in each PubmedArticle, which can
be a cited reference. Europe PMC lookup by PMID is kept when PubMed has no PMCID.
"""

import csv
import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
AVAIL = ROOT / "data" / "fulltext" / "availability.json"


def esummary(pmids):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?" + urllib.parse.urlencode(
        {"db": "pubmed", "id": ",".join(pmids), "retmode": "json"}
    )
    req = urllib.request.Request(url, headers={"User-Agent": "HMC-scoping-review"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def main():
    old = {row["pmid"]: row for row in json.loads(AVAIL.read_text(encoding="utf-8"))}
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            if row["decision"] == "retain_for_full_text" and row["source"].startswith("PubMed")
        ]
    pmids = [row["identifier"].replace("PMID:", "") for row in rows]
    data = esummary(pmids)
    fixed = []
    doi_changes = 0
    pmc_added = 0
    for row in rows:
        pmid = row["identifier"].replace("PMID:", "")
        item = data["result"][pmid]
        doi = ""
        pmcid = ""
        for aid in item.get("articleids") or []:
            if aid.get("idtype") == "doi":
                doi = aid.get("value") or ""
            if aid.get("idtype") == "pmc":
                pmcid = aid.get("value") or ""
        previous = old.get(pmid, {})
        if previous.get("doi") and previous.get("doi") != doi:
            doi_changes += 1
        if pmcid and not previous.get("pmcid"):
            pmc_added += 1
        fixed.append(
            {
                "pmid": pmid,
                "doi": doi,
                "pmcid": pmcid or previous.get("pmcid") or "",
                "is_oa": previous.get("is_oa") or ("Y" if pmcid else ""),
                "title": row["title"],
                "pmcid_source": "pubmed_esummary" if pmcid else "europepmc_pmid",
            }
        )
    AVAIL.write_text(json.dumps(fixed, indent=2), encoding="utf-8")
    print("records", len(fixed), "doi_changes", doi_changes, "pmc_added", pmc_added)
    print("with_pmcid", sum(1 for row in fixed if row["pmcid"]))


if __name__ == "__main__":
    main()
