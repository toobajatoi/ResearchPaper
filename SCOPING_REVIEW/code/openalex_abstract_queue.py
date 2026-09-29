"""Print the next unread OpenAlex titles so abstract screening can proceed in batches.

Does not change the screening log.
"""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
ALEX = ROOT / "data" / "openalex" / "search1_narrow_anthropomorph_llm.csv"


def norm_doi(value):
    text = re.sub(r"^https?://(dx\.)?doi\.org/", "", (value or "").strip(), flags=re.I)
    return text.lower()


def main():
    abstracts = {}
    with ALEX.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            abstracts[norm_doi(row.get("doi"))] = row
    unread = []
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["source"] != "OpenAlex narrow title-and-abstract":
                continue
            if "Abstract not yet read" not in row["reason"]:
                continue
            if "abstract field is empty" in row["reason"]:
                continue
            unread.append(row)
    print("unread", len(unread))
    shown = 0
    for row in unread:
        if shown >= 40:
            break
        item = abstracts.get(norm_doi(row["identifier"]))
        title = row["title"]
        abstract = (item or {}).get("abstract") or ""
        print("---")
        print(row["identifier"])
        print(title)
        print(abstract[:900].replace("\n", " "))
        shown += 1


if __name__ == "__main__":
    main()
