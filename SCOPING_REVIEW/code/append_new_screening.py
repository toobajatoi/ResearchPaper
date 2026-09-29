"""Append searches run on 29 September 2026 and the full texts read that day."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
DATE = "2026-09-29"

SEARCH2_ABSTRACT = {
    "42507678": (
        "retain_for_full_text",
        "Abstract: native Japanese raters score LLM workplace replies for linguistic politeness and honorific form, plus socio-cultural values and social action. Full text not yet read.",
    ),
    "42277102": (
        "retain_for_full_text",
        "Abstract: GPT-4o outputs are rated for pragmatic politeness and cultural appropriateness after culturally aware prompts. Full text not yet read.",
    ),
    "41982350": (
        "exclude_abstract",
        "Voice-based GenAI study of learners' intercultural competence and speaking anxiety. Social politeness is coded in learner engagement, not as a cue in machine language.",
    ),
    "39752663": (
        "exclude_abstract",
        "Korean users rate a ChatGPT mental-health chatbot on global empathy, listening, and satisfaction. The abstract does not analyze linguistic features of the replies.",
    ),
    "35071147": (
        "retain_for_full_text",
        "Abstract: experiment manipulates French tu/vous and German du/Sie in a health chatbot and links the address form to human-like evaluation. Full text not yet read.",
    ),
}


def load():
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


def append(rows, source, items):
    start = 1 + max((int(row["record_number"]) for row in rows if row["source"] == source), default=0)
    for offset, item in enumerate(items):
        rows.append(
            {
                "source": source,
                "search_date": DATE,
                "record_number": str(start + offset),
                "authors": item.get("authors", ""),
                "year": item.get("year", ""),
                "title": item["title"],
                "identifier": item["identifier"],
                "stage": item["stage"],
                "decision": item["decision"],
                "reason": item["reason"],
            }
        )


def main():
    fieldnames, rows = load()
    existing_ids = {row["identifier"] for row in rows}

    for row in rows:
        if row["identifier"] == "PMID:37938776":
            row["stage"] = "full_text"
            row["decision"] = "include"
            row["reason"] = (
                "[conceptual] arXiv 2305.16367 is the full text of this Nature paper. "
                "It treats role-play as a way to describe LLM dialogue without literal anthropomorphism, "
                "and it analyzes first-person I/me, claims of self-preservation, and relational language as cues that induce anthropomorphic readings."
            )

    search1 = set(json.loads((ROOT / "data" / "pubmed" / "search1_ids.json").read_text(encoding="utf-8"))["pmids"])
    search2 = json.loads((ROOT / "data" / "pubmed" / "search2_records.json").read_text(encoding="utf-8"))["items"]
    casa = json.loads((ROOT / "data" / "pubmed" / "casa_extra_records.json").read_text(encoding="utf-8"))["items"]

    new_search2 = []
    for item in search2:
        if item["pmid"] in search1:
            continue
        decision, reason = SEARCH2_ABSTRACT.get(
            item["pmid"],
            (
                "exclude_title",
                "Search 2 title does not examine anthropomorphic or human-like communicative cues. The hit is a language, clinical, or benchmark paper.",
            ),
        )
        stage = "title" if decision == "exclude_title" else "abstract"
        new_search2.append(
            {
                "authors": item["authors"],
                "year": item["pubdate"][:4],
                "title": item["title"],
                "identifier": f"PMID:{item['pmid']}",
                "stage": stage,
                "decision": decision,
                "reason": reason,
            }
        )
    append(rows, "PubMed supplementary Search 2", new_search2)

    new_casa = []
    for item in casa:
        if item["pmid"] in search1:
            continue
        new_casa.append(
            {
                "authors": item["authors"],
                "year": item["pubdate"][:4],
                "title": item["title"],
                "identifier": f"PMID:{item['pmid']}",
                "stage": "title",
                "decision": "exclude_title",
                "reason": "CASA extra query. Title is a robot study, a global anthropomorphism scale, or an unrelated CASA acronym. No communicative-cue analysis is indicated.",
            }
        )
    append(rows, "PubMed CASA extra", new_casa)

    seeds = [
        {
            "authors": "DeVrio, Alicia; Cheng, Myra; Egede, Lisa; Olteanu, Alexandra; Blodgett, Su Lin",
            "year": "2025",
            "title": "A Taxonomy of Linguistic Expressions That Contribute to Anthropomorphism of Language Technologies",
            "identifier": "https://doi.org/10.1145/3706598.3714038",
            "stage": "full_text",
            "decision": "include",
            "reason": "[taxonomy] Full text read from arXiv 2502.09870. Builds 19 types of linguistic expressions in language-technology outputs, including first-person reference, emotion, relationships, politeness, and stylistic choice.",
        },
        {
            "authors": "Ibrahim, Lujain; Akbulut, Canfer; Elasmar, Rasmi; Rastogi, Charvi; Kahng, Minsuk; Morris, Meredith Ringel; McKee, Kevin R.; Rieser, Verena; Shanahan, Murray; Weidinger, Laura",
            "year": "2025",
            "title": "Multi-turn evaluation of anthropomorphic behaviours in large language models",
            "identifier": "https://arxiv.org/abs/2502.07077",
            "stage": "full_text",
            "decision": "include",
            "reason": "[measurement] Full text read from arXiv 2502.07077v3. AnthroBench labels 14 behaviours in Gemini, Claude, GPT-4o, and Mistral, including first-person pronouns and relationship-building, and validates them with 1,101 English-proficient participants.",
        },
        {
            "authors": "Cheng, Myra; Blodgett, Su Lin; DeVrio, Alicia; Egede, Lisa; Olteanu, Alexandra",
            "year": "2025",
            "title": "Dehumanizing Machines: Mitigating Anthropomorphic Behaviors in Text Generation Systems",
            "identifier": "https://doi.org/10.18653/v1/2025.acl-long.1259",
            "stage": "full_text",
            "decision": "include",
            "reason": "[taxonomy] Full text read from arXiv 2502.14019 and the ACL Anthology record. Inventory of interventions on anthropomorphic text, including removal of first-person pronouns, empathetic phrasing, and conversational cues.",
        },
    ]
    seeds = [item for item in seeds if item["identifier"] not in existing_ids]
    append(rows, "Citation seed, open full text", seeds)

    acl_items = []
    keep_urls = set()
    for line in (ROOT / "data" / "acl" / "search1_title_keep.txt").read_text(encoding="utf-8").splitlines():
        if " | " not in line:
            continue
        left, url = line.rsplit(" | ", 1)
        keep_urls.add(url)
        if "2025.acl-long.1259" in url:
            continue
        year = left.split(")")[0].replace("(", "").split(".")[-1].strip()
        title = left.split(") ", 1)[1]
        acl_items.append(
            {
                "authors": "",
                "year": year,
                "title": title,
                "identifier": url,
                "stage": "title",
                "decision": "retain_for_abstract",
                "reason": "ACL Anthology title names anthropomorphism or a communicative cue. Abstract not yet read. Not an inclusion.",
            }
        )
    for line in (ROOT / "data" / "acl" / "search1_title_exclude.txt").read_text(encoding="utf-8").splitlines():
        if " | " not in line:
            continue
        left, url = line.rsplit(" | ", 1)
        year = left.split(")")[0].replace("(", "").split(".")[-1].strip()
        title = left.split(") ", 1)[1]
        acl_items.append(
            {
                "authors": "",
                "year": year,
                "title": title,
                "identifier": url,
                "stage": "title",
                "decision": "exclude_title",
                "reason": "ACL title screen. The title does not name anthropomorphic communication or a cue such as empathy, persona, politeness, honorifics, or pronouns.",
            }
        )
    append(rows, "ACL Anthology metadata Search 1", acl_items)

    with SCREEN.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("rows", len(rows), "search2_new", len(new_search2), "casa_new", len(new_casa), "acl", len(acl_items))


if __name__ == "__main__":
    main()
