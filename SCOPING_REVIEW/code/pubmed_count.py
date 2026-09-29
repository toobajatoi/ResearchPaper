"""PubMed supplementary Search 1 count and id list. Not a primary database."""

import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "pubmed"
OUT.mkdir(parents=True, exist_ok=True)

TERM = (
    '(anthropomorph*[tiab] OR "human-like"[tiab] OR "human likeness"[tiab] '
    'OR "social presence"[tiab] OR "social cue*"[tiab] '
    'OR "computers are social actors"[tiab] OR "human-machine communication"[tiab]) '
    'AND ("large language model*"[tiab] OR "language model*"[tiab] OR chatbot*[tiab] '
    'OR "generative AI"[tiab] OR "generative artificial intelligence"[tiab] '
    'OR "conversational agent*"[tiab] OR "conversational AI"[tiab]) '
    'AND ("2020/01/01"[dp] : "2026/09/29"[dp])'
)


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "HMC-scoping-review"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.load(resp)


def main():
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": TERM,
        "retmode": "json",
        "retmax": "0",
        "datetype": "pdat",
        "mindate": "2020/01/01",
        "maxdate": "2026/09/29",
    }
    url = base + "?" + urllib.parse.urlencode(params)
    data = get(url)
    count = int(data["esearchresult"]["count"])
    print("pubmed count", count)
    ids = []
    retmax = 200
    for start in range(0, count, retmax):
        params["retstart"] = str(start)
        params["retmax"] = str(retmax)
        page = get(base + "?" + urllib.parse.urlencode(params))
        ids.extend(page["esearchresult"]["idlist"])
    (OUT / "search1_ids.json").write_text(
        json.dumps(
            {
                "search_date": "2026-09-29",
                "term": TERM,
                "count": count,
                "ids_saved": len(ids),
                "pmids": ids,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("ids saved", len(ids))


if __name__ == "__main__":
    main()
