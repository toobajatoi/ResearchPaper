"""Test abstract rules against OpenAlex decisions already made by reading.

Does not change the screening log.
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


def norm_doi(value):
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", (value or "").strip(), flags=re.I).lower()


def predict(text):
    if CUE.search(text):
        return "keep"
    if SURVEY.search(text) or OFF.search(text):
        return "exclude"
    return "unread"


def main():
    abstracts = {}
    with ALEX.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            abstracts[norm_doi(row.get("doi"))] = (row.get("abstract") or "")
    hand = []
    unread_pred = {"keep": 0, "exclude": 0, "unread": 0}
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if not row["source"].startswith("OpenAlex"):
                continue
            abstract = abstracts.get(norm_doi(row["identifier"]), "")
            text = row["title"] + " " + abstract
            pred = predict(text)
            if "Abstract not yet read" in row["reason"]:
                unread_pred[pred] += 1
                continue
            if row["decision"] in {"exclude_abstract", "exclude_title", "retain_for_full_text"}:
                hand.append((pred, row["decision"], row["title"][:70]))
    print("unread buckets", unread_pred)
    print("hand", len(hand))
    wrong = [item for item in hand if (item[0] == "exclude" and item[1] == "retain_for_full_text") or (item[0] == "keep" and item[1].startswith("exclude"))]
    print("conflicts", len(wrong))
    for item in wrong:
        print(" | ".join(item))


if __name__ == "__main__":
    main()
