"""Record one batch of OpenAlex abstract decisions. Does not mark studies included."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"

DECISIONS = {
    "https://doi.org/10.1016/j.concog.2024.103733": (
        "exclude_abstract",
        "abstract",
        "Mind-perception experiment on agency and experience. No linguistic cue analysis.",
    ),
    "https://doi.org/10.1080/14703297.2025.2499177": (
        "exclude_abstract",
        "abstract",
        "Embodied mixed-reality agent. Perception and cognitive load, not textual cues.",
    ),
    "https://doi.org/10.1075/is.25116.maz": (
        "exclude_abstract",
        "abstract",
        "Survey of perceived anthropomorphism, privacy, and trust. No linguistic cue analysis.",
    ),
    "https://doi.org/10.1016/j.techsoc.2025.102995": (
        "retain_for_abstract",
        "retrieved",
        "OpenAlex abstract field is empty. Still unread.",
    ),
    "https://doi.org/10.1080/10447318.2026.2632156": (
        "exclude_abstract",
        "abstract",
        "Interviews about how people perceive LLM-to-LLM dialogue. No analysis of the wording.",
    ),
    "https://doi.org/10.1080/08874417.2024.2442438": (
        "exclude_abstract",
        "abstract",
        "Adoption survey. Anthropomorphism is a measured characteristic, not a cue analysis.",
    ),
    "https://doi.org/10.1016/j.ijhcs.2024.103375": (
        "exclude_abstract",
        "abstract",
        "Perceptions of text-to-image outputs. Visual, not linguistic cues.",
    ),
    "https://doi.org/10.18653/v1/2025.emnlp-main.164": (
        "exclude_duplicate",
        "abstract",
        "Duplicate of https://aclanthology.org/2025.emnlp-main.164/, already queued for full text.",
    ),
    "https://doi.org/10.1007/s13347-025-00875-8": (
        "exclude_abstract",
        "abstract",
        "Conceptual essay on the definition of generative AI. No linguistic cue analysis.",
    ),
    "https://doi.org/10.2139/ssrn.5894082": (
        "exclude_title",
        "title",
        "Symbol-grounding essay. OpenAlex has no abstract. The title is not about communication cues.",
    ),
    "https://doi.org/10.1108/jcm-03-2025-7704": (
        "exclude_abstract",
        "abstract",
        "Special-issue editorial on marketing. No cue analysis.",
    ),
    "https://doi.org/10.3389/fcomp.2025.1638657": (
        "exclude_abstract",
        "abstract",
        "Opinion piece on trust in AI tutors. No linguistic cue analysis.",
    ),
    "https://doi.org/10.1080/10447318.2024.2426029": (
        "exclude_abstract",
        "abstract",
        "Addiction survey. Perceived anthropomorphism and empathy are ratings, not wording.",
    ),
    "https://doi.org/10.23919/jsc.2025.0014": (
        "exclude_abstract",
        "abstract",
        "Privacy essay. Anthropomorphism is discussed as an over-trust risk, not as cues.",
    ),
    "https://doi.org/10.1093/idpl/ipae018": (
        "exclude_abstract",
        "abstract",
        "Legal commentary on automation bias. Human-like answers are a premise, not the analysis.",
    ),
    "https://doi.org/10.1016/j.actpsy.2025.105791": (
        "exclude_abstract",
        "abstract",
        "Self-efficacy and acceptance survey. No linguistic cue analysis.",
    ),
    "https://doi.org/10.3390/electronics14183624": (
        "exclude_abstract",
        "abstract",
        "Machinery safety evaluation. Anthropomorphized here means simulated reasoning, not communication cues.",
    ),
    "https://doi.org/10.55549/epess.1412832": (
        "exclude_abstract",
        "abstract",
        "Research-agenda matrix for conversational marketing. No linguistic cue analysis.",
    ),
    "https://doi.org/10.1016/j.ijinfomgt.2026.103072": (
        "retain_for_abstract",
        "retrieved",
        "OpenAlex abstract field is empty. Still unread.",
    ),
    "https://doi.org/10.1080/10447318.2024.2375686": (
        "exclude_abstract",
        "abstract",
        "Adoption survey. Anthropomorphism is a predictor, not a cue analysis.",
    ),
    "https://doi.org/10.1080/14778238.2025.2555856": (
        "exclude_abstract",
        "abstract",
        "Experiment on avatar anthropomorphism and employee engagement. Visual design, not textual cues.",
    ),
    "https://doi.org/10.1109/tcss.2025.3556397": (
        "exclude_abstract",
        "abstract",
        "Personalized travel generation. Anthropomorphic here means user-like plans, not communication cues.",
    ),
    "https://doi.org/10.1080/10447318.2024.2376370": (
        "exclude_abstract",
        "abstract",
        "Discontinuance survey. Perceived anthropomorphism is a rating, not a cue analysis.",
    ),
    "https://doi.org/10.18653/v1/2026.acl-long.118": (
        "exclude_abstract",
        "abstract",
        "Position paper on anthropomorphic words in the LLM research literature, not cues in model output.",
    ),
    "https://doi.org/10.48550/arxiv.2408.03945": (
        "exclude_abstract",
        "abstract",
        "Discussion of anthropomorphizing tutors in education. No linguistic cue analysis.",
    ),
    "https://doi.org/10.1016/j.ijinfomgt.2025.102996": (
        "retain_for_abstract",
        "retrieved",
        "OpenAlex abstract field is empty. Title names politeness, so this stays queued.",
    ),
    "https://doi.org/10.48550/arxiv.2305.14784": (
        "exclude_duplicate",
        "abstract",
        "Duplicate of https://doi.org/10.18653/v1/2023.nllp-1.1.",
    ),
    "https://doi.org/10.15637/jlecon.2294": (
        "exclude_abstract",
        "abstract",
        "Marketing framework for generative AI and anthropomorphism. No linguistic cue analysis.",
    ),
    "https://doi.org/10.1609/aies.v7i1.31613": (
        "retain_for_full_text",
        "abstract",
        "Maps anthropomorphic design features of conversational agents and their risks. Full text needed. Not an inclusion.",
    ),
    "https://doi.org/10.1344/der.2024.45.106-114": (
        "exclude_abstract",
        "abstract",
        "Teachers' views of ChatGPT in communication courses. No cue analysis.",
    ),
    "https://doi.org/10.5281/zenodo.8253308": (
        "exclude_abstract",
        "abstract",
        "Marketing review of anthropomorphic conversational agents. No linguistic cue analysis.",
    ),
    "https://doi.org/10.1007/s11023-024-09667-z": (
        "exclude_abstract",
        "abstract",
        "Theological argument that LLMs personify past speech. No linguistic cue analysis.",
    ),
    "https://doi.org/10.1186/s13040-025-00458-5": (
        "exclude_abstract",
        "abstract",
        "Clinical-trial screening pipeline. Anthropomorphized names a prompting strategy, not a cue analysis.",
    ),
    "https://doi.org/10.21203/rs.3.rs-9224936/v1": (
        "retain_for_full_text",
        "abstract",
        "Scoping review of anthropomorphizing LLM chatbots. OpenAlex abstract is empty. Full text needed. Not an inclusion.",
    ),
    "https://doi.org/10.31234/osf.io/uqxcb_v1": (
        "exclude_duplicate",
        "abstract",
        "Duplicate of https://doi.org/10.1177/25152459251357566.",
    ),
    "https://doi.org/10.1007/978-981-96-4016-4_10": (
        "retain_for_abstract",
        "retrieved",
        "OpenAlex abstract field is empty. Still unread.",
    ),
    "https://doi.org/10.1093/9780198945215.003.0071": (
        "exclude_abstract",
        "abstract",
        "Philosophical argument against treating LLMs as collaborators. No linguistic cue analysis.",
    ),
    "https://doi.org/10.1080/10447318.2025.2544006": (
        "exclude_abstract",
        "abstract",
        "Survey of dependence and fear. Perceived anthropomorphism is a rating, not a cue analysis.",
    ),
    "https://doi.org/10.3390/electronics14061210": (
        "exclude_abstract",
        "abstract",
        "Compares search, an LLM, and a NAO robot for retrieval. Robot appearance, not textual cues.",
    ),
    "https://doi.org/10.1186/s12888-026-08288-3": (
        "retain_for_full_text",
        "abstract",
        "Case report. The abstract names second-person dialogue, repeated keywords, and typographical emphasis as the features the user treated as signals. Full text needed. Not an inclusion.",
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
