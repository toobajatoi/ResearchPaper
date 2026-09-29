"""Turn the IEEE website search JSON into a citation table. No full texts."""

import json
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "publisher_search" / "ieee_page1.json"
OUT = ROOT / "data" / "publisher_search" / "ieee_citations.csv"


def authors_of(record):
    names = []
    for author in record.get("authors") or []:
        name = author.get("preferredName") or author.get("normalizedName") or ""
        if name:
            names.append(name)
    return "; ".join(names)


def main():
    data = json.loads(RAW.read_text(encoding="utf-8"))
    records = data.get("records") or []
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["year", "authors", "title", "venue", "doi", "article_number", "ieee_link"],
        )
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    "year": record.get("publicationYear") or "",
                    "authors": authors_of(record),
                    "title": record.get("articleTitle") or record.get("title") or "",
                    "venue": record.get("publicationTitle") or "",
                    "doi": record.get("doi") or "",
                    "article_number": record.get("articleNumber") or "",
                    "ieee_link": record.get("htmlLink") or record.get("documentLink") or "",
                }
            )
    print("records", len(records), "total", data.get("totalRecords"))


if __name__ == "__main__":
    main()
