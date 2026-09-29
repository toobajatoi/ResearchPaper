"""Write cue-flagged unread OpenAlex abstracts for reading. Does not decide."""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
ALEX = ROOT / "data" / "openalex" / "search1_narrow_anthropomorph_llm.csv"
OUT = ROOT / "data" / "openalex" / "abstract_batch_cues.txt"
CUE = re.compile(
    r"first[- ]person|pronouns?|politeness|honorifics?|self-disclosure|"
    r"\bpersona\b|role[- ]play|linguistic cue|communication cue|anthropomorphic cue|"
    r"empathetic (language|expression|phrasing)|backchannels?|speech acts?|"
    r"terms of address|sociolect|grammatical (gender|person)",
    re.I,
)


def norm_doi(value):
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", (value or "").strip(), flags=re.I).lower()


def main():
    abstracts = {}
    with ALEX.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            abstracts[norm_doi(row.get("doi"))] = row.get("abstract") or ""
    lines = []
    n = 0
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if not row["source"].startswith("OpenAlex"):
                continue
            if "Abstract not yet read" not in row["reason"]:
                continue
            abstract = abstracts.get(norm_doi(row["identifier"]), "")
            if not CUE.search(row["title"] + " " + abstract):
                continue
            if n >= 25:
                break
            lines.append("---")
            lines.append(row["identifier"])
            lines.append(row["title"])
            lines.append(abstract[:800].replace("\n", " "))
            n += 1
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", n)


if __name__ == "__main__":
    main()
