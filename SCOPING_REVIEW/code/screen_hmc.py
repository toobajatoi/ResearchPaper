"""Title and abstract decisions for the Human-Machine Communication hand search.

Decisions were made from the OAI titles and abstracts harvested on 2026-09-29.
A retain decision means the full text still has to be read. It is not inclusion.
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "hmc" / "hmc_oai_records.json"
OUT = ROOT / "data" / "screening.csv"

# Record numbers are the harvest order in hmc_titles.csv.
RETAIN = {
    33: "Chatbots as support providers; abstract discusses communicative features of bots. Full text needed to see whether cues are analyzed.",
    48: "Abstract states that empathy in human-machine communication is achieved through linguistic behavior.",
    54: "Abstract examines communicative anthropomorphization of socialbots and how users assign humanlike features in conversation.",
    62: "Abstract proposes Artificial Sociality for communicative AI, including large language models such as ChatGPT.",
    66: "Compares a chatbot and a human advisor on responsive conversational features.",
    76: "Studies a voice assistant's politeness and machine-likeness. Full text needed to see whether the cues are linguistic.",
    91: "Essay generated with ChatGPT. Full text needed to see whether it conceptualizes anthropomorphic language.",
    97: "Title concerns an anthropomorphic media representative and social responses.",
    102: "Examines agency negotiation in human-generative-AI collaboration. Full text needed to see whether linguistic cues are analyzed.",
    118: "Conversation analysis of naturally occurring student-chatbot interactions.",
    123: "Experiment on interpersonal closeness produced by large language model text.",
    124: "Perceived gender of AI conversational assistants. Full text needed to see whether gender is treated as a communicative cue.",
    125: "Longitudinal study of perceiving communicative AI as a tool or a social actor.",
    126: "Interviews on communication and relationship development with the chatbot Replika.",
    127: "Develops a measure of human-likeness perceptions of text-based conversational agents.",
}

VOLUMES = {9, 23, 32, 43, 45, 58, 64, 69, 89, 110, 113, 129, 131}
EDITORIALS = {8, 22, 30, 42, 44, 51, 59, 88, 99, 108, 114}

ROBOT = {
    1, 3, 4, 6, 16, 24, 29, 36, 52, 57, 71, 82, 121, 122, 128,
}
VOICE = {11, 27, 38, 41, 49, 63, 65}


def reason_for(number, title):
    if number in RETAIN:
        return "retain_for_full_text", RETAIN[number]
    if number in VOLUMES or "complete volume" in title.lower():
        return "exclude_title_abstract", "Complete-volume file. The articles are screened individually."
    if number in EDITORIALS:
        return "exclude_title_abstract", "Editorial or issue introduction without an analysis of anthropomorphic cues in generated language."
    if number in ROBOT:
        return "exclude_title_abstract", "Embodied or social robot study. Textual large-language-model communication is not the focus."
    if number in VOICE:
        return "exclude_title_abstract", "Voice-based assistant or smart speaker. The abstract does not analyze textual communication cues."
    return (
        "exclude_title_abstract",
        "Does not examine anthropomorphic or human-like communication cues in large language model or generative-language output.",
    )


def main():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    rows = []
    for number, item in enumerate(data["items"], start=1):
        title = item.get("title") or ""
        decision, reason = reason_for(number, title)
        rows.append(
            {
                "source": "HMC journal OAI hand search",
                "search_date": "2026-09-29",
                "record_number": number,
                "authors": item.get("creators") or "",
                "year": (item.get("date") or "")[:4],
                "title": title,
                "identifier": item.get("identifier") or "",
                "stage": "title_abstract",
                "decision": decision,
                "reason": reason,
            }
        )
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    retained = sum(1 for row in rows if row["decision"] == "retain_for_full_text")
    excluded = len(rows) - retained
    print(f"hmc screened {len(rows)}; retained for full text {retained}; excluded {excluded}")


if __name__ == "__main__":
    main()
