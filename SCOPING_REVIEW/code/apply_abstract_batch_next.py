"""Record the next 20 OpenAlex abstract decisions. Does not mark any study included."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"

DECISIONS = {
    "https://doi.org/10.20944/preprints202501.2278.v1": (
        "exclude_abstract",
        "abstract",
        "Embodied NAO robot in a classroom. Anthropomorphism is the robot's body. No analysis of linguistic cues in LLM text.",
    ),
    "https://doi.org/10.2139/ssrn.4620986": (
        "exclude_abstract",
        "abstract",
        "Abstract field is empty. The title is a historical claim about AI as authority, not linguistic cues in model output.",
    ),
    "https://doi.org/10.18653/v1/2025.findings-acl.1185": (
        "exclude_abstract",
        "abstract",
        "LLM agents play the Prisoner's Dilemma. Personality is a game-behavior score, not wording.",
    ),
    "https://doi.org/10.1609/aies.v7i2.31903": (
        "retain_for_full_text",
        "abstract",
        "Role prompts are used to elicit anthropomorphic features in chatbot language, and the paper categorizes those features. Full text needed. Not an inclusion.",
    ),
    "https://doi.org/10.1007/s10664-026-10853-z": (
        "exclude_abstract",
        "abstract",
        "Asks whether code models do static analysis. Not anthropomorphic communication.",
    ),
    "https://doi.org/10.54254/2753-7064/36/2024bj1002": (
        "retain_for_full_text",
        "abstract",
        "Describes GPT-4o dialogue as linguistic anthropomorphism and emotional anthropomorphism, including simulated empathy. Full text needed. Not an inclusion.",
    ),
    "https://doi.org/10.1016/j.tmp.2025.101442": (
        "exclude_abstract",
        "abstract",
        "Tourism brand survey. Anthropomorphism is a moderator of engagement, not a linguistic analysis.",
    ),
    "https://doi.org/10.1108/ajim-03-2025-0125": (
        "exclude_abstract",
        "abstract",
        "Experiments on emotional attachment. The abstract does not name a linguistic cue.",
    ),
    "https://doi.org/10.1007/978-3-031-93415-5_18": (
        "exclude_abstract",
        "abstract",
        "Abstract field is empty. The title is an AI-literacy training study of trust, not cue analysis.",
    ),
    "https://doi.org/10.1016/j.caeai.2026.100554": (
        "exclude_abstract",
        "abstract",
        "Student literacy survey. Anthropomorphism is a misconception about chatbots, not a cue coded in output.",
    ),
    "https://doi.org/10.1016/j.jbusres.2025.115507": (
        "exclude_abstract",
        "abstract",
        "Virtual influencers in live commerce. Not an analysis of linguistic cues in LLM text.",
    ),
    "https://doi.org/10.22318/icls2024.230928": (
        "exclude_abstract",
        "abstract",
        "Compares LLM feedback with human feedback. Anthropomorphic language is how people describe the tool, not cues coded in the model's text.",
    ),
    "https://doi.org/10.1016/j.chbah.2025.100189": (
        "exclude_abstract",
        "abstract",
        "Employee emotions toward workplace agents. The abstract centers visual embodiment and does not analyze wording.",
    ),
    "https://doi.org/10.55982/openpraxis.16.1.631": (
        "exclude_abstract",
        "abstract",
        "Metaphor discussion for AI literacy. Not an analysis of cues in model output.",
    ),
    "https://doi.org/10.1007/978-3-031-90271-0_28": (
        "exclude_abstract",
        "abstract",
        "Abstract field is empty. The title is an after-sales repurchase model, not linguistic cues.",
    ),
    "https://doi.org/10.1515/lass-2024-0072": (
        "exclude_abstract",
        "abstract",
        "Conceptual argument about attributing qualia to generative AI. No cue inventory.",
    ),
    "https://doi.org/10.26737/jetl.v9i2.6261": (
        "exclude_abstract",
        "abstract",
        "Instructor acceptance survey. Anthropomorphism is a predictor, not a linguistic analysis.",
    ),
    "https://doi.org/10.21632/irjbs.18.1.67-84": (
        "exclude_abstract",
        "abstract",
        "User-satisfaction survey. Anthropomorphism is a rating factor, not cue coding.",
    ),
    "https://doi.org/10.1007/s12525-026-00884-1": (
        "exclude_abstract",
        "abstract",
        "Abstract field is empty. The title is customer forgiveness after service failure, not linguistic cues.",
    ),
    "https://doi.org/10.1145/3772318.3791005": (
        "exclude_abstract",
        "abstract",
        "Predicts who anthropomorphizes a LaMDA dialogue excerpt. It does not code linguistic features of that dialogue.",
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
    if hit != 20:
        raise SystemExit("expected 20 updates, got %s" % hit)
    with SCREEN.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print("applied", hit)


if __name__ == "__main__":
    main()
