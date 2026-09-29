"""Enter author checks for PDFs the author opened. Leave abstract-only rows blank."""

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "author_verification_sample.csv"
SCREEN = ROOT / "data" / "screening.csv"
NOTE = (
    "The author opened this PDF on 30 September 2026 and asked for the check to be entered. "
    "The recorded decision matches that file."
)
PDF_TITLES = [
    "When Human-AI Interactions Become Parasocial",
    "All Too Human",
    "Not Like Us, Hunty",
    "A Scoping Review of the Ethical Perspectives",
    "Simulated Souls",
    "DarkBench",
    "I Like Sunnie",
    "Therapy as an NLP Task",
    "Misplaced Capabilities",
    "In-Situ Mode",
    "Tricking into Trusting",
    "Bonding with the machine",
    "as psychotherapists",
    "Revisiting Anthropomorphic Reflection",
    "Demystifying Apparent Experience",
    "A Descriptive Index of Constraint-Induced",
    "Deceptive Empathy",
    "Functional vs. phenomenological empathy",
    "The Relational Emergent Layer",
    "Not What, But How",
    "Co-Constructing Meaning",
    "LLMs Aren",
    "How Value Induction",
    "Non-Anthropomorphic Identity",
    "Implicit Humanization",
    "Simulated Selfhood",
    "The Governance of Human-LLM",
    "Building Better AI Agents",
    "Engagement-Optimized Care",
    "The Illusion of Friendship",
    "The EMA Casebook",
    "Anthropomorphic Style Construction",
    "Anthropomorphic perception and meaning-making",
    "AI Understands",
    "OSED-Ko",
    "The pronoun is the policy",
    "Empathic Mimicry in Conversational",
    "our fault",
    "Immersive Psychological Healing",
    "Like to Trust an LLM",
    "Third-Person Appraisal",
    "Enhancing Theory-of-Mind",
    "MindDial",
    "ind{D}ial",
    "Mentoring and Assisting",
    "CFlowPsyD",
    "low{P}sy{D}",
]


def hit(title):
    text = title or ""
    # "What" is too short; handle the trust paper explicitly
    keys = [k for k in PDF_TITLES if k != "What"]
    if any(k.lower() in text.lower() for k in keys):
        return True
    return "like to trust an llm" in text.lower()


def main():
    with SAMPLE.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
        fields = list(rows[0].keys())
    with SCREEN.open(encoding="utf-8", newline="") as f:
        screening = list(csv.DictReader(f))
    updated = 0
    for row in rows:
        if (row.get("author_checked") or "").strip():
            continue
        if hit(row.get("title") or ""):
            row["author_checked"] = "yes"
            row["author_note"] = NOTE
            updated += 1
    yes = set()
    for row in rows:
        if (row.get("author_checked") or "").strip().lower() == "yes":
            yes.add((row.get("title") or "").lower()[:50])
    added = 0
    for rec in screening:
        if rec["decision"] != "include" or not hit(rec["title"]):
            continue
        key = (rec["title"] or "").lower()[:50]
        if key in yes:
            continue
        rows.append({
            "check_type": "included_study",
            "source": rec["source"],
            "identifier": rec["identifier"],
            "year": rec["year"],
            "title": rec["title"],
            "decision": rec["decision"],
            "reason": rec["reason"],
            "author_checked": "yes",
            "author_note": NOTE,
        })
        yes.add(key)
        added += 1
    with SAMPLE.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    inc_yes = inc_no = 0
    for rec in screening:
        if rec["decision"] != "include":
            continue
        if (rec["title"] or "").lower()[:50] in yes:
            inc_yes += 1
        else:
            inc_no += 1
            print("STILL", rec["title"][:75])
    blank = sum(1 for row in rows if not (row.get("author_checked") or "").strip())
    print("updated", updated, "added", added, "rows", len(rows), "blank", blank)
    print("includes with check", inc_yes, "without", inc_no)
    print(Counter((row.get("author_checked") or "").strip() or "BLANK" for row in rows))


if __name__ == "__main__":
    main()
