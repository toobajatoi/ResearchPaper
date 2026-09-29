"""Record one batch of OpenAlex abstract decisions. Does not mark studies included."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"

DECISIONS = {
    "https://doi.org/10.1145/3774779": (
        "exclude_abstract",
        "abstract",
        "Compares embodiment and theory-of-mind prompting on trust and anthropomorphism ratings. No linguistic cue analysis.",
    ),
    "https://doi.org/10.48550/arxiv.2405.13803": (
        "retain_for_full_text",
        "abstract",
        "Compares an LLM well-being agent with persona and conversational design against one without. Full text needed. Not an inclusion.",
    ),
    "https://doi.org/10.1109/cscwd61410.2024.10580436": (
        "exclude_abstract",
        "abstract",
        "Personality prompts are used to raise task scores. Not an analysis of wording.",
    ),
    "https://doi.org/10.2196/preprints.55988": (
        "exclude_duplicate",
        "abstract",
        "Duplicate of https://doi.org/10.2196/55988.",
    ),
    "https://doi.org/10.1093/clinchem/hvad129": (
        "exclude_abstract",
        "abstract",
        "Clinical-chemistry commentary. Human-like conversation is a premise, not the analysis.",
    ),
    "https://doi.org/10.1080/08874417.2025.2566197": (
        "exclude_abstract",
        "abstract",
        "Continued-use survey. Anthropomorphism is an adoption factor, not a cue analysis.",
    ),
    "https://doi.org/10.1016/j.techsoc.2025.103015": (
        "retain_for_abstract",
        "retrieved",
        "OpenAlex abstract field is empty. Still unread.",
    ),
    "https://doi.org/10.3389/frai.2026.1681525": (
        "exclude_abstract",
        "abstract",
        "Systems-theory reframing that avoids attributing agency. No linguistic cue analysis.",
    ),
    "https://doi.org/10.1038/s41598-025-18906-x": (
        "exclude_abstract",
        "abstract",
        "Use-intention survey. Empathy and warmth are ratings, not an analysis of wording.",
    ),
    "https://doi.org/10.1007/978-3-031-93736-1_24": (
        "retain_for_abstract",
        "retrieved",
        "OpenAlex abstract field is empty. Title names anthropomorphic design, so this stays queued.",
    ),
    "https://doi.org/10.23947/2414-1143-2025-11-4-19-28": (
        "retain_for_full_text",
        "abstract",
        "Students rate chatbots whose strategies follow Brown and Levinson politeness theory. Full text needed to confirm the systems are LLMs. Not an inclusion.",
    ),
    "https://doi.org/10.4324/9781003676423-6": (
        "retain_for_full_text",
        "abstract",
        "Chapter on the Eliza effect and multimodal cues in LLM interfaces. Full text needed. Not an inclusion.",
    ),
    "https://doi.org/10.1145/3715336.3735700": (
        "retain_for_full_text",
        "abstract",
        "Compares a personified LLM agent with a non-personified assistant. Full text needed to see if personification is linguistic. Not an inclusion.",
    ),
    "https://doi.org/10.1108/apjba-03-2025-0172": (
        "exclude_abstract",
        "abstract",
        "Brand-anthropomorphism survey. Not cues in model text.",
    ),
    "https://doi.org/10.1007/978-981-95-0211-0_29": (
        "retain_for_abstract",
        "retrieved",
        "OpenAlex abstract field is empty. Still unread.",
    ),
    "https://doi.org/10.1177/02666669241306735": (
        "exclude_abstract",
        "abstract",
        "Platform-switching survey. Perceived anthropomorphism is a pull factor, not a cue analysis.",
    ),
    "https://doi.org/10.48550/arxiv.2409.02244": (
        "retain_for_full_text",
        "abstract",
        "Compares LLM and human peer-counselor behaviors in multi-turn CBT, including empathetic responses. Full text needed. Not an inclusion.",
    ),
    "https://doi.org/10.1080/10447318.2025.2498486": (
        "exclude_abstract",
        "abstract",
        "Attachment survey. Anthropomorphic features are not specified as wording.",
    ),
    "https://doi.org/10.1049/csy2.70037": (
        "exclude_abstract",
        "abstract",
        "Guide-robot system. Textual cues are not the object.",
    ),
    "https://doi.org/10.3390/su18115759": (
        "exclude_abstract",
        "abstract",
        "Motivation survey. Anthropomorphic perception is a mediator, not a cue analysis.",
    ),
    "https://doi.org/10.48550/arxiv.2409.18996": (
        "exclude_abstract",
        "abstract",
        "Survey of cross-modal reasoning. Anthropomorphic here means human-like sensing, not communication cues.",
    ),
    "https://doi.org/10.48550/arxiv.2601.17096": (
        "exclude_abstract",
        "abstract",
        "Cultural-alignment experiment. Anthropomorphism names the frameworks the paper rejects, not cues in the text.",
    ),
    "https://doi.org/10.1111/jlse.12141": (
        "exclude_abstract",
        "abstract",
        "Legal commentary on ChatGPT. No linguistic cue analysis.",
    ),
    "https://doi.org/10.1109/vl/hcc60511.2024.00021": (
        "exclude_abstract",
        "abstract",
        "Ethics of interface mystification. No linguistic cue inventory.",
    ),
    "https://doi.org/10.1145/3772318.3790316": (
        "exclude_abstract",
        "abstract",
        "Public discourse about LLMs, not cues in model output.",
    ),
    "https://doi.org/10.1108/jhti-02-2025-0229": (
        "exclude_abstract",
        "abstract",
        "Travel-planning survey. AI anthropomorphism is a subjective norm, not a cue analysis.",
    ),
    "https://doi.org/10.5281/zenodo.18357935": (
        "exclude_abstract",
        "abstract",
        "Epistemic argument about consciousness judgments from text. No linguistic cue analysis.",
    ),
    "https://doi.org/10.2139/ssrn.5037486": (
        "exclude_duplicate",
        "abstract",
        "Duplicate of https://doi.org/10.1016/j.techsoc.2025.102995.",
    ),
    "https://doi.org/10.3389/fpsyg.2025.1662331": (
        "exclude_abstract",
        "abstract",
        "Exercise-motivation survey. Anthropomorphism is a scale score, not a cue analysis.",
    ),
    "https://doi.org/10.3390/jtaer20020099": (
        "exclude_abstract",
        "abstract",
        "Disclosure survey. Empathy and social presence are affordance ratings, not an analysis of wording.",
    ),
    "https://doi.org/10.1177/00472875261441570": (
        "exclude_abstract",
        "abstract",
        "Tourism survey. Anthropomorphic features are not specified as wording.",
    ),
    "https://doi.org/10.3389/fpubh.2026.1816917": (
        "exclude_abstract",
        "abstract",
        "Narrative review of problematic chatbot use. Anthropomorphism is a proposed risk factor, not a cue analysis.",
    ),
    "https://doi.org/10.48550/arxiv.2508.08101": (
        "exclude_duplicate",
        "abstract",
        "Duplicate of https://doi.org/10.1080/10447318.2026.2661827.",
    ),
    "https://doi.org/10.1080/17439884.2025.2532550": (
        "exclude_abstract",
        "abstract",
        "Classroom activity on co-creating with generative AI. No linguistic cue analysis.",
    ),
    "https://doi.org/10.1101/2024.05.02.24306753": (
        "exclude_abstract",
        "abstract",
        "Medical-education patient simulation. No linguistic cue analysis.",
    ),
    "https://doi.org/10.1186/s12888-025-07671-w": (
        "exclude_abstract",
        "abstract",
        "User accounts of agency in AI therapy. No linguistic cue analysis.",
    ),
    "https://doi.org/10.3389/feduc.2025.1649747": (
        "exclude_abstract",
        "abstract",
        "Acceptance of anthropomorphic features, including voice. Textual cues are not the object.",
    ),
    "https://doi.org/10.1109/tlt.2025.3560032": (
        "exclude_abstract",
        "abstract",
        "Appearance of digital teachers. Visual, not textual cues.",
    ),
    "https://doi.org/10.3390/info15110679": (
        "exclude_abstract",
        "abstract",
        "Psychometric trait scores of in-vehicle models. Not an analysis of wording.",
    ),
    "https://doi.org/10.5772/intechopen.1010894": (
        "exclude_abstract",
        "abstract",
        "Marketing overview of human-like conversational tools. No linguistic cue analysis.",
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
