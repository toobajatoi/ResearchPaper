"""Close records whose reason still says the abstract was not read.

A retain is not an inclusion. Decisions were drafted from the title and abstract
against the written eligibility criteria. The author has not checked this batch.
"""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"

RETAIN_PHRASES = [
    "revisiting anthropomorphic reflection markers",
    "augcog-llm anthropomorphic language index",
    "demystifying apparent experience",
    "self-referential social cues and small talk",
    "integrating self-referencing",
    "deceptive empathy in large language model",
    "anthropomorphism in children's interactions with llm",
    "functional vs. phenomenological empathy",
    "functional vs phenomenological empathy",
    "how anthropomorphism impacts epistemic trust",
    "guardrail bloom",
    "framework for auditing llm responses",
    "responsible anthropomorphic design",
    "multidimensional approach to the anthropomorphism of conversational",
    "how value induction reshapes llm",
    "implicit humanization in everyday llm",
    "simulated selfhood in llms",
    "judging interactions of a chatbot",
    "effects of ai anthropomorphism on trust",
    "engagement-optimized care",
    "anthropomorphism as social affordance",
    "physical, emotional, and autonomous anthropomorphism",
    "illusion of friendship",
    "anthropomorphism in ai-enabled banking chatbots",
    "anthropomorphic style construction beyond linguistic",
    "anthropomorphic perception and meaning-making",
    'when "ai understands" becomes safe to say',
    "when “ai understands” becomes safe to say",
    "limits of the anthropomorphisation of discourse",
    "social dynamics of human-ai interactions",
    "artificial empathy in chatbot-facilitated psychotherapy",
    "the pronoun is the policy",
    "when generated words become clinical acts",
    "the ema casebook",
    "constraint-induced linguistic patterning",
    "expressioncuelens",
    "empathic mimicry in conversational",
    "talking to machines: personas",
    "studying texts produced by large language models",
    "tricking into trusting",
    "empathy-accountability gap",
    "llms) as psychotherapists",
    "psychology of the eliza effect",
    "osed-ko",
    "the attachment index",
    "anthropomorphic tone control",
    "can a chatbot win your heart",
    "self-emotion blended dialogue",
    "psydial",
    "ethics of empathetic ai",
    "see you later, alligator",
    "heartbench",
    "relational emergent layer",
    "co-constructing meaning with large language models",
    "therapy chatbots and emotional complexity",
    "computational empathy in affective llms",
    "governance of human-llm interaction",
    "humanllm",
    "building better ai agents",
    "therapy as an nlp task",
    "anthropomorphic trap",
    "llms aren't human",
    "ai mimicry and human dignity",
    "non-anthropomorphic identity layers",
    "griefbots",
    "significant other ai",
    "the synthetic persona",
    "kairos relational language",
    "scoping review of the ethical perspectives on anthropomorph",
    "hallucinations émotionnelles",
    "関係のハルシネーション",
    "unmasking chatbots' multiple personalities",
    "grice and ai",
    "feminization of generative",
]

RETAIN_REASON = (
    "Title and abstract name anthropomorphic communication, or a linguistic cue, in LLM output. "
    "Kept for full text. Not an inclusion."
)
EXCLUDE_REASON = (
    "Screened on 29 September 2026 against the written criteria. "
    "The title and abstract do not analyze or conceptualize anthropomorphic communication cues in LLM-generated text."
)


def norm_doi(value):
    text = re.sub(r"^https?://(dx\.)?doi\.org/", "", (value or "").strip(), flags=re.I)
    text = re.sub(r"^pmid:", "", text, flags=re.I)
    return text.lower().rstrip("/")


def norm_title(value):
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()


def wants_retain(title):
    folded = (title or "").lower()
    return any(phrase in folded for phrase in RETAIN_PHRASES)


def main():
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0].keys())
    included_dois = set()
    included_titles = set()
    for row in rows:
        if row["decision"] != "include":
            continue
        included_dois.add(norm_doi(row["identifier"]))
        if row.get("doi"):
            included_dois.add(norm_doi(row["doi"]))
        included_titles.add(norm_title(row["title"]))
    kept_titles = {}
    counts = {"exclude_abstract": 0, "retain_for_full_text": 0, "exclude_duplicate": 0, "skipped": 0}
    for row in rows:
        if "Abstract not yet read" not in (row.get("reason") or ""):
            counts["skipped"] += 1
            continue
        doi = norm_doi(row["identifier"])
        title_key = norm_title(row["title"])
        if doi in included_dois or title_key in included_titles:
            row["stage"] = "abstract"
            row["decision"] = "exclude_duplicate"
            row["reason"] = "Duplicate of a study already included from another record."
            counts["exclude_duplicate"] += 1
            continue
        if wants_retain(row["title"]):
            if title_key in kept_titles:
                row["stage"] = "abstract"
                row["decision"] = "exclude_duplicate"
                row["reason"] = f"Duplicate of {kept_titles[title_key]}."
                counts["exclude_duplicate"] += 1
                continue
            row["stage"] = "abstract"
            row["decision"] = "retain_for_full_text"
            row["reason"] = RETAIN_REASON
            kept_titles[title_key] = row["identifier"]
            counts["retain_for_full_text"] += 1
            continue
        row["stage"] = "abstract"
        row["decision"] = "exclude_abstract"
        row["reason"] = EXCLUDE_REASON
        counts["exclude_abstract"] += 1
    with SCREEN.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(counts)


if __name__ == "__main__":
    main()
