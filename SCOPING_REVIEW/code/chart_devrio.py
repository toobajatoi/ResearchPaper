"""Chart DeVrio et al. 2025 from the CHI full text. Does not copy the paper."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "evidence_matrix.csv"
STUDY = "https://doi.org/10.1145/3706598.3714038"

FIELDS = {
    "venue": "CHI '25: Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems",
    "research_objective": "How text produced by language technologies contributes to anthropomorphism of those technologies.",
    "system_or_llm": "Language technologies, mostly LLM-based systems (including LaMDA, GPT-4, ChatGPT, Bing Chat, Gemini, Bard, Claude, Pi, and Replika). The case set also includes earlier systems such as ELIZA, PARRY, and Sophia.",
    "language_of_communication": "English",
    "cultural_context": "Cases and annotations are in English. The authors describe a standard American English norm among the annotators.",
    "study_type": "taxonomy from an exploratory case study and a synthesis of prior literature",
    "dataset_or_sample": "50 public sources published 2017-2024 (90 percent from 2022-2024); 395 conversational turns; 3,954 annotations.",
    "interaction_type": "One conversational turn: a user input paired with the verbatim system output.",
    "anthropomorphism_definition": "The attribution of human-like qualities to inanimate objects or entities.",
    "cue_category_in_source_terms": "Five lenses: internal states; social positioning; materiality; autonomy; communication skills. Nineteen expression types: intelligence; self-assessment; self-awareness and identity; self-comparison; personality; perspectives; relationships; reciprocation; pretense and authenticity; emotions; intention; morality; conventionality; (dis)agreeableness; vulnerability; right to privacy; anticipation, recall, and change; embodiment; deliberate language manipulation.",
    "operationalization": "Bottom-up thematic analysis of in-the-wild English outputs, stopped at saturation, checked against expressions already named in prior work.",
    "measurement_method": "Open coding. At least two researchers annotated each output. This is not a user-perception experiment.",
    "findings": "The authors identify 19 types of textual expressions that can contribute to anthropomorphism, read through five lenses. First-person pronouns and self-naming are expressions of self-awareness and identity. Politeness and markers such as please and thanks are expressions of agreeableness. Empathy and emojis are expressions of emotion. The paper does not test which expressions produce stronger anthropomorphism or harm. It presents the taxonomy as a vocabulary for later measurement and design decisions.",
    "limitations_stated_by_authors": "Public, often high-profile cases may miss expressions. Hype around generative AI can change how far people anthropomorphize outputs. Most cases come from LLM dialogue. Annotations and cases are in English, by a team used to standard American English. The authors state that anthropomorphism is likely to differ across languages and cultures.",
    "relevance_to_cross_lingual_research": "The source states that its cases and annotations are English and that anthropomorphism is likely to occur differently across languages and cultures. It calls for the same kind of work on non-English language technologies.",
    "charting_status": "Charted from the CHI full text on 29 September 2026. Example quotations were not copied into this matrix.",
}


def main():
    with MATRIX.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0].keys())
    hit = 0
    for row in rows:
        if row.get("study_id") != STUDY and row.get("doi") != "10.1145/3706598.3714038":
            continue
        row.update(FIELDS)
        hit += 1
    if hit != 1:
        raise SystemExit("expected one DeVrio row, found %s" % hit)
    with MATRIX.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print("charted", hit)


if __name__ == "__main__":
    main()
