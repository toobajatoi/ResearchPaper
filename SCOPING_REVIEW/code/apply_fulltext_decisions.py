"""Record full-text decisions for the 46 PMC papers.

Batch files are the first read of the passage extracts. OVERRIDES replace
decisions that were checked against the XML after that read.
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / "data" / "fulltext" / "decisions"
SCREEN = ROOT / "data" / "screening.csv"

OVERRIDES = {
    "42726769": {
        "decision": "include",
        "tag": "perception-plus-cues",
        "reason": "Scenario experiment on simulated AI live-stream hosts operationalizes social dialogue cues as second- versus third-person pronouns, emotional-word density, and active empathy versus passive retrieval, alongside visual and voice cues.",
        "system": "Simulated AI live-stream host (TTS; generative status not established)",
        "cues": "pronoun person; emotional word density; active empathy vs passive retrieval; visual appearance; TTS prosody",
        "language": "not stated",
        "quote": "Social Dialogue Cues Pronoun Usage Second-person Dominant Third-person Dominant Emotional Word Density > 15% < 2% Response Strategy Active Empathy Passive Retrieval",
    },
    "42651447": {
        "decision": "include",
        "tag": "perception-plus-cues",
        "reason": "Appendix B scripts operationalize low, medium, and high chatbot anthropomorphism with greetings, identity labels, first-person recommendation phrasing, empathy and reassurance, and self-disclosure. The paper states that the exact Chinese wordings are archived on OSF.",
        "system": "Scripted financial, health, and e-commerce advisor chatbot",
        "cues": "greeting; personal name vs system label; first-person recommendation phrasing; empathy and reassurance; self-disclosure",
        "language": "Chinese wordings stated as archived; reporting language English",
        "quote": "Hello, I’m Li Wei, your personal advisor. Decisions like this can feel stressful—I’ll walk through it with you step by step.",
    },
    "42510216": {
        "decision": "include",
        "tag": "perception-plus-cues",
        "reason": "Scenario experiment contrasts a high-empathy government-chatbot script (“I understand you may need your ID urgently,” plus emoticons) with a procedural low-empathy script. The stimuli are researcher-written scripts; a generative model is not established.",
        "system": "Scripted government service chatbot",
        "cues": "perspective-taking acknowledgment; emoticon; procedural versus emotionally responsive wording",
        "language": "not stated in the checked passage; authors at a Chinese university",
        "quote": "It proactively acknowledged users’ urgent needs and provided more emotionally resonant responses (e.g., “I understand you may need your ID urgently”)",
    },
    "41060458": {
        "decision": "include",
        "tag": "review",
        "reason": "Review section on anthropomorphizing chatbots catalogs communicative steps: human name, informal language, verbal cues, slowed replies, humor, personality matching, self-introduction, addressing the user by name, repeating the user’s answer, and typos as a humanness penalty.",
        "system": "AI chatbots, including generative chatbots, as reviewed",
        "cues": "human name; informal language; verbal anthropomorphic cues; humor; self-introduction; address by name; repetition; typos",
        "language": "not stated",
        "quote": "The use of a human name and informal language style increases the anthropomorphism of a chatbot.",
    },
    "38957452": {
        "decision": "include",
        "tag": "conceptual",
        "reason": "The emotional-expression section, missing from the first extract, describes ChatGPT identifying distress, offering empathic replies, and using congratulatory and supportive phrasing, with examples.",
        "system": "ChatGPT",
        "cues": "empathic response to distress; congratulatory phrasing; emotional support",
        "language": "English examples",
        "quote": "ChatGPT is equipped to identify expressions of negative feelings and offer empathetic responses.",
    },
    "40123640": {
        "decision": "include",
        "tag": "conceptual",
        "reason": "Perspective paper argues that humanlike language and conversation are agentive cues that invite anthropomorphism of LLMs, via hyperactive agency detection. It does not inventory finer linguistic features.",
        "system": "Large language models (ChatGPT, Gemini, LaMDA discussed)",
        "cues": "humanlike language and conversational contingency as an agentive cue",
        "language": "not stated",
        "quote": "Mimicking humanlike language and conversation is the cornerstone of what LLMs are designed to accomplish.",
    },
    "39661968": {
        "decision": "include",
        "tag": "review",
        "reason": "Systematic review of 12 studies that evaluated empathy in LLM outputs. It charts models, rating methods, and output limitations such as repetitive empathic phrases and overly long replies. Most included measures are global ratings rather than linguistic feature codes.",
        "system": "ChatGPT-3.5, GPT-4, LLaMA, and fine-tuned chatbots, as reviewed",
        "cues": "empathic phrases; emotionally supportive responses; response length",
        "language": "English-language publications reviewed",
        "quote": "Limitations were noted, including repetitive use of empathic phrases, difficulty following initial instructions, overly lengthy responses",
    },
    "39631034": {
        "decision": "exclude_full_text",
        "tag": "",
        "reason": "The paper analyzes anthropomorphic language in scholarly and media reporting about LaMDA and other LLMs, and argues against consciousness claims. It does not analyze communicative cues in model-generated text.",
        "system": "LaMDA and other LLMs, discussed as the object of reporting",
        "cues": "none in model output; anthropomorphic wording in abstracts and journalism",
        "language": "English",
        "quote": "We argue that describing LaMDA (or any other LLM) as a conscious being is a part of the wider problem of anthropomorphic language in scholarly and journalistic reporting.",
    },
}


def load_batches():
    rows = []
    for path in sorted(DECISIONS.glob("batch_*.json")):
        rows.extend(json.loads(path.read_text(encoding="utf-8")))
    return rows


def main():
    merged = []
    for row in load_batches():
        override = OVERRIDES.get(row["pmid"])
        if override:
            row = {**row, **override, "checked_against": "pmc_xml"}
        else:
            row = {**row, "checked_against": "passage_extract"}
        merged.append(row)
    extra_ids = {"40123640", "39661968", "39631034"}
    have = {row["pmid"] for row in merged}
    missing = extra_ids - have
    if missing:
        avail = {
            item["pmid"]: item
            for item in json.loads((ROOT / "data" / "fulltext" / "availability.json").read_text(encoding="utf-8"))
        }
        for pmid in sorted(missing):
            meta = avail[pmid]
            merged.append(
                {
                    "pmid": pmid,
                    "pmcid": meta["pmcid"],
                    "title": meta["title"],
                    **OVERRIDES[pmid],
                    "checked_against": "pmc_xml",
                }
            )
    out = DECISIONS / "final_decisions.json"
    out.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
    by_pmid = {row["pmid"]: row for row in merged}
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        records = list(reader)
    updated = 0
    for record in records:
        pmid = record["identifier"].replace("PMID:", "")
        decision = by_pmid.get(pmid)
        if not decision:
            continue
        if not record["source"].startswith("PubMed"):
            continue
        record["stage"] = "full_text"
        record["decision"] = decision["decision"]
        tag = decision.get("tag") or ""
        reason = decision["reason"]
        if tag:
            reason = f"[{tag}] {reason}"
        record["reason"] = reason
        updated += 1
    with SCREEN.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    include = sum(1 for row in merged if row["decision"] == "include")
    exclude = sum(1 for row in merged if row["decision"] == "exclude_full_text")
    other = len(merged) - include - exclude
    print("records", len(merged), "include", include, "exclude", exclude, "other", other, "csv_updated", updated)


if __name__ == "__main__":
    main()
