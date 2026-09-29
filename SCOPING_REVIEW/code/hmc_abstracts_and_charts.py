"""Decide the 15 HMC records from fetched article-page abstracts.

PDFs still return HTTP 403. Abstracts that clearly fail the LLM-wording
rule are excluded. Abstracts that may still be in scope stay unread.
Chart fields for included studies are filled only where the extracted
finding already states them. Empty language cells become
"Not stated in the text read". Nothing is marked author-checked.
"""

import csv
import random
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
MATRIX = ROOT / "data" / "evidence_matrix.csv"
SAMPLE = ROOT / "data" / "author_verification_sample.csv"

EXCLUDE = {
    "https://stars.library.ucf.edu/hmc/vol4/iss1/8":
        "Abstract read from the journal page. Literature review and propositions on bots as support. Linguistic cues in LLM output are not analyzed.",
    "https://stars.library.ucf.edu/hmc/vol6/iss1/8":
        "Abstract read from the journal page. Social-media socialbots. Users anthropomorphize the bots. The object is not LLM-generated text.",
    "https://stars.library.ucf.edu/hmc/vol8/iss1/4":
        "Abstract read from the journal page. Study-advising chatbots. LLM-generated text is not shown. Outcomes are preference, warmth, and satisfaction.",
    "https://stars.library.ucf.edu/hmc/vol8/iss1/3":
        "Abstract read from the journal page. Voice-assistant politeness and machine-likeness. Textual cues in LLM output cannot be examined.",
    "https://stars.library.ucf.edu/hmc/vol10/iss1/2":
        "Abstract read from the journal page. Essay on authorship with ChatGPT. Anthropomorphic cues in the output are not analyzed.",
    "https://stars.library.ucf.edu/hmc/vol10/iss1/6":
        "Abstract read from the journal page. Social cues in an e-scooter rental app. Not LLM-generated text.",
    "https://stars.library.ucf.edu/hmc/vol11/iss1/8":
        "Abstract read from the journal page. Interviews about generative AI in creative work. Chatbot messages are not analyzed.",
    "https://stars.library.ucf.edu/hmc/vol13/iss1/3":
        "Abstract read from the journal page. Participants rated human-likeness of LLM replies. Linguistic features are not named.",
    "https://stars.library.ucf.edu/hmc/vol13/iss1/4":
        "Abstract read from the journal page. Perceived gender of AI assistants and task stereotypes. Generated wording is not analyzed.",
    "https://stars.library.ucf.edu/hmc/vol13/iss1/5":
        "Abstract read from the journal page. Survey of credibility, tool-versus-social-actor perception, and text versus voice. Generated wording is not analyzed.",
    "https://stars.library.ucf.edu/hmc/vol13/iss1/7":
        "Abstract read from the journal page. Interviews about relationships with Replika. Companion messages are not analyzed.",
    "https://stars.library.ucf.edu/hmc/vol13/iss1/2":
        "Abstract read from the journal page. Measures of human-likeness perception for customer-service chatbots. LLM output is not shown.",
}

RETAIN = {
    "https://stars.library.ucf.edu/hmc/vol6/iss1/6":
        "Abstract read from the journal page. Analyzes linguistic empathy strategies. The abstract does not show that the systems are LLMs. PDF returned HTTP 403.",
    "https://stars.library.ucf.edu/hmc/vol7/iss1/5":
        "Abstract read from the journal page. Conceptualizes Artificial Sociality and names LLMs. Cue analysis is not shown. PDF returned HTTP 403.",
    "https://stars.library.ucf.edu/hmc/vol12/iss1/5":
        "Abstract read from the journal page. Conversation analysis of 503 student chats with LLM chatbots. Anthropomorphic cue labels are not shown. PDF returned HTTP 403.",
}

NOT_STATED = "Not stated in the text read"

# Only facts already present in the extracted finding. Language is filled
# only when that finding names the language of the communication.
CHARTS = {
    "PMID:42507678": {
        "system_or_llm": "Five LLMs",
        "language_of_communication": "Japanese",
        "study_type": "Rating of LLM replies",
        "cue_category_in_source_terms": "Politeness and honorifics; authors' term is cultural alignment",
    },
    "https://doi.org/10.18653/v1/2025.acl-long.1259": {
        "system_or_llm": NOT_STATED,
        "language_of_communication": NOT_STATED,
        "study_type": "Intervention inventory",
        "cue_category_in_source_terms": "First-person pronouns, empathetic phrasing, follow-up questions",
    },
    "https://aclanthology.org/2025.sicon-1.10/": {
        "system_or_llm": "OverlapBot, an LLM chatbot",
        "language_of_communication": NOT_STATED,
        "study_type": "User comparison",
        "cue_category_in_source_terms": "Text overlaps, backchannels, proactive replies, interruptions",
    },
    "https://aclanthology.org/2025.emnlp-main.164/": {
        "system_or_llm": "LLMs",
        "language_of_communication": NOT_STATED,
        "study_type": "Conceptual taxonomy",
        "cue_category_in_source_terms": "Perceptive, linguistic, behavioral, and cognitive cues",
    },
    "https://aclanthology.org/2025.coling-main.239/": {
        "system_or_llm": "LLMs",
        "language_of_communication": NOT_STATED,
        "study_type": "Comparison of LLM and human text",
        "cue_category_in_source_terms": "Politeness and specificity",
    },
    "https://aclanthology.org/2024.findings-emnlp.567/": {
        "system_or_llm": "GPT-4",
        "language_of_communication": NOT_STATED,
        "study_type": "Annotation and rewrite study",
        "cue_category_in_source_terms": "Expressing preferences and emotions",
    },
    "https://aclanthology.org/2023.ranlp-1.18/": {
        "system_or_llm": "ChatGPT",
        "language_of_communication": NOT_STATED,
        "study_type": "Model comparison",
        "cue_category_in_source_terms": "Positive-emotion wording",
    },
    "https://aclanthology.org/2023.emnlp-main.290/": {
        "system_or_llm": "Dialogue systems",
        "language_of_communication": NOT_STATED,
        "study_type": "Position paper",
        "cue_category_in_source_terms": "Gender stereotypes and what counts as acceptable language",
    },
    "https://aclanthology.org/2026.findings-eacl.4/": {
        "system_or_llm": "LLMs",
        "language_of_communication": NOT_STATED,
        "study_type": "Benchmark",
        "cue_category_in_source_terms": "Simulated empathy and presence; emotional enmeshment; illusion of presence; overdependence",
    },
    "https://aclanthology.org/2026.clpsych-1.26/": {
        "system_or_llm": "LLMs",
        "language_of_communication": NOT_STATED,
        "study_type": "Audit with psychologist annotation",
        "cue_category_in_source_terms": "Attachment-language cues, anthropomorphism, over-dependence, boundary blurring",
    },
    "https://aclanthology.org/2026.acl-long.241/": {
        "system_or_llm": "Models fine-tuned on dialogue corpora",
        "study_type": "Fine-tuning experiment",
        "cue_category_in_source_terms": "Backchannels and fillers",
    },
    "https://aclanthology.org/2025.findings-acl.328/": {
        "system_or_llm": "LLMs; training set OCEAN-Chat",
        "language_of_communication": NOT_STATED,
        "study_type": "Training experiment",
        "cue_category_in_source_terms": "Big Five traits expressed in chat",
    },
    "https://aclanthology.org/2025.acl-long.1261/": {
        "system_or_llm": "LLMs",
        "language_of_communication": NOT_STATED,
        "study_type": "Measurement",
        "cue_category_in_source_terms": "Human-like tone (HumT); warmth, social closeness, femininity, low status",
    },
    "https://aclanthology.org/2024.sigdial-1.21/": {
        "system_or_llm": "LLM simulation agents",
        "language_of_communication": NOT_STATED,
        "study_type": "Simulation experiment",
        "cue_category_in_source_terms": "Self-emotion, separate from the user's state",
    },
    "https://aclanthology.org/2024.lrec-main.1166/": {
        "system_or_llm": "LLMs",
        "study_type": "Dataset and generation study",
        "cue_category_in_source_terms": "Extraversion expressed in dialogue",
    },
    "https://doi.org/10.48550/arxiv.2503.10728": {
        "system_or_llm": "Models",
        "language_of_communication": NOT_STATED,
        "study_type": "Measurement",
        "cue_category_in_source_terms": "Anthropomorphism as one of six dark patterns",
    },
    "https://doi.org/10.48550/arxiv.2405.13803": {
        "system_or_llm": "Sunnie LLM agent",
        "language_of_communication": NOT_STATED,
        "study_type": "User study",
        "cue_category_in_source_terms": "Persona prompts and multi-turn conversation",
    },
    "https://doi.org/10.48550/arxiv.2409.02244": {
        "system_or_llm": "LLM counselor",
        "language_of_communication": NOT_STATED,
        "study_type": "Comparison with human counselors",
        "cue_category_in_source_terms": "Self-disclosure and small talk",
    },
    "https://doi.org/10.1145/3771844": {
        "language_of_communication": NOT_STATED,
        "study_type": "Experiment",
    },
    "https://doi.org/10.48550/arxiv.2605.28305": {
        "system_or_llm": "LLMs",
        "language_of_communication": NOT_STATED,
        "study_type": "Measurement",
        "cue_category_in_source_terms": "Reflection markers: wait, hmm, alternatively",
    },
    "https://doi.org/10.48550/arxiv.2607.18250": {
        "system_or_llm": "LLM chatbots",
        "language_of_communication": NOT_STATED,
        "study_type": "Systematic review",
        "cue_category_in_source_terms": "Human-like persona construction, adaptive scaffolding, supportive companionship",
    },
    "https://doi.org/10.48550/arxiv.2606.02493": {
        "system_or_llm": "LLMs",
        "language_of_communication": NOT_STATED,
        "study_type": "Measurement",
        "cue_category_in_source_terms": "Anthropomorphic cues in answers",
    },
    "https://doi.org/10.48550/arxiv.2603.19030": {
        "system_or_llm": "LLMs",
        "language_of_communication": NOT_STATED,
        "study_type": "Conceptual",
        "cue_category_in_source_terms": "Big Five scores; the authors argue these do not measure personality",
    },
    "https://doi.org/10.48550/arxiv.2606.08172": {
        "system_or_llm": "LLMs",
        "language_of_communication": NOT_STATED,
        "study_type": "Measurement",
        "cue_category_in_source_terms": "Empathic language and anthropomorphism under persona prompts",
    },
    "https://doi.org/10.48550/arxiv.2407.11977": {
        "system_or_llm": "LLM conversational agents",
        "language_of_communication": NOT_STATED,
        "study_type": "Conceptual",
        "cue_category_in_source_terms": "Persona",
    },
    "https://doi.org/10.48550/arxiv.2605.23787": {
        "system_or_llm": NOT_STATED,
        "language_of_communication": NOT_STATED,
        "study_type": "Interviews and diaries",
        "cue_category_in_source_terms": "Anthropomorphic cues and default validation",
    },
    "https://doi.org/10.48550/arxiv.2601.08874": {
        "system_or_llm": NOT_STATED,
        "language_of_communication": NOT_STATED,
        "study_type": "Conceptual",
        "cue_category_in_source_terms": "Empathic fluency; illusion of friendship",
    },
    "https://arxiv.org/abs/2508.09998": {
        "system_or_llm": "Gemma-3, Phi-4, o3-mini, and Claude-4",
        "language_of_communication": NOT_STATED,
        "study_type": "Benchmark",
        "cue_category_in_source_terms": "Companionship behaviours; anthropomorphic behaviour is part of the taxonomy",
    },
}


def main():
    with SCREEN.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
        fields = list(rows[0].keys()) if rows else []
    changed = 0
    for row in rows:
        ident = row["identifier"]
        url = ident.split(" | ")[0]
        if url in EXCLUDE and row["decision"] == "retain_for_full_text":
            row["stage"] = "abstract"
            row["decision"] = "exclude_abstract"
            row["reason"] = EXCLUDE[url]
            changed += 1
        elif url in RETAIN and row["decision"] == "retain_for_full_text":
            row["reason"] = RETAIN[url]
            changed += 1
    with SCREEN.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print("screening rows updated", changed)
    print(Counter(r["decision"] for r in rows))

    with MATRIX.open(encoding="utf-8", newline="") as f:
        mrows = list(csv.DictReader(f))
        mfields = list(mrows[0].keys())
    filled = 0
    for row in mrows:
        spec = CHARTS.get(row["study_id"])
        if not spec:
            continue
        for key, value in spec.items():
            if key not in mfields:
                raise SystemExit("bad column " + key)
            if not (row.get(key) or "").strip():
                row[key] = value
                filled += 1
        if not (row.get("charting_status") or "").strip():
            row["charting_status"] = (
                "Partial. System, language, study type, and cue labels filled from the extracted finding on 30 September 2026. Not author-verified."
            )
    with MATRIX.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=mfields)
        writer.writeheader()
        writer.writerows(mrows)
    print("matrix cells filled", filled, "rows", len(mrows))
    print("language", Counter((r.get("language_of_communication") or "").strip() or "(empty)" for r in mrows))
    empty = []
    for r in mrows:
        for key in ("system_or_llm", "language_of_communication", "study_type", "cue_category_in_source_terms"):
            if not (r.get(key) or "").strip():
                empty.append((r["study_id"], key))
    print("still empty", empty)

    with SAMPLE.open(encoding="utf-8", newline="") as f:
        sample = list(csv.DictReader(f))
        sfields = list(sample[0].keys())
    seen = {(r.get("identifier") or "")[:60] for r in sample}
    pool = [
        r for r in rows
        if r["decision"] == "exclude_abstract" and (r.get("identifier") or "")[:60] not in seen
    ]
    rng = random.Random(20260930)
    n = (len(pool) + 9) // 10
    picked = rng.sample(pool, n)
    for r in picked:
        sample.append({
            "check_type": "abstract_exclusion_10pct_seed_20260930",
            "source": r["source"],
            "identifier": r["identifier"],
            "year": r["year"],
            "title": r["title"],
            "decision": r["decision"],
            "reason": r["reason"],
            "author_checked": "",
            "author_note": "Drawn 30 September 2026 from abstract exclusions not already in this file. Seed 20260930. Not checked by the author.",
        })
    with SAMPLE.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=sfields)
        writer.writeheader()
        writer.writerows(sample)
    print("verification pool", len(pool), "drawn", n, "sample rows now", len(sample))


if __name__ == "__main__":
    main()
