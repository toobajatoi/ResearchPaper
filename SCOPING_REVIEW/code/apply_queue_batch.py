import csv
from pathlib import Path

SCREEN = Path(__file__).resolve().parents[1] / "data" / "screening.csv"

INCLUDE = {
    "https://aclanthology.org/2025.sicon-1.10/": "Full text read on 30 September 2026. OverlapBot, an LLM chatbot, generates text overlaps, backchannels, proactive replies, and interruptions. Users made 72 percent more turns than with turn-taking.",
    "https://aclanthology.org/2025.emnlp-main.164/": "Full text read on 30 September 2026. Conceptual design taxonomy of LLM anthropomorphism with four cue groups: perceptive, linguistic, behavioral, and cognitive.",
    "https://aclanthology.org/2025.coling-main.239/": "Full text read on 30 September 2026. LLM counterspeech is distinguishable from human counterspeech. The linguistic differences named are politeness and specificity.",
    "https://aclanthology.org/2024.findings-emnlp.567/": "Full text read on 30 September 2026. Self-anthropomorphism in dialogue is operationalized as expressing preferences and emotions. GPT-4 classifies and rewrites responses. Two annotators on 500 turns had Cohen's kappa 0.83.",
    "https://aclanthology.org/2023.ranlp-1.18/": "Full text read on 30 September 2026. Emotion-conditioned ChatGPT uses positive-emotion wording more often than the standard model. A prompt-only emotion condition does the opposite.",
    "https://aclanthology.org/2023.emnlp-main.290/": "Full text read on 30 September 2026. Position paper on linguistic factors that lead users to personify dialogue systems, including gender stereotypes and what counts as acceptable language.",
    "https://aclanthology.org/2026.findings-eacl.4/": "Full text read on 30 September 2026. Affective hallucination is defined as LLM replies that simulate empathy and presence. AHaBench scores emotional enmeshment, illusion of presence, and overdependence. DPO reduced those behaviours.",
    "https://aclanthology.org/2026.clpsych-1.26/": "Full text read on 30 September 2026. Audits attachment-language cues in LLM replies, including anthropomorphism and over-dependence. Judge models alone were unreliable. Twenty-five psychologist-annotated conversations showed boundary blurring.",
    "https://aclanthology.org/2026.acl-long.241/": "Full text read on 30 September 2026. Fine-tuning on English and Japanese dialogue corpora changes how models represent backchannels and fillers. Fine-tuned generations were closer to human utterances.",
    "https://aclanthology.org/2025.findings-acl.328/": "Full text read on 30 September 2026. P-React trains LLMs to express Big Five traits in chat, treated as anthropomorphic behaviour. The training set is OCEAN-Chat.",
    "https://aclanthology.org/2025.acl-long.1261/": "Full text read on 30 September 2026. HumT measures human-like tone in LLM text. Higher HumT tracks warmth, social closeness, femininity, and low status. DumT reduces that tone. Users often preferred less human-like outputs.",
    "https://aclanthology.org/2024.sigdial-1.21/": "Full text read on 30 September 2026. Giving LLM simulation agents a self-emotion, separate from the user's state, made their dialogue strategies more like human strategies and changed about half of their decisions.",
    "https://aclanthology.org/2024.lrec-main.1166/": "Full text read on 30 September 2026. PSYDIAL is a Korean dialogue set in which LLMs are prompted to express Extraversion. Models trained on it produced personality-bearing replies that chit-chat models did not.",
    "https://arxiv.org/abs/2508.09998": "Full text read on 30 September 2026. INTIMA scores 31 companionship behaviours with 368 prompts. On Gemma-3, Phi-4, o3-mini, and Claude-4, companionship-reinforcing replies were more common than boundary-maintaining ones. Anthropomorphic behaviour is part of the taxonomy.",
}

EXCLUDE_FULL = {
    "https://aclanthology.org/2021.gebnlp-1.4/": "Full text read on 30 September 2026. The systems are Alexa, Google Assistant, and Siri in 2021, not large language models. Gendered pronouns in those outputs are out of the LLM set.",
    "https://aclanthology.org/2021.naacl-main.61/": "Full text read on 30 September 2026. A 2021 decoding method for neural chatbots. Acknowledgement is a generation-quality target. The systems are pre-LLM dialogue models.",
    "https://aclanthology.org/2022.emnlp-main.215/": "Full text read on 30 September 2026. Ratings of about 900 dialogue-corpus turns for whether a machine could say them. The object is training data, not LLM-generated text.",
    "https://aclanthology.org/2025.emnlp-main.1508/": "Full text read on 30 September 2026. V-VAE is a control method for persona-consistent chat. It does not analyze anthropomorphic communication cues.",
    "https://aclanthology.org/2025.findings-acl.1185/": "Full text read on 30 September 2026. Personality is a Big Five score that changes with Prisoner's Dilemma payoffs. It is not an analysis of wording.",
}

EXCLUDE_ABSTRACT = {
    "https://doi.org/10.1109/iscid68789.2025.00026": "Abstract retrieved on 30 September 2026. Users prefer a customized persona chatbot for emotional support and a functional chatbot for tasks. Linguistic features of the personas are not analyzed. The IEEE PDF was not retrieved.",
    "https://doi.org/10.1109/tts.2025.3563812": "Abstract retrieved on 30 September 2026. Ethical scenarios for empathetic AI in medicine. The paper does not analyze linguistic cues in model output. The IEEE PDF was not retrieved.",
    "https://doi.org/10.1109/hri61500.2025.10973942": "Abstract retrieved on 30 September 2026. A physical collaborative robot uses small talk during assembly. The system is an embodied robot, not an LLM. The IEEE PDF was not retrieved.",
}

DUPLICATE = {
    "https://doi.org/10.18653/v1/2025.acl-long.1261": "Duplicate of https://aclanthology.org/2025.acl-long.1261/. The Anthology record is the included version.",
    "https://doi.org/10.18653/v1/2025.findings-acl.328": "Duplicate of https://aclanthology.org/2025.findings-acl.328/. The Anthology record is the included version.",
}

RETAIN = {
    "https://doi.org/10.1109/iccci70321.2026.11666502": "Abstract retrieved on 30 September 2026. AnthroKit controls LLM tone with six parameters: warmth, empathy, formality, hedging, self-reference, and emoji. Experiment n=126. The IEEE PDF was not retrieved, so this is not an inclusion.",
}

rows = list(csv.DictReader(SCREEN.open(encoding="utf-8")))
fields = list(rows[0].keys())
counts = {"include": 0, "full": 0, "abs": 0, "dup": 0, "retain": 0}
for row in rows:
    ident = row["identifier"]
    if ident in INCLUDE and row["decision"] == "retain_for_full_text":
        row["stage"] = "full_text"
        row["decision"] = "include"
        row["reason"] = INCLUDE[ident]
        counts["include"] += 1
    elif ident in EXCLUDE_FULL and row["decision"] == "retain_for_full_text":
        row["stage"] = "full_text"
        row["decision"] = "exclude_full_text"
        row["reason"] = EXCLUDE_FULL[ident]
        counts["full"] += 1
    elif ident in EXCLUDE_ABSTRACT and row["decision"] == "retain_for_full_text":
        row["stage"] = "abstract"
        row["decision"] = "exclude_abstract"
        row["reason"] = EXCLUDE_ABSTRACT[ident]
        counts["abs"] += 1
    elif ident in DUPLICATE and row["decision"] == "retain_for_full_text":
        row["stage"] = "abstract"
        row["decision"] = "exclude_duplicate"
        row["reason"] = DUPLICATE[ident]
        counts["dup"] += 1
    elif ident in RETAIN:
        row["reason"] = RETAIN[ident]
        counts["retain"] += 1

print(counts)
with SCREEN.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

from collections import Counter

print(Counter(row["decision"] for row in rows))
print("n", len(rows))
