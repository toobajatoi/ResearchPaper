"""Reopen exclusions after the abstract check. Does not set author_checked.

None of these rows is marked included. Full text is still required.
"""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
SAMPLE = ROOT / "data" / "author_verification_sample.csv"

FULL = "retain_for_full_text"
ABS = "retain_for_abstract"

# identifier -> (stage, decision, reason)
UPDATES = {
    "https://aclanthology.org/2025.acl-long.1261/": (
        "abstract",
        FULL,
        "Abstract read. HumT and SocioT measure human-like tone in LLM text and relate it to warmth, closeness, femininity, and status. Full text not yet charted. Not an inclusion.",
    ),
    "https://doi.org/10.18653/v1/2025.acl-long.1261": (
        "abstract",
        FULL,
        "Same study as the ACL Anthology record 2025.acl-long.1261. Kept for full text. Not an inclusion.",
    ),
    "https://doi.org/10.48550/arxiv.2502.13259": (
        "duplicate",
        "exclude_duplicate",
        "Preprint of Cheng, Yu, and Jurafsky, ACL 2025, DOI 10.18653/v1/2025.acl-long.1261. The version of record is kept.",
    ),
    "https://aclanthology.org/2021.conll-1.4/": (
        "abstract",
        FULL,
        "Abstract read. Language style changed how human-like a text agent seemed, including pronouns and projected gender. The agent is pre-LLM. Full text waits on the LLM-versus-conversational-AI scope decision. Not an inclusion.",
    ),
    "https://aclanthology.org/2026.findings-eacl.4/": (
        "abstract",
        FULL,
        "Abstract read. Affective hallucination includes LLM replies that simulate relational closeness, such as offering presence. Full text not yet charted. Not an inclusion.",
    ),
    "https://aclanthology.org/2026.acl-long.241/": (
        "abstract",
        FULL,
        "Abstract read. Backchannels and fillers in English and Japanese are studied as human-like conversational behaviour in language models. Full text not yet charted. Not an inclusion.",
    ),
    "https://aclanthology.org/2025.findings-acl.328/": (
        "abstract",
        FULL,
        "Personality expressed in generated text is in scope under the 29 September 2026 rule. Full text not yet charted. Not an inclusion.",
    ),
    "https://doi.org/10.18653/v1/2025.findings-acl.328": (
        "abstract",
        FULL,
        "Same study as ACL Anthology 2025.findings-acl.328. Kept for full text. Not an inclusion.",
    ),
    "https://doi.org/10.48550/arxiv.2406.12548": (
        "duplicate",
        "exclude_duplicate",
        "Preprint of the P-React conference paper, DOI 10.18653/v1/2025.findings-acl.328. The version of record is kept.",
    ),
    "PMID:41438004": (
        "abstract",
        FULL,
        "Personality expressed in generated text is in scope under the 29 September 2026 rule. The paper shapes personality in LLM wording. Full text not yet charted. Not an inclusion.",
    ),
    "https://aclanthology.org/2024.findings-emnlp.77/": (
        "abstract",
        "exclude_abstract",
        "Abstract check: traits are formalised as behaviour patterns such as truthfulness and sycophancy, not as communication cues. Exclusion stands.",
    ),
    "PMID:39176045": (
        "abstract",
        "exclude_abstract",
        "Philosophy of whether GPT-4 is sentient. It does not analyze communication cues. Exclusion stands.",
    ),
    "https://doi.org/10.3389/fpsyg.2024.1292675": (
        "abstract",
        "exclude_abstract",
        "Same paper as PMID 39176045. Philosophy of machine consciousness, not communication cues. Exclusion stands.",
    ),
    "https://aclanthology.org/2026.acl-long.639/": (
        "abstract",
        "exclude_abstract",
        "Human-like here means indistinguishable from human writing across languages. That is text detection, not anthropomorphic cues. Exclusion stands. The concreteness and cultural-gap result can be mentioned in the discussion.",
    ),
}

TITLE_KEEP = {
    "https://aclanthology.org/2026.tacl-1.24/": "Title names role-playing LLMs. Abstract not yet read. Not an inclusion.",
    "https://aclanthology.org/2026.lrec-1.881/": "Title names personality induction in LLMs. Abstract not yet read. Not an inclusion.",
    "https://aclanthology.org/2026.findings-acl.368/": "Title names emotion-aware social agents. Abstract not yet read. Not an inclusion.",
    "https://aclanthology.org/2026.findings-acl.1283/": "Title names LLM role-playing. Abstract not yet read. Not an inclusion.",
    "https://aclanthology.org/2026.eacl-long.82/": "Title names generative personality simulation. Abstract not yet read. Not an inclusion.",
    "https://aclanthology.org/2026.clpsych-1.26/": "Title names attachment language cues in human-LLM dialogue. Abstract not yet read. Not an inclusion.",
    "https://aclanthology.org/2025.naacl-long.323/": "Title names role-playing in text-based worlds. Abstract not yet read. Not an inclusion.",
    "https://aclanthology.org/2025.naacl-long.367/": "Title names backchannel prediction. Abstract must show whether the cue is textual. Not an inclusion.",
    "https://aclanthology.org/2025.findings-acl.47/": "Title names role-playing LLMs. Abstract not yet read. Not an inclusion.",
    "https://aclanthology.org/2025.findings-acl.938/": "Title names a survey of role-playing agents. Abstract not yet read. Not an inclusion.",
    "https://aclanthology.org/2025.findings-acl.1185/": "Title names personality in LLM agents. Abstract must show that personality is expressed in wording. Not an inclusion.",
    "https://aclanthology.org/2025.emnlp-main.1730/": "Title names filler insertion in speech synthesis. Abstract must show whether a textual cue is analyzed. Not an inclusion.",
    "https://aclanthology.org/2024.yrrsds-1.32/": "Title names emotional and social engagement in conversational agents. Abstract not yet read. Not an inclusion.",
    "https://aclanthology.org/2024.sigdial-1.21/": "Title names emotion in generated dialogue. Abstract not yet read. Not an inclusion.",
    "https://aclanthology.org/2024.naacl-long.228/": "Title names role-play prompting. Abstract must show a cue analysis rather than a prompt recipe. Not an inclusion.",
    "https://aclanthology.org/2024.lrec-main.1166/": "Title names personality-based dialogue generation. Abstract not yet read. Not an inclusion.",
    "https://aclanthology.org/2024.findings-emnlp.819/": "Title names role-playing agents. Abstract not yet read. Not an inclusion.",
    "https://doi.org/10.18653/v1/2026.clpsych-1.26": "Same study as ACL Anthology 2026.clpsych-1.26. Abstract not yet read. Not an inclusion.",
}

INTIMA = {
    "source": "Citation chase",
    "search_date": "2026-09-29",
    "record_number": "1",
    "authors": "Kaffee, Lucie-Aimée; Pistilli, Giada; Jernite, Yacine",
    "year": "2026",
    "title": "INTIMA: A Benchmark for Human-AI Companionship Behavior",
    "identifier": "https://arxiv.org/abs/2508.09998",
    "stage": "abstract",
    "decision": FULL,
    "reason": (
        "Located from the arXiv PDF, which carries a 2026 AAAI copyright line. "
        "The benchmark scores companionship-reinforcing and boundary-maintaining replies, "
        "including anthropomorphic wording, in Gemma-3, Phi-4, o3-mini, and Claude. "
        "Full text is not yet charted. Not an inclusion."
    ),
}


def load(path):
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return rows, list(rows[0].keys())


def main():
    rows, fields = load(SCREEN)
    seen = set()
    for row in rows:
        update = UPDATES.get(row["identifier"])
        if update:
            row["stage"], row["decision"], row["reason"] = update
            seen.add(row["identifier"])
        reason = TITLE_KEEP.get(row["identifier"])
        if reason and row["decision"] == "exclude_title":
            row["stage"] = "title"
            row["decision"] = ABS
            row["reason"] = reason
            seen.add(row["identifier"])
        elif reason and row["decision"] == ABS and "Narrow OpenAlex" in row["reason"]:
            row["reason"] = reason
            seen.add(row["identifier"])
    missing = [key for key in list(UPDATES) + list(TITLE_KEEP) if key not in seen]
    if not any(row["identifier"] == INTIMA["identifier"] for row in rows):
        rows.append(INTIMA)
    with SCREEN.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    sample, sfields = load(SAMPLE)
    changed = 0
    for row in sample:
        match = next((item for item in rows if item["identifier"] == row["identifier"]), None)
        if not match:
            continue
        if row["decision"] != match["decision"] or row["reason"] != match["reason"]:
            row["decision"] = match["decision"]
            row["reason"] = match["reason"]
            changed += 1
        if row["author_checked"] or row["author_note"]:
            raise SystemExit("author fields were not empty")
    with SAMPLE.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=sfields)
        writer.writeheader()
        writer.writerows(sample)
    print("updated", len(seen), "sample rows refreshed", changed, "missing", missing)


if __name__ == "__main__":
    main()
