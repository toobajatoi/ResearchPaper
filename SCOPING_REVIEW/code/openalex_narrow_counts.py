"""Count narrowed OpenAlex title-and-abstract queries. Does not export records."""

import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "openalex" / "narrow_counts_2026-09-29.json"

A = (
    '(anthropomorphism OR anthropomorphic OR anthropomorphised OR anthropomorphized '
    'OR "human-like" OR "human likeness" OR "social presence" OR "social cues" '
    'OR "computers are social actors" OR "human-machine communication")'
)
LLM_TIGHT = (
    '("large language model" OR "large language models" OR LLM OR LLMs '
    'OR "generative AI" OR "generative artificial intelligence")'
)
LLM_PLUS_LM = (
    '("large language model" OR "large language models" OR LLM OR LLMs '
    'OR "generative AI" OR "generative artificial intelligence" '
    'OR "language model" OR "language models")'
)


def count(query):
    filt = (
        f"title_and_abstract.search:{query},"
        "from_publication_date:2020-01-01,"
        "to_publication_date:2026-09-29"
    )
    params = urllib.parse.urlencode({"filter": filt, "per-page": "1"})
    url = "https://api.openalex.org/works?" + params
    req = urllib.request.Request(url, headers={"User-Agent": "HMC-scoping-review"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.load(resp)
    return data.get("meta", {}).get("count")


def main():
    queries = {
        "A_and_llm_or_generative_ai": f"{A} AND {LLM_TIGHT}",
        "A_and_llm_or_language_model": f"{A} AND {LLM_PLUS_LM}",
    }
    rows = {}
    for name, query in queries.items():
        rows[name] = {"count": count(query), "query": query}
        print(name, rows[name]["count"], flush=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps({"search_date": "2026-09-29", "field": "title_and_abstract.search", "counts": rows}, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
