"""Fill findings for included studies from passages already extracted.

Does not invent a result. Does not overwrite a findings cell that already has text.
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "evidence_matrix.csv"
DECISIONS = ROOT / "data" / "fulltext" / "decisions" / "final_decisions.json"

SEED_FINDINGS = {
    "PMID:37938776": "The paper treats role-play as a way to describe LLM dialogue, and it analyzes first-person I/me, claims of self-preservation, and relational language as cues that induce anthropomorphic readings.",
    "PMID:42507678": "Native raters scored Japanese workplace replies from five LLMs on linguistic form, including politeness and honorifics. The authors call this cultural alignment.",
    "https://doi.org/10.1145/3706598.3714038": "The paper builds a taxonomy of 19 types of linguistic expressions in language-technology outputs, including first-person reference, emotion, relationships, politeness, and stylistic choice.",
    "https://arxiv.org/abs/2502.07077": "AnthroBench labels 14 behaviours in Gemini, Claude, GPT-4o, and Mistral. Relationship-building and first-person pronouns were the dominant behaviours in a study of 1,101 English-proficient adults.",
    "https://doi.org/10.18653/v1/2025.acl-long.1259": "The paper inventories interventions on anthropomorphic text, including removal of first-person pronouns, empathetic phrasing, and conversational cues such as follow-up questions.",
}

STATUS = "Finding is taken from the full text already read. The remaining charting cells are not a complete extraction."


def main():
    decisions = {
        item["pmid"]: item
        for item in json.loads(DECISIONS.read_text(encoding="utf-8"))
        if item.get("decision") == "include"
    }
    with MATRIX.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0].keys())
    filled = 0
    for row in rows:
        if row.get("findings"):
            continue
        pmid = row["study_id"].replace("PMID:", "")
        item = decisions.get(pmid)
        if item and item.get("quote"):
            row["findings"] = item["quote"]
            if not row.get("system_or_llm"):
                row["system_or_llm"] = item.get("system") or ""
            if not row.get("language_of_communication"):
                row["language_of_communication"] = item.get("language") or ""
            if not row.get("study_type"):
                row["study_type"] = item.get("tag") or ""
            if not row.get("cue_category_in_source_terms"):
                row["cue_category_in_source_terms"] = item.get("cues") or ""
        elif row["study_id"] in SEED_FINDINGS:
            row["findings"] = SEED_FINDINGS[row["study_id"]]
        else:
            continue
        row["charting_status"] = STATUS
        filled += 1
    with MATRIX.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print("findings filled", filled, "of", len(rows))


if __name__ == "__main__":
    main()
