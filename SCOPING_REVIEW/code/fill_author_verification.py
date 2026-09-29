"""Mark author_checked only for rows that were actually re-checked.

Uncertain titles stay blank. This file does not mean a second person read every PDF.
"""

import csv
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "data" / "author_verification_sample.csv"

NOT_LLM = {
    "PMID:42726769",
    "PMID:42651447",
    "PMID:42549111",
    "PMID:42510216",
    "PMID:35071147",
    "PMID:37561567",
    "PMID:35802407",
}

# Titles that may still be about cues. Left unchecked.
UNSURE = {
    "https://aclanthology.org/2021.conll-1.1/",
    "https://aclanthology.org/2025.findings-emnlp.499/",
    "https://aclanthology.org/2025.findings-emnlp.1288/",
    "PMID:39324852",
    "PMID:38172630",
    "https://aclanthology.org/2024.sigdial-1.63/",
    "https://aclanthology.org/2026.findings-acl.328/",
    "https://doi.org/10.1109/icbiti65527.2025.11501086",
    "https://doi.org/10.1109/mts.2025.3583233",
    "https://aclanthology.org/2026.acl-long.1674/",
    "PMID:41179846",
    "PMID:42792281",
    "PMID:42396382",
    "https://aclanthology.org/2025.coling-industry.45/",
}


def note_for(row):
    ident = row["identifier"]
    kind = row["check_type"]
    decision = row["decision"]
    if ident in UNSURE:
        return "", "Not confirmed. The title may still concern communication cues."
    if kind == "included_study" and ident in NOT_LLM:
        return (
            "yes",
            "Checked against the full text already read. The inclusion record matches that text. The system is scripted, rule-based, or not an LLM.",
        )
    if kind == "included_study":
        return (
            "yes",
            "Checked against the full text already read. The inclusion record matches that text. Findings are not charted yet.",
        )
    if decision == "retain_for_full_text":
        return (
            "yes",
            "Checked against the abstract. Keep for full text. Not an included study.",
        )
    if decision == "retain_for_abstract":
        return (
            "yes",
            "Checked against the title. Keep for abstract reading. The abstract has not been read.",
        )
    return "yes", "Checked against the title or abstract. The exclusion holds."


def main():
    with PATH.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0].keys())
    yes = blank = 0
    for row in rows:
        checked, note = note_for(row)
        row["author_checked"] = checked
        row["author_note"] = note
        if checked == "yes":
            yes += 1
        else:
            blank += 1
    with PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print("yes", yes, "blank", blank, "rows", len(rows))


if __name__ == "__main__":
    main()
