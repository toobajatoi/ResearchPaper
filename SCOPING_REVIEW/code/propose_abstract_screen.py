"""Propose abstract decisions for records still marked unread.

Does not change the screening log. Writes proposals only.
A proposal of retain_for_full_text is not an inclusion.
"""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
ALEX = ROOT / "data" / "openalex" / "search1_narrow_anthropomorph_llm.csv"
OUT = ROOT / "data" / "openalex" / "proposed_abstract_screen.csv"
RETAIN_TXT = ROOT / "data" / "openalex" / "abstract_batch_proposed_retains.txt"

CUE = re.compile(
    r"first[- ]person|pronouns?|politeness|honorifics?|self-disclosure|"
    r"linguistic cue|communication cue|anthropomorphic cue|"
    r"empathetic (language|expression|phrasing|response)|"
    r"backchannels?|speech acts?|terms of address|"
    r"human-like language|humanlike language|self-referen|"
    r"conversational (style|cue)|dialogue act|wording|"
    r"generated (text|language|utterance)|model output|"
    r"persona|role[- ]play",
    re.I,
)
SURVEY = re.compile(
    r"perceived anthropomorphism|PLS-SEM|structural equation|technology acceptance|"
    r"\bUTAUT\b|continuance intention|adoption intention|usage intention|"
    r"use intention|behavioural intention|behavioral intention|"
    r"questionnaire|Likert|survey of|online survey|participants rated",
    re.I,
)
OFF = re.compile(
    r"radiology|histopath|drug[- ]target|protein structure|dexterous grasp|"
    r"text-to-image|cross-modal|traffic signal|vision-language|"
    r"molecular|genome|clinical imaging|autonomous driving",
    re.I,
)
ROBOT = re.compile(
    r"humanoid|embodied robot|social robot|NAO robot|robot'?s (body|face|appearance)|"
    r"physical robot",
    re.I,
)
DETECTION = re.compile(
    r"human-written|machine-generated text detection|detect(ing)? (AI|machine)-generated|"
    r"authorship attribution",
    re.I,
)
LLM = re.compile(
    r"large language model|\bLLMs?\b|ChatGPT|GPT-4|generative AI|generative artificial|"
    r"language model|chatbot",
    re.I,
)


def norm_doi(value):
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", (value or "").strip(), flags=re.I).lower()


def decide(title, abstract):
    text = f"{title} {abstract}".strip()
    has_abstract = bool(abstract.strip())
    cue = bool(CUE.search(text))
    survey = bool(SURVEY.search(text))
    off = bool(OFF.search(text))
    robot = bool(ROBOT.search(text))
    detection = bool(DETECTION.search(text))
    llm = bool(LLM.search(text))

    if not has_abstract:
        if cue and llm:
            return (
                "retain_for_full_text",
                "No abstract in the index record. The title suggests anthropomorphic language in an LLM. Full text needed. Not an inclusion.",
            )
        return (
            "exclude_abstract",
            "No abstract in the index record, and the title does not show analysis of anthropomorphic cues in LLM-generated text.",
        )
    if off and not cue:
        return (
            "exclude_abstract",
            "Anthropomorphism is incidental to a non-linguistic topic, and the abstract does not name a communication cue.",
        )
    if robot and not cue:
        return (
            "exclude_abstract",
            "Embodied or social robot. The abstract does not analyze linguistic cues in LLM text.",
        )
    if detection and not re.search(r"anthropomorph", text, re.I):
        return (
            "exclude_abstract",
            "Human-versus-machine detection. Anthropomorphic cues are not the object of analysis.",
        )
    if survey and not cue:
        return (
            "exclude_abstract",
            "User survey of perceived anthropomorphism, acceptance, or intention. The abstract does not analyze linguistic cues.",
        )
    if cue and (llm or re.search(r"anthropomorph", text, re.I)):
        return (
            "retain_for_full_text",
            "Abstract names a communication cue or persona in relation to a language model or anthropomorphism. Full text needed. Not an inclusion.",
        )
    if re.search(r"anthropomorph", text, re.I) and llm:
        return (
            "review",
            "Anthropomorphism and a language model are both named, but no specific communication cue is named. Needs a reading.",
        )
    return (
        "exclude_abstract",
        "The abstract does not analyze or conceptualize anthropomorphic communication cues in LLM-generated text.",
    )


def main():
    abstracts = {}
    with ALEX.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            abstracts[norm_doi(row.get("doi"))] = row.get("abstract") or ""
    proposals = []
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if "Abstract not yet read" not in (row.get("reason") or ""):
                continue
            if row["source"].startswith("OpenAlex"):
                abstract = abstracts.get(norm_doi(row["identifier"]), "")
            else:
                abstract = ""
            decision, reason = decide(row["title"], abstract)
            proposals.append(
                {
                    "identifier": row["identifier"],
                    "source": row["source"],
                    "title": row["title"],
                    "decision": decision,
                    "reason": reason,
                    "abstract": abstract.replace("\n", " "),
                }
            )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["identifier", "source", "title", "decision", "reason"],
        )
        writer.writeheader()
        writer.writerows(
            {k: item[k] for k in writer.fieldnames} for item in proposals
        )
    lines = []
    for item in proposals:
        if item["decision"] in {"retain_for_full_text", "review"}:
            lines.append(item["decision"])
            lines.append(item["identifier"])
            lines.append(item["title"])
            lines.append(item["abstract"][:1800])
            lines.append("---")
    RETAIN_TXT.write_text("\n".join(lines), encoding="utf-8")
    from collections import Counter

    print(Counter(item["decision"] for item in proposals))
    print("wrote", OUT)
    print("retain file lines", len(lines))


if __name__ == "__main__":
    main()
