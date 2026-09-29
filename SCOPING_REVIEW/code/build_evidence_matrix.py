"""Start the evidence matrix from full-text decisions already recorded.

Cells that were not extracted stay empty. This is not a finished chart.
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / "data" / "fulltext" / "decisions" / "final_decisions.json"
SCREEN = ROOT / "data" / "screening.csv"
OUT = ROOT / "data" / "evidence_matrix.csv"

COLUMNS = [
    "study_id",
    "citation",
    "year",
    "venue",
    "doi",
    "url",
    "source",
    "research_objective",
    "system_or_llm",
    "language_of_communication",
    "cultural_context",
    "study_type",
    "dataset_or_sample",
    "interaction_type",
    "anthropomorphism_definition",
    "cue_category_in_source_terms",
    "operationalization",
    "measurement_method",
    "inclusion_reason",
    "findings",
    "limitations_stated_by_authors",
    "relevance_to_cross_lingual_research",
    "charting_status",
]


def blank():
    return {column: "" for column in COLUMNS}


def main():
    decisions = json.loads(DECISIONS.read_text(encoding="utf-8"))
    included = [item for item in decisions if item.get("decision") == "include"]
    rows = []
    for item in included:
        row = blank()
        row["study_id"] = "PMID:" + item["pmid"]
        row["citation"] = item.get("title") or ""
        row["system_or_llm"] = item.get("system") or ""
        row["language_of_communication"] = item.get("language") or ""
        row["study_type"] = item.get("tag") or ""
        row["cue_category_in_source_terms"] = item.get("cues") or ""
        row["inclusion_reason"] = item.get("reason") or ""
        row["findings"] = ""
        row["source"] = "PubMed supplementary Search 1"
        row["charting_status"] = "partial: taken from the full-text decision note, not a complete extraction"
        rows.append(row)
    charted = {item["pmid"] for item in included}
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        for item in csv.DictReader(handle):
            if item["decision"] != "include":
                continue
            if item["source"] == "PubMed supplementary Search 1":
                pmid = item["identifier"].replace("PMID:", "")
                if pmid in charted:
                    continue
            row = blank()
            row["study_id"] = item["identifier"]
            row["citation"] = item["authors"] + " (" + item["year"] + "). " + item["title"]
            row["year"] = item["year"]
            row["doi"] = item["identifier"]
            row["source"] = item["source"]
            row["inclusion_reason"] = item["reason"]
            row["findings"] = ""
            row["charting_status"] = "partial: open full text was read; extraction fields are not complete"
            rows.append(row)
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print("matrix rows", len(rows))


if __name__ == "__main__":
    main()
