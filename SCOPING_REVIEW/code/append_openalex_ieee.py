"""Add the narrowed OpenAlex export and the IEEE website hits to the screening log.

OpenAlex rows are not screened. IEEE rows are title-screened only.
Neither set is marked included.
"""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
OPENALEX = ROOT / "data" / "openalex" / "search1_narrow_anthropomorph_llm.csv"
IEEE = ROOT / "data" / "publisher_search" / "ieee_citations.csv"

IEEE_RETAIN = {
    "11665619",
    "10714528",
    "10973919",
    "11184734",
    "10613707",
    "11574165",
    "11666502",
    "11579311",
    "11227929",
    "11015514",
    "11676983",
    "10973942",
}


def norm_doi(value):
    text = (value or "").strip().lower()
    text = text.replace("https://doi.org/", "").replace("http://doi.org/", "")
    return text


def main():
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0].keys())
    known = set()
    for row in rows:
        doi = norm_doi(row["identifier"])
        if doi.startswith("10."):
            known.add(doi)
        if "info:doi/" in row["identifier"]:
            known.add(norm_doi(row["identifier"].split("info:doi/")[-1].split("|")[0].strip()))
    added_oa = skipped_oa = 0
    with OPENALEX.open(encoding="utf-8", newline="") as handle:
        for index, work in enumerate(csv.DictReader(handle), 1):
            doi = norm_doi(work["doi"])
            if doi and doi in known:
                skipped_oa += 1
                continue
            identifier = work["doi"] or work["openalex_id"]
            if doi:
                known.add(doi)
            rows.append(
                {
                    "source": "OpenAlex narrow title-and-abstract",
                    "search_date": "2026-09-29",
                    "record_number": str(index),
                    "authors": work["authors"],
                    "year": work["year"],
                    "title": work["title"],
                    "identifier": identifier,
                    "stage": "retrieved",
                    "decision": "retain_for_abstract",
                    "reason": "Narrow OpenAlex record. Abstract not yet read. Not an inclusion.",
                }
            )
            added_oa += 1
    added_ieee = retain_ieee = exclude_ieee = 0
    with IEEE.open(encoding="utf-8", newline="") as handle:
        for index, work in enumerate(csv.DictReader(handle), 1):
            doi = norm_doi(work["doi"])
            if doi and doi in known:
                continue
            keep = work["article_number"] in IEEE_RETAIN
            if doi:
                known.add(doi)
            rows.append(
                {
                    "source": "IEEE Xplore website",
                    "search_date": "2026-09-29",
                    "record_number": str(index),
                    "authors": work["authors"],
                    "year": work["year"],
                    "title": work["title"],
                    "identifier": ("https://doi.org/" + doi) if doi else work["ieee_link"],
                    "stage": "title",
                    "decision": "retain_for_abstract" if keep else "exclude_title",
                    "reason": (
                        "IEEE title suggests anthropomorphic or empathetic communication. Abstract not yet read. Not an inclusion."
                        if keep
                        else "IEEE title does not describe anthropomorphic communication cues in machine-generated text. Not an inclusion."
                    ),
                }
            )
            added_ieee += 1
            if keep:
                retain_ieee += 1
            else:
                exclude_ieee += 1
    with SCREEN.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(
        "openalex added",
        added_oa,
        "skipped",
        skipped_oa,
        "ieee added",
        added_ieee,
        "ieee retain",
        retain_ieee,
        "ieee exclude",
        exclude_ieee,
        "rows",
        len(rows),
    )


if __name__ == "__main__":
    main()
