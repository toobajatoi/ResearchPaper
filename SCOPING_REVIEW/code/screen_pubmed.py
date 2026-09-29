"""Title screening of the PubMed supplementary search.

Every title in data/pubmed/titles.txt was read. Records in RETAIN are kept
for abstract reading. They are not included studies.
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data" / "pubmed" / "search1_summaries.json").read_text(encoding="utf-8"))
OUT = ROOT / "data" / "screening.csv"

# 1-based indexes matching titles.txt
RETAIN = {
    3: "Conversational AI framed as a social actor. Abstract needed to see whether communicative cues are reviewed.",
    10: "Frames large language models as tools, models, or partners. Abstract needed for the partner conceptualization.",
    16: "Names conversational attributes of generative AI as part of trust. Abstract needed.",
    19: "Studies chatbot anthropomorphism. Abstract needed to see whether the cues are linguistic or visual.",
    22: "Reframes conversational AI as tool or companion.",
    23: "Conceptual paper on the psychology of anthropomorphism in human-AI relationships.",
    28: "Models chatbot anthropomorphism and consumer decisions. Abstract needed for the operationalization.",
    29: "Review of the antecedents and consequences of AI anthropomorphism.",
    33: "Older adults' use of social chatbots, including anthropomorphism and authenticity.",
    37: "Social presence in a model of relational intelligence in AI chatbots.",
    41: "Perceived anthropomorphism. Abstract needed to see whether communicative features are specified.",
    42: "Anthropomorphism and trust in large language models across age groups.",
    46: "Scoping review of human-like conversational agents as social partners.",
    47: "Government chatbot empathy and continued use.",
    52: "Review of human-likeness and social roles in persuasive large language models.",
    54: "Kinship construction in human-AI communication among Chinese users.",
    58: "Chatbot design characteristics. Abstract needed to see whether they include linguistic cues.",
    77: "Perceived anthropomorphism and adoption of healthcare chatbots.",
    78: "Sycophancy and anthropomorphic projection in AI mental-health support.",
    79: "AI chatbot characteristics and consumer behavior. Abstract needed.",
    85: "Social presence of a dementia-prevention chatbot.",
    101: "Conceptual analysis of human-like epistemic trust in conversational AI.",
    105: "Anthropomorphic appearance and empathic responses of medical conversational agents. Abstract needed to separate visual and linguistic cues.",
    107: "Responsiveness, warmth, and anthropomorphism in conversational AI for learning.",
    134: "Acceptance of social chatbots and the role of anthropomorphism.",
    139: "Friendlike conversation with AI companions.",
    147: "Anthropomorphism and social presence in a live-streaming setting. Abstract needed to see whether language is analyzed.",
    151: "Human-like cues and trust in customer-service chatbots.",
    156: "Message humanness as a predictor that an AI is perceived as human.",
    164: "Whether therapy chatbots empathize, and emotional complexity.",
    174: "Mixed-methods study of generative-AI anthropomorphism.",
    183: "Generative-AI anthropomorphism in an exercise-motivation model. Abstract needed for the operationalization.",
    189: "Embodied conversational agent appearance and message emotion. Abstract needed to see whether message wording is analyzed.",
    192: "Compares GPT-generated and clinician wording, including human empathy and human wording.",
    202: "Describes a human-like AI counseling service. Abstract needed.",
    211: "Individual differences in anthropomorphism and connection to AI companions.",
    217: "Human-like features of generative AI and usage intention.",
    218: "Review of anthropomorphic chatbots and mental health.",
    245: "Anthropomorphic tendencies as a moderator of attachment to conversational AI.",
    248: "Whether artificial agents are perceived similarly to humans.",
    251: "Patient views of empathy, compassion, and self-disclosure in medical large language models.",
    266: "Evaluates AI-generated outputs for an illusion of empathy.",
    268: "Conceptual analysis of human-like trust in conversational AI.",
    281: "Empathic technology in patient-AI dialogue.",
    284: "AI chatbots with social cues in a depression intervention.",
    308: "Mental-state attributions and trust in large language models.",
    313: "Benefits and dangers of anthropomorphic conversational agents.",
    320: "Youth slang in an educational chatbot.",
    322: "Dynamics of human-AI interaction from robots to chatbots. Abstract needed.",
    335: "Cultural variation in attitudes toward social chatbots.",
    338: "Anthropomorphism in large language models.",
    346: "Chatbot response strategies and emoji use.",
    354: "Conversational AI and theory-of-mind and autonomy biases.",
    373: "Systematic review of large language models and empathy.",
    376: "Foundations of trust in an AI chatbot. Abstract needed.",
    378: "Conceptual paper on deanthropomorphising NLP.",
    385: "Human-chatbot relations and significant otherness.",
    404: "Compares a text chatbot with a human-AI video bot.",
    420: "Taxonomy of social communication, affiliation, and presence features.",
    431: "Large language models and attributes considered uniquely human.",
    436: "Gender in human-machine communication.",
    442: "Scoping review of conversational agents as humanlike virtual health carers.",
    447: "Humanization of large language models in conversational AI for depression.",
    448: "ChatGPT from human-computer interaction and psychology perspectives.",
    467: "Compares an anthropomorphic digital human with a text-based chatbot.",
    473: "Folk attributions of consciousness to large language models.",
    476: "Human-like traits of ChatGPT and information sharing.",
    478: "Behavioural cues that elicit human-like response patterns from chatbots.",
    482: "Mind perception and social support of chatbots.",
    491: "Scoping review of human-like conversations with conversational agents.",
    507: "GPT-3 communication with diverse social groups.",
    527: "Scoping review of embodied conversational agents using motivational interviewing.",
    535: "Argument about the Computers Are Social Actors paradigm.",
    537: "Role play with large language models.",
    568: "Anthropomorphic cues, perceived anthropomorphism, and social presence of healthcare conversational agents.",
    572: "Voice assistant empathy and engagement. Abstract needed to see whether the cues are linguistic.",
    601: "Anthropomorphic chatbots and counseling satisfaction.",
    618: "Chatbots and social presence in online learning.",
    619: "Friendly language used by product-recommendation chatbots.",
    620: "Development of an anthropomorphic conversational agent.",
    622: "Systematic review of language use in conversational-agent health communication.",
    632: "Anthropomorphic interactions with personal voice assistants.",
    636: "Regular chatbot use and human-technology relationship.",
    644: "Personalization of conversational-agent interaction styles.",
    645: "Compares a monologue-style embodied agent with textual guidance.",
    191: "Social presence of embodied conversational agents. Abstract needed to see whether language is the object of analysis.",
}

SPECIFIC_EXCLUDE = {
    4: "Anthropomorphic image type. The title concerns visual appearance, not linguistic cues.",
    81: "Human-like virtual profiles on Instagram. The title concerns visual profiles and audience metrics.",
    119: "Avatar design of a virtual doctor. The title concerns visual human-likeness, animal-likeness, and object-likeness.",
    223: "Uncanny valley of embodied conversational agents. The title concerns attractiveness and visual anthropomorphism.",
    225: "Agent entrance styles and social presence in augmented reality. The title concerns spatial entrance, not language.",
    231: "Empathetic humanoid robot. The title concerns gestures and embodiment, not large-language-model text.",
    629: "Antibody humanization in bioinformatics, not communication.",
}


def reason_for(index, title):
    if index in RETAIN:
        return "retain_for_abstract", RETAIN[index]
    if index in SPECIFIC_EXCLUDE:
        return "exclude_title", SPECIFIC_EXCLUDE[index]
    lowered = title.lower()
    if any(word in lowered for word in ("robot", "exoskeleton", "humanoid", "radiotherapy", "radiology")):
        return (
            "exclude_title",
            "Robot, vision, or clinical-system paper. The title does not analyze anthropomorphic communication cues in generated language.",
        )
    if any(word in lowered for word in ("antibody humanization", "humeness evaluation", "bioph")):
        return "exclude_title", "Antibody humanization, not communication."
    return (
        "exclude_title",
        "Title does not examine anthropomorphic or human-like communication cues in machine-generated language.",
    )


def main():
    items = DATA["items"]
    new_rows = []
    for index, item in enumerate(items, start=1):
        title = (item.get("title") or "").replace("\n", " ")
        decision, reason = reason_for(index, title)
        new_rows.append(
            {
                "source": "PubMed supplementary Search 1",
                "search_date": "2026-09-29",
                "record_number": index,
                "authors": item.get("authors") or "",
                "year": (item.get("pubdate") or "")[:4],
                "title": title,
                "identifier": f"PMID:{item.get('pmid','')}",
                "stage": "title",
                "decision": decision,
                "reason": reason,
            }
        )
    with OUT.open(encoding="utf-8", newline="") as handle:
        existing = list(csv.DictReader(handle))
    # Drop any earlier PubMed rows if the script is rerun.
    existing = [row for row in existing if row["source"] != "PubMed supplementary Search 1"]
    fieldnames = list(existing[0].keys()) if existing else list(new_rows[0].keys())
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)
        writer.writerows(new_rows)
    retained = sum(1 for row in new_rows if row["decision"] == "retain_for_abstract")
    print(f"pubmed screened {len(new_rows)}; retained {retained}; excluded {len(new_rows) - retained}")


if __name__ == "__main__":
    main()
