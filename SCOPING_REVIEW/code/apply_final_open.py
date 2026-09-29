import csv
from pathlib import Path

SCREEN = Path(__file__).resolve().parents[1] / "data" / "screening.csv"

INCLUDE = {
    "https://doi.org/10.48550/arxiv.2607.18250": "Full text read on 30 September 2026. Systematic review of 35 studies. Drivers of children's anthropomorphism of LLM chatbots include human-like persona construction, adaptive scaffolding, supportive companionship, and non-human embodied design.",
}
EXCLUDE_FULL = {
    "https://doi.org/10.48550/arxiv.2601.10198": "Full text read on 30 September 2026. HumanLLM scores fidelity to psychological patterns in role-play scenarios. The object is cognitive-pattern simulation, not anthropomorphic communication cues.",
}
EXCLUDE_ABSTRACT = {
    "https://doi.org/10.1186/s12888-026-08288-3": "Abstract on file. Case report of a psychotic episode during ChatGPT use. The dialogue is not analyzed as anthropomorphic cues.",
    "https://doi.org/10.1007/s00146-024-02108-6": "Abstract on file. ChatGPT was prompted to draw images of itself. The object is visual self-representation.",
    "https://doi.org/10.4324/9781003676423-6": "Abstract on file. Book chapter on AI aesthetics and fictional imaginaries of conscious machines. Not an analysis of linguistic cues in LLM output.",
    "https://doi.org/10.1145/3715336.3735700": "Abstract on file. Lab study of a personified appliance agent versus a non-personified assistant. Linguistic features are not analyzed.",
    "https://openalex.org/W7112105913": "Record is an OSF preregistration, not a completed analysis of cues.",
    "https://doi.org/10.17605/osf.io/ez6t7": "Abstract on file. The experiment uses a pseudo-LLM, which is outside the LLM-output set.",
    "https://doi.org/10.4018/979-8-2600-2977-0.ch008": "Abstract on file. Chapter on synthetic virtual influencers in marketing. LLM communication cues are not the object.",
    "https://doi.org/10.63332/joph.v4i3.3243": "Abstract on file. Interviews about personas users attribute to generative AI. Model messages are not analyzed.",
    "https://doi.org/10.32920/ifmj.v5i1-2.2427": "Abstract on file. Autoethnography of Midjourney image generation and grief. Not an analysis of LLM dialogue cues.",
}
DUPLICATE = {
    "https://openalex.org/W7124513812": "Duplicate of https://doi.org/10.1145/3805689.3812324. The DOI record stays in the full-text queue.",
}

rows = list(csv.DictReader(SCREEN.open(encoding="utf-8")))
fields = list(rows[0].keys())
counts = {k: 0 for k in ("include", "full", "abs", "dup")}
for row in rows:
    ident = row["identifier"]
    if row["decision"] != "retain_for_full_text" and ident not in DUPLICATE:
        continue
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
print(counts)
from collections import Counter
print(Counter(r["decision"] for r in rows))
with SCREEN.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
