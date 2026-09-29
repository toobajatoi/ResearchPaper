"""Record abstract decisions for the 49 ACL Search 1 title-keeps.

Cheng et al. 2025 is already included from the open full text and has no ACL screening row.
Decisions below are abstract decisions. None of the retains is marked included.
"""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
ABSTRACTS = ROOT / "data" / "acl" / "search1_keep_abstracts.txt"

RETAIN = {
    "2025.sicon-1.10": "Abstract defines human-like text behavior as backchanneling, proactive responses, and interruptions. Full text not yet read. Not an inclusion.",
    "2025.emnlp-main.164": "Abstract proposes perceptive, linguistic, behavioral, and cognitive cues for LLM anthropomorphism. Full text not yet read. Not an inclusion.",
    "2025.emnlp-main.1508": "Abstract operationalizes human-like chat as talking style, interaction patterns, and personal attributes. Full text must show whether those are communication cues. Not an inclusion.",
    "2025.coling-main.239": "Abstract ties human likeness of generated counterspeech to linguistic differences, politeness, and specificity. Full text not yet read. Not an inclusion.",
    "2024.findings-emnlp.567": "Abstract contrasts self-anthropomorphic and non-self-anthropomorphic dialogue responses, including preferences and emotions. Full text not yet read. Not an inclusion.",
    "2023.ranlp-1.18": "Abstract compares ChatGPT response versions on use of positive-emotion language. Full text not yet read. Not an inclusion.",
    "2023.emnlp-main.290": "Abstract discusses linguistic factors that elicit anthropomorphism of dialogue systems. Full text not yet read. Not an inclusion.",
    "2022.emnlp-main.215": "Abstract rates whether dialog-system utterances are possible for a machine and treats some as falsely anthropomorphic. Full text not yet read. Not an inclusion.",
    "2021.naacl-main.61": "Abstract treats acknowledgement of prior turns as a human-like feature of generated replies. Full text not yet read. Not an inclusion.",
    "2021.gebnlp-1.4": "Abstract examines gendered and anthropomorphic assistant outputs. Full text must check system type and whether the cues are textual. Not an inclusion.",
}

EXCLUDE = {
    "2026.lrec-1.210": "Global ratings of understanding, empathy, harm, and reasoning. The abstract does not identify linguistic features.",
    "2026.lrec-1.217": "Persona prompts and ingroup or outgroup bias. Not an analysis of anthropomorphic communication cues.",
    "2026.findings-acl.585": "Human-like motivated reasoning under political personas. Cognitive bias, not communication cues.",
    "2026.findings-acl.958": "Personality-steering method. No analysis of anthropomorphic language.",
    "2026.findings-acl.981": "Persona-simulation benchmark. Style scores measure persona match, not anthropomorphic communication.",
    "2026.findings-acl.1159": "Benchmark of understanding user personas, not cues in machine language.",
    "2026.acl-long.118": "Anthropomorphic wording in research articles about LLMs, not cues in model output.",
    "2026.acl-long.1783": "Anthropomorphism operationalized as fidelity to psychological patterns in role-play. The abstract does not analyze linguistic cues.",
    "2025.yrrsds-1.6": "Non-verbal and embodied cues. Textual communication is not the object.",
    "2025.ommm-1.3": "Detection of anthropomorphic language in AI-research utterances, not in model-to-user communication.",
    "2025.ommm-1.8": "Anthropomorphism in YouTube discourse about AI, not in model output.",
    "2025.ommm-1.10": "Anthropomorphic verbs in scientific and public description of LLMs, not cues in model output.",
    "2025.nlpsi-1.6": "Cooperation instructions in a negotiation game. Prompt effect, not a cue analysis.",
    "2025.findings-acl.287": "Theory-of-mind alignment. No linguistic anthropomorphic cues named.",
    "2025.findings-acl.926": "Anthropomorphic language in ACL abstracts and news, not in model output.",
    "2025.findings-emnlp.1100": "Persona role-play framework. Consistency and knowledge, not anthropomorphic cues.",
    "2025.emnlp-demos.70": "Empathetic speech model. Spoken and paralinguistic output; textual cues are not the object.",
    "2025.conll-1.38": "Human-likeness of a mental lexicon on a word-association task. Not communication cues.",
    "2025.coling-main.10": "Method for generating empathetic replies. The abstract does not identify linguistic cues.",
    "2024.naacl-long.341": "Benchmark of human-like dialogue capabilities. No cue inventory in the abstract.",
    "2024.findings-emnlp.420": "Persona prompts for subjective annotation. Not anthropomorphic communication.",
    "2024.eacl-long.49": "Metric for anthropomorphism in research papers and news headlines, not in model output.",
    "2024.acl-long.801": "Speech acoustics for empathetic dialogue. Voice, not textual cues.",
    "2024.acl-demos.7": "Avatar with a talking face and speech. Visual and voice anthropomorphism.",
    "2023.yrrsds-1.12": "Author research overview. No analysis of textual cues.",
    "2023.yrrsds-1.14": "The abstract does not describe a study or a conceptualization that can be charted.",
    "2023.yrrsds-1.23": "Spoken-dialogue research plan. Textual cues are not analyzed.",
    "2023.sigdial-1.57": "Position on common ground. The abstract does not specify communicative cues in system text.",
    "2023.nllp-1.1": "The cues named in the abstract are human voice and pictorial avatars, not textual features.",
    "2023.findings-acl.605": "Psycholinguistic pronoun priming. Human-like parsing, not anthropomorphic communication.",
    "2023.findings-acl.843": "Architecture for empathetic generation. No cue analysis.",
    "2022.findings-aacl.14": "Taxonomy of user self-disclosure, not of machine language.",
    "2022.coling-1.1": "Language-model predictions of Italian zero-pronoun coreference. Not anthropomorphic communication.",
    "2022.codi-1.3": "How users test a social chatbot. User behavior, not machine cues.",
    "2021.wanlp-1.17": "Arabic empathetic generation scored with perplexity, BLEU, and a global empathy rating.",
    "2020.wanlp-1.6": "LSTM sequence-to-sequence chatbot, not an LLM. Global empathy and fluency scores.",
    "2020.nlp4convai-1.14": "Persona chit-chat generation. No anthropomorphic-cue analysis.",
    "2020.acl-main.131": "Persona-perception dialogue model. No anthropomorphic-cue analysis.",
    "2020.aacl-main.65": "Persona embeddings for transfer. Not an analysis of anthropomorphic communication.",
}


def authors_from_abstracts():
    text = ABSTRACTS.read_text(encoding="utf-8")
    found = {}
    for block in text.split("\n---\n"):
        ident = re.search(r"^ID: (\S+)", block, re.M)
        authors = re.search(r"^AUTHORS: (.+)$", block, re.M)
        if ident and authors:
            found[ident.group(1)] = authors.group(1).replace(" and ", "; ")
    return found


def anthology_id(url):
    match = re.search(r"aclanthology\.org/([^/\s]+)/?", url or "")
    return match.group(1) if match else ""


def main():
    authors = authors_from_abstracts()
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0].keys()) if rows else []
    retain_n = exclude_n = skipped = 0
    for row in rows:
        if row["source"] != "ACL Anthology metadata Search 1":
            continue
        if row["decision"] != "retain_for_abstract":
            skipped += 1
            continue
        key = anthology_id(row["identifier"])
        row["authors"] = authors.get(key, row["authors"])
        if key in RETAIN:
            row["stage"] = "abstract"
            row["decision"] = "retain_for_full_text"
            row["reason"] = RETAIN[key]
            retain_n += 1
        elif key in EXCLUDE:
            row["stage"] = "abstract"
            row["decision"] = "exclude_abstract"
            row["reason"] = EXCLUDE[key]
            exclude_n += 1
        else:
            raise SystemExit(f"no decision for {key}")
    with SCREEN.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("retain", retain_n, "exclude", exclude_n, "already decided", skipped)
    expected = set(RETAIN) | set(EXCLUDE)
    print("decision keys", len(expected))


if __name__ == "__main__":
    main()
