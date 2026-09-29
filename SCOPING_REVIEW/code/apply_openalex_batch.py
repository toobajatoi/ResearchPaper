"""Record one batch of OpenAlex abstract decisions. Does not mark studies included."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"

DECISIONS = {
    "https://doi.org/10.1145/3758871.3758884": (
        "exclude_abstract",
        "abstract",
        "User study of media dependency on role-playing chatbots. The anthropomorphism level is not specified as linguistic cues.",
    ),
    "https://doi.org/10.48550/arxiv.2409.15769": (
        "retain_for_full_text",
        "abstract",
        "Compares third-person narrator, first-person creator, and first-person object modes in generative characters. Full text needed. Not an inclusion.",
    ),
    "https://doi.org/10.14569/ijacsa.2025.0161218": (
        "exclude_abstract",
        "abstract",
        "Technology-acceptance review. No linguistic cue analysis.",
    ),
    "https://doi.org/10.1145/3772318.3790891": (
        "exclude_abstract",
        "abstract",
        "Fandom study of an AI VTuber. Persona is the performer character, not an analysis of wording.",
    ),
    "https://doi.org/10.48550/arxiv.2411.17157": (
        "exclude_duplicate",
        "abstract",
        "Duplicate of https://doi.org/10.1145/3758871.3758884.",
    ),
    "https://doi.org/10.48550/arxiv.2405.06079": (
        "exclude_duplicate",
        "abstract",
        "Duplicate of https://doi.org/10.1145/3613905.3650818. The system is a pseudo-LLM and is out of scope.",
    ),
    "https://doi.org/10.5281/zenodo.19679579": (
        "retain_for_full_text",
        "abstract",
        "Conceptual paper. Affective risk is tied to person-like linguistic cues. Full text needed. Not an inclusion.",
    ),
    "https://doi.org/10.5281/zenodo.19679578": (
        "exclude_duplicate",
        "abstract",
        "Duplicate of https://doi.org/10.5281/zenodo.19679579.",
    ),
    "https://doi.org/10.3389/fcogn.2026.1824836": (
        "exclude_duplicate",
        "abstract",
        "Duplicate of PMID:42549111. The system is a pseudo-LLM and is out of scope.",
    ),
    "https://doi.org/10.3929/ethz-c-000803246": (
        "exclude_duplicate",
        "abstract",
        "Duplicate of https://doi.org/10.1145/3805689.3812324, already queued for full text.",
    ),
    "https://doi.org/10.5167/uzh-435494": (
        "exclude_duplicate",
        "abstract",
        "Duplicate of https://doi.org/10.1145/3805689.3812324, already queued for full text.",
    ),
    "https://doi.org/10.48550/arxiv.2601.09869": (
        "exclude_duplicate",
        "abstract",
        "Duplicate of https://doi.org/10.1145/3805689.3812324, already queued for full text.",
    ),
    "https://doi.org/10.1145/3768310.3807828": (
        "exclude_abstract",
        "abstract",
        "Qualitative note on consequential anthropomorphism. The abstract does not name linguistic features.",
    ),
    "https://doi.org/10.3389/fpsyg.2025.1568911": (
        "exclude_abstract",
        "abstract",
        "Source-attribution experiment. The message wording is held constant.",
    ),
    "https://doi.org/10.48550/arxiv.2402.04470": (
        "exclude_duplicate",
        "abstract",
        "Duplicate of https://doi.org/10.1177/25152459251357566.",
    ),
    "https://doi.org/10.5281/zenodo.18885750": (
        "exclude_abstract",
        "abstract",
        "Conceptual paper on narrative capture. No linguistic cue analysis.",
    ),
    "https://doi.org/10.5281/zenodo.18885751": (
        "exclude_duplicate",
        "abstract",
        "Duplicate of https://doi.org/10.5281/zenodo.18885750.",
    ),
    "https://doi.org/10.5281/zenodo.17846743": (
        "exclude_abstract",
        "abstract",
        "Dataset note on observed emotional overflow. It does not analyze linguistic cues.",
    ),
    "https://doi.org/10.5281/zenodo.17797656": (
        "exclude_duplicate",
        "abstract",
        "Duplicate of https://doi.org/10.5281/zenodo.17846743.",
    ),
    "https://doi.org/10.5281/zenodo.18934917": (
        "exclude_duplicate",
        "abstract",
        "Duplicate of https://doi.org/10.5281/zenodo.17846743.",
    ),
    "https://doi.org/10.5281/zenodo.17924460": (
        "exclude_duplicate",
        "abstract",
        "Duplicate of https://doi.org/10.5281/zenodo.17846743.",
    ),
    "https://doi.org/10.5281/zenodo.17652408": (
        "exclude_duplicate",
        "abstract",
        "Duplicate of https://doi.org/10.5281/zenodo.17846743.",
    ),
    "https://doi.org/10.5281/zenodo.17790906": (
        "exclude_duplicate",
        "abstract",
        "Duplicate of https://doi.org/10.5281/zenodo.17846743.",
    ),
    "https://doi.org/10.48550/arxiv.2607.18250": (
        "retain_for_full_text",
        "abstract",
        "Systematic review of children's interactions with LLM chatbots. One driver named is human-like persona construction. Full text needed. Not an inclusion.",
    ),
    "https://doi.org/10.48550/arxiv.2601.10198": (
        "retain_for_full_text",
        "abstract",
        "Benchmark of persona and role-play dialogue. Full text needed to see whether the behaviours are linguistic cues. Not an inclusion.",
    ),
}


def main():
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0].keys())
    hit = 0
    for row in rows:
        choice = DECISIONS.get(row["identifier"])
        if not choice:
            continue
        if "Abstract not yet read" not in row["reason"]:
            continue
        decision, stage, reason = choice
        row["decision"] = decision
        row["stage"] = stage
        row["reason"] = reason
        hit += 1
    with SCREEN.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print("applied", hit)


if __name__ == "__main__":
    main()
