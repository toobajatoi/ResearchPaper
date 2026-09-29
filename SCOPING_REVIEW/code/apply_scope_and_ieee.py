"""Apply the LLM-only scope decision and the IEEE abstract exclusion."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
SAMPLE = ROOT / "data" / "author_verification_sample.csv"

SCOPE = {
    "PMID:42726769": "Scope decision 29 September 2026: primary set is LLM-generated text. This study uses a simulated live-stream host. Generative status was not established.",
    "PMID:42651447": "Scope decision 29 September 2026: primary set is LLM-generated text. The anthropomorphism manipulation is a researcher-written script.",
    "PMID:42549111": "Scope decision 29 September 2026: primary set is LLM-generated text. The system is a pseudo-LLM.",
    "PMID:42510216": "Scope decision 29 September 2026: primary set is LLM-generated text. The stimuli are researcher-written government-chatbot scripts.",
    "PMID:35071147": "Scope decision 29 September 2026: primary set is LLM-generated text. MIA is a rule-based scripted chatbot.",
    "PMID:37561567": "Scope decision 29 September 2026: primary set is LLM-generated text. The stimuli are humanlike versus machine-like scripts for health conversational agents, not established LLM output.",
    "PMID:35802407": "Scope decision 29 September 2026: primary set is LLM-generated text. This review charts conversational agents, including pre-LLM systems.",
    "https://aclanthology.org/2021.conll-1.4/": "Scope decision 29 September 2026: primary set is LLM-generated text. This is a pre-LLM conversational agent.",
}

IEEE = "https://doi.org/10.1109/icbiti65527.2025.11501086"
IEEE_REASON = "Conceptual attachment model; no linguistic cue analysis; abstract read on IEEE Xplore."


def load(path):
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return rows, list(rows[0].keys())


def main():
    rows, fields = load(SCREEN)
    hit = 0
    for row in rows:
        if row["identifier"] in SCOPE:
            pre_llm_title_only = row["identifier"].startswith("https://aclanthology.org/2021.conll")
            row["stage"] = "abstract" if pre_llm_title_only else "full_text"
            row["decision"] = "exclude_abstract" if pre_llm_title_only else "exclude_full_text"
            row["reason"] = SCOPE[row["identifier"]]
            hit += 1
        if row["identifier"].lower() == IEEE:
            row["stage"] = "abstract"
            row["decision"] = "exclude_abstract"
            row["reason"] = IEEE_REASON
            hit += 1
    sample, sfields = load(SAMPLE)
    for row in sample:
        match = next((item for item in rows if item["identifier"] == row["identifier"]), None)
        if row["identifier"].lower() == IEEE:
            row["decision"] = "exclude_abstract"
            row["reason"] = IEEE_REASON
            row["author_checked"] = "yes"
            row["author_note"] = IEEE_REASON
        elif match and row["identifier"] in SCOPE:
            row["decision"] = match["decision"]
            row["reason"] = match["reason"]
    with SCREEN.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    with SAMPLE.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=sfields)
        writer.writeheader()
        writer.writerows(sample)
    print("updated", hit)


if __name__ == "__main__":
    main()
