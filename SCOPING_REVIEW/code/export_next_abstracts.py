"""Write the next unread abstracts to a local file for screening. Does not change the log."""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
ALEX = ROOT / "data" / "openalex" / "search1_narrow_anthropomorph_llm.csv"
OUT = ROOT / "data" / "openalex" / "abstract_batch_next.txt"


def norm_doi(value):
    text = re.sub(r"^https?://(dx\.)?doi\.org/", "", (value or "").strip(), flags=re.I)
    return text.lower()


def main():
    abstracts = {}
    with ALEX.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            abstracts[norm_doi(row.get("doi"))] = row
    lines = []
    n = 0
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["source"] != "OpenAlex narrow title-and-abstract":
                continue
            if "Abstract not yet read" not in row["reason"]:
                continue
            if "abstract field is empty" in row["reason"]:
                continue
            item = abstracts.get(norm_doi(row["identifier"])) or {}
            abstract = (item.get("abstract") or "").replace("\n", " ")
            lines.append(row["identifier"])
            lines.append(row["title"])
            lines.append(abstract)
            lines.append("---")
            n += 1
            if n >= 20:
                break
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", n, OUT)


if __name__ == "__main__":
    main()
