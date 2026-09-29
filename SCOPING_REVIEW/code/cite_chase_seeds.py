"""Save works cited by, and works citing, the four seed papers. Does not screen them."""

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "citation_chase"
OUT.mkdir(parents=True, exist_ok=True)

SEEDS = {
    "devrio_2025": "10.1145/3706598.3714038",
    "cheng_2025": "10.18653/v1/2025.acl-long.1259",
    "shanahan_2023": "10.1038/s41586-023-06647-8",
    "ibrahim_2026": "10.48550/arxiv.2502.07077",
}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "HMC-scoping-review"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.load(resp)


def work_by_doi(doi):
    filt = urllib.parse.quote(f"doi:{doi}", safe="")
    data = get(
        "https://api.openalex.org/works?filter="
        + filt
        + "&select=id,doi,display_name,publication_year,cited_by_count,referenced_works"
    )
    results = data.get("results") or []
    return results[0] if results else None


def titles_for(openalex_ids):
    found = []
    for start in range(0, len(openalex_ids), 50):
        chunk = openalex_ids[start : start + 50]
        filt = "openalex_id:" + "|".join(item.rsplit("/", 1)[-1] for item in chunk)
        params = urllib.parse.urlencode(
            {"filter": filt, "per-page": "50", "select": "id,doi,display_name,publication_year"}
        )
        data = get("https://api.openalex.org/works?" + params)
        for work in data.get("results") or []:
            found.append(
                {
                    "openalex_id": work.get("id"),
                    "doi": work.get("doi"),
                    "year": work.get("publication_year"),
                    "title": work.get("display_name"),
                }
            )
        time.sleep(0.3)
    return found


def citing(openalex_id, cited_by_count):
    short = openalex_id.rsplit("/", 1)[-1]
    rows = []
    cursor = "*"
    while cursor and len(rows) < cited_by_count and len(rows) < 200:
        params = urllib.parse.urlencode(
            {
                "filter": f"cites:{short},from_publication_date:2020-01-01",
                "per-page": "50",
                "cursor": cursor,
                "select": "id,doi,display_name,publication_year",
            }
        )
        data = get("https://api.openalex.org/works?" + params)
        batch = data.get("results") or []
        if not batch:
            break
        for work in batch:
            rows.append(
                {
                    "openalex_id": work.get("id"),
                    "doi": work.get("doi"),
                    "year": work.get("publication_year"),
                    "title": work.get("display_name"),
                }
            )
        cursor = (data.get("meta") or {}).get("next_cursor")
        time.sleep(0.3)
    return rows


def main():
    report = {}
    for name, doi in SEEDS.items():
        work = work_by_doi(doi)
        if not work:
            report[name] = {"doi": doi, "found": False}
            print(name, "not found", flush=True)
            continue
        referenced = titles_for(work.get("referenced_works") or [])
        cites = citing(work["id"], work.get("cited_by_count") or 0)
        report[name] = {
            "doi": doi,
            "found": True,
            "openalex_id": work["id"],
            "title": work.get("display_name"),
            "cited_by_count": work.get("cited_by_count"),
            "referenced_saved": len(referenced),
            "citing_saved": len(cites),
            "citing_capped": len(cites) >= 200,
            "referenced_works": referenced,
            "citing_works": cites,
        }
        print(name, "refs", len(referenced), "citing", len(cites), "count", work.get("cited_by_count"), flush=True)
        time.sleep(0.4)
    (OUT / "seed_citation_chase.json").write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
