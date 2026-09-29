"""Record full-text decisions for two open papers whose PDFs were read."""

import csv
from pathlib import Path

SCREEN = Path(__file__).resolve().parents[1] / "data" / "screening.csv"
UPDATES = {
    "PMID:35071147": {
        "stage": "full_text",
        "decision": "include",
        "authors": "Ollier, Joseph; Nißen, Marcia; von Wangenheim, Florian",
        "reason": (
            "Full text read from the Frontiers PDF. A rule-based, text-only healthcare chatbot "
            "(MIA) used a fixed script. The only manipulated cue was the second-person address "
            "pronoun: French tu/vous and German du/Sie. Participants rated how humanlike the "
            "agent felt. Included as perception-plus-cues. The system is not an LLM."
        ),
    },
    "PMID:42507678": {
        "stage": "full_text",
        "decision": "include",
        "authors": "Gao, Zhiwei; Shimizu, Nobuyuki; Fujita, Sumio; Peng, Shaowen; Wakamiya, Shoko; Aramaki, Eiji",
        "reason": (
            "Full text read from the PLOS PDF. Five LLMs answered Japanese workplace prompts. "
            "Native raters scored linguistic form, including politeness and honorifics (keigo), "
            "separately from cultural values and social action. The authors' term is cultural "
            "alignment, not anthropomorphism. Included because honorifics and politeness in "
            "LLM output are treated as social communication."
        ),
    },
}


def main():
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0].keys())
    hit = 0
    for row in rows:
        update = UPDATES.get(row["identifier"])
        if not update:
            continue
        row.update(update)
        hit += 1
    if hit != 2:
        raise SystemExit(f"updated {hit}")
    with SCREEN.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("updated", hit)


if __name__ == "__main__":
    main()
