"""Export the narrowed OpenAlex query. Does not resume the loose Search 1 pull."""

import json
from pathlib import Path

import openalex_search as ox

QUERY = (
    '(anthropomorphism OR anthropomorphic OR anthropomorphised OR anthropomorphized) '
    'AND ("large language model" OR "large language models" OR LLM OR LLMs '
    'OR "generative AI" OR "generative artificial intelligence")'
)
NAME = "search1_narrow_anthropomorph_llm"


def main():
    reported, rows = ox.run_query(NAME, QUERY)
    ox.write_csv(NAME, rows)
    summary = {
        "search_date": ox.SEARCH_DATE,
        "source": "OpenAlex",
        "field": "title_and_abstract.search",
        "name": NAME,
        "query": QUERY,
        "reported_count": reported,
        "rows_saved": len(rows),
        "note": (
            "Replaces Scopus and Web of Science as the multidisciplinary index. "
            "The earlier loose query counted 11245 because it also matched "
            "human-like, social presence, and chatbot. This query keeps title "
            "and abstract, and requires an anthropomorphism stem plus an LLM "
            "or generative-AI term."
        ),
    }
    path = ox.OUT / "search1_narrow_summary.json"
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("saved", len(rows), "reported", reported)


if __name__ == "__main__":
    main()
