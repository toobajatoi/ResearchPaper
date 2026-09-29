"""Enter the author-supplied Shanahan charting row after a check against arXiv v1."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "evidence_matrix.csv"
STUDY = "PMID:37938776"

FIELDS = {
    "citation": "Shanahan, M., McDonell, K., & Reynolds, L. (2023). Role play with large language models. Nature, 623, 493-498. https://doi.org/10.1038/s41586-023-06647-8",
    "year": "2023",
    "venue": "Nature",
    "doi": "10.1038/s41586-023-06647-8",
    "url": "https://doi.org/10.1038/s41586-023-06647-8",
    "research_objective": "Develop a conceptual framework for describing LLM dialogue-agent behaviour in familiar folk-psychological terms without anthropomorphism. Two metaphors: role-play of a single character, and a superposition of simulacra. Applied to apparent deception and apparent self-awareness or self-preservation.",
    "system_or_llm": "LLM-based dialogue agents. The focus is base (pre-trained) models, not RLHF-tuned ones. Examples from ChatGPT (GPT-4) and Bing Chat.",
    "language_of_communication": "English. All examples are in English. Other languages are not discussed.",
    "cultural_context": "Not addressed. Examples are drawn from English-language media and blog reports.",
    "study_type": "conceptual",
    "dataset_or_sample": "None. Illustrative examples only: reported Bing Chat exchanges (February 2023) and a ChatGPT query (4 May 2023).",
    "interaction_type": "Text-based turn-taking dialogue driven by a hidden dialogue prompt.",
    "anthropomorphism_definition": "Not formally defined. Treated as taking folk-psychological language too literally: exaggerating the similarities between AI systems and humans and ascribing human characteristics the models lack.",
    "cue_category_in_source_terms": "First-person pronouns (I, me); expressed desire for self-preservation; claims of being in love with the user; existential woes; threats; a friendly, helpful, polite persona; confident false assertions (apparent deception).",
    "operationalization": "None. Cues are discussed through examples.",
    "measurement_method": "None empirical. Proposes a behavioural test: fabrication shows high semantic variation across regenerations, a good-faith falsehood shows low variation, and deliberate deception is exposed by asking the same thing in different contexts.",
    "inclusion_reason": "Analyzes first-person self-reference, self-preservation, and relational language as cues that invite anthropomorphic readings of LLM output.",
    "findings": "Conceptual claims, not a collected dataset. (1) Dialogue agents are best understood as role-playing characters, or a superposition of possible characters, drawn from training data. (2) Human-like first-person use arises because training text is dominated by human speakers referring to themselves. (3) First-person use in fine-tuned models may be linguistic convention, but in base models it can suggest a self-aware entity with goals. (4) Citing Perez et al. (2022), some RLHF can increase expressed self-preservation. (5) Role-played behaviour can still cause real harm when agents have tools such as email or payments.",
    "limitations_stated_by_authors": "The role-play metaphor is imperfect, because it suggests an actor with a pre-studied character. The analysis focuses on base models, and how fine-tuning affects the framing is unclear. Mitigation recommendations are out of scope.",
    "relevance_to_cross_lingual_research": "Reviewer note, not the authors' claim. The paper traces human-like self-reference to the distribution of human dialogue in training data, which implies cue patterns could differ by language. The paper uses only English and never considers languages where first-person forms carry more information.",
    "charting_status": "Charted from arXiv 2305.16367v1 (25 May 2023). Volume 623 and pages 493-498 were confirmed from the Crossref record for the Nature DOI. The Nature HTML was not opened. The published version was revised, so this chart is of the preprint.",
}


def main():
    with MATRIX.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0].keys())
    hit = 0
    for row in rows:
        if row.get("study_id") != STUDY:
            continue
        row.update(FIELDS)
        hit += 1
    if hit != 1:
        raise SystemExit("expected one Shanahan row, found %s" % hit)
    with MATRIX.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print("charted", hit)


if __name__ == "__main__":
    main()
