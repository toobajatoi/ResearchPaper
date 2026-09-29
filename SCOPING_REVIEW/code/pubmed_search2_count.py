"""PubMed Search 2 and CASA-extra counts. Saves ids only after the count is known."""

import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "pubmed"
DATE = '("2020/01/01"[dp] : "2026/09/29"[dp])'

BLOCK_A = (
    '(anthropomorph*[tiab] OR "human-like"[tiab] OR "human like"[tiab] OR humanlike[tiab] '
    'OR "human-likeness"[tiab] OR "human likeness"[tiab] OR "social cue*"[tiab] '
    'OR "social presence"[tiab] OR "computers are social actors"[tiab] '
    'OR "human-machine communication"[tiab] OR "human machine communication"[tiab])'
)
BLOCK_B = (
    '("large language model*"[tiab] OR "language model*"[tiab] OR LLM[tiab] OR LLMs[tiab] '
    'OR "generative AI"[tiab] OR "generative artificial intelligence"[tiab] OR "generative model*"[tiab] '
    'OR chatbot*[tiab] OR "conversational AI"[tiab] OR "conversational agent*"[tiab] '
    'OR "dialogue system*"[tiab] OR "dialog system*"[tiab] OR "AI assistant*"[tiab] '
    'OR "artificial intelligence assistant*"[tiab] OR "conversational assistant*"[tiab] '
    'OR "machine-generated"[tiab] OR "machine generated"[tiab] OR "AI-generated"[tiab] '
    'OR "text generation"[tiab] OR "language technolog*"[tiab])'
)
BLOCK_C = (
    '(Urdu[tiab] OR Hindi[tiab] OR Arabic[tiab] OR Persian[tiab] OR Farsi[tiab] OR Punjabi[tiab] '
    'OR Bengali[tiab] OR Bangla[tiab] OR Chinese[tiab] OR Mandarin[tiab] OR Cantonese[tiab] '
    'OR Japanese[tiab] OR Korean[tiab] OR Spanish[tiab] OR French[tiab] OR multilingual[tiab] '
    'OR "cross-lingual"[tiab] OR crosslingual[tiab] OR "cross-linguistic"[tiab] OR crosslinguistic[tiab] '
    'OR "non-English"[tiab] OR "low-resource"[tiab] OR "South Asian"[tiab] OR "Global South"[tiab] '
    'OR "cultural context*"[tiab] OR "linguistic variation"[tiab] OR "linguistic difference*"[tiab])'
)
BLOCK_D = (
    '(honorific*[tiab] OR "grammatical gender"[tiab] OR "address form*"[tiab] OR "kinship term*"[tiab] '
    'OR politeness[tiab] OR "speech act*"[tiab] OR "person reference"[tiab] OR "self-reference"[tiab] '
    'OR "first person"[tiab] OR "first-person"[tiab] OR pronoun*[tiab])'
)
SEARCH_2 = f"{BLOCK_C} AND {BLOCK_B} AND ({BLOCK_A} OR {BLOCK_D}) AND {DATE}"
CASA = (
    '(CASA[tiab] AND (anthropomorph*[tiab] OR chatbot*[tiab] OR "language model*"[tiab] '
    f'OR LLM[tiab] OR LLMs[tiab])) AND {DATE}'
)


def esearch(term, retmax):
    data = urllib.parse.urlencode(
        {
            "db": "pubmed",
            "term": term,
            "retmode": "json",
            "retmax": str(retmax),
            "retstart": "0",
        }
    ).encode()
    req = urllib.request.Request(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
        data=data,
        headers={"User-Agent": "HMC-scoping-review"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.load(resp)


def main():
    for name, term in (("search2", SEARCH_2), ("casa_extra", CASA)):
        payload = esearch(term, 0)
        result = payload["esearchresult"]
        count = int(result["count"])
        print(name, count, flush=True)
        record = {
            "search_date": "2026-09-29",
            "name": name,
            "count": count,
            "querytranslation": result.get("querytranslation"),
            "term": term,
        }
        (OUT / f"{name}_count.json").write_text(json.dumps(record, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
