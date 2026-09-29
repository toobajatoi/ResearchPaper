"""Exclude unread OpenAlex abstracts that match rules already checked by hand.

A record is excluded only when the abstract does not name a linguistic cue and it
matches a survey-rating pattern or a non-linguistic topic. Records that name a cue
are left unread. This does not mark any study included.
"""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
ALEX = ROOT / "data" / "openalex" / "search1_narrow_anthropomorph_llm.csv"

CUE = re.compile(
    r"first[- ]person|pronouns?|politeness|honorifics?|self-disclosure|"
    r"\bpersona\b|role[- ]play|linguistic cue|communication cue|anthropomorphic cue|"
    r"empathetic (language|expression|phrasing)|backchannels?|speech acts?|"
    r"terms of address|sociolect|grammatical (gender|person)",
    re.I,
)
SURVEY = re.compile(
    r"perceived anthropomorphism|PLS-SEM|structural equation|technology acceptance|"
    r"\bUTAUT\b|continuance intention|adoption intention|usage intention|"
    r"use intention|behavioural intention|behavioral intention",
    re.I,
)
OFF = re.compile(
    r"radiology|histopath|drug[- ]target|protein structure|dexterous grasp|"
    r"text-to-image|cross-modal|traffic signal|vision-language",
    re.I,
)
REASON = (
    "Abstract screened with the rules checked against the 160 abstracts already read. "
    "Anthropomorphism is a survey rating or a non-linguistic topic, and the abstract does not name a linguistic cue."
)


def norm_doi(value):
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", (value or "").strip(), flags=re.I).lower()


def main():
    abstracts = {}
    with ALEX.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            abstracts[norm_doi(row.get("doi"))] = row.get("abstract") or ""
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0].keys())
    hit = 0
    for row in rows:
        if not row["source"].startswith("OpenAlex"):
            continue
        if "Abstract not yet read" not in row["reason"]:
            continue
        text = row["title"] + " " + abstracts.get(norm_doi(row["identifier"]), "")
        if CUE.search(text):
            continue
        if not (SURVEY.search(text) or OFF.search(text)):
            continue
        row["stage"] = "abstract"
        row["decision"] = "exclude_abstract"
        row["reason"] = REASON
        hit += 1
    with SCREEN.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print("excluded", hit)


if __name__ == "__main__":
    main()
