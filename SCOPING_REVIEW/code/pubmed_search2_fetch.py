"""Save PubMed ids and titles for Search 2 and the CASA extra query."""

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "pubmed"


def post(url, fields):
    data = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(url, data=data, headers={"User-Agent": "HMC-scoping-review"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.load(resp)


def ids_for(term):
    payload = post(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
        {"db": "pubmed", "term": term, "retmode": "json", "retmax": "200"},
    )
    result = payload["esearchresult"]
    return int(result["count"]), result["idlist"]


def summaries(pmids):
    payload = post(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
        {"db": "pubmed", "id": ",".join(pmids), "retmode": "json"},
    )
    result = payload["result"]
    rows = []
    for pmid in pmids:
        item = result.get(pmid) or {}
        doi = ""
        for aid in item.get("articleids") or []:
            if aid.get("idtype") == "doi":
                doi = aid.get("value") or ""
        rows.append(
            {
                "pmid": pmid,
                "title": item.get("title") or "",
                "authors": "; ".join(a.get("name") or "" for a in item.get("authors") or []),
                "source": item.get("source") or "",
                "pubdate": item.get("pubdate") or "",
                "doi": doi,
            }
        )
    return rows


def main():
    search1 = set(json.loads((OUT / "search1_ids.json").read_text(encoding="utf-8"))["pmids"])
    for name in ("search2", "casa_extra"):
        meta = json.loads((OUT / f"{name}_count.json").read_text(encoding="utf-8"))
        count, pmids = ids_for(meta["term"])
        if count != len(pmids):
            raise SystemExit(f"{name} count {count} ids {len(pmids)}")
        rows = summaries(pmids)
        overlap = [row["pmid"] for row in rows if row["pmid"] in search1]
        record = {
            "search_date": "2026-09-29",
            "name": name,
            "count": count,
            "overlap_with_search1": overlap,
            "items": rows,
        }
        (OUT / f"{name}_records.json").write_text(
            json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        lines = []
        for index, row in enumerate(rows, start=1):
            mark = " [also Search 1]" if row["pmid"] in search1 else ""
            lines.append(f"{index}. PMID:{row['pmid']} ({row['pubdate']}) {row['title']}{mark}")
        (OUT / f"{name}_titles.txt").write_text("\n".join(lines), encoding="utf-8")
        print(name, count, "overlap", len(overlap), flush=True)
        time.sleep(0.4)


if __name__ == "__main__":
    main()
