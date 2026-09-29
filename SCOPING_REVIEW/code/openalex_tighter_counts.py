"""Count tighter OpenAlex variants. Records are not exported."""

import json
import urllib.parse
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "openalex" / "tighter_counts_2026-09-29.json"

ANTH = '(anthropomorphism OR anthropomorphic OR anthropomorphised OR anthropomorphized)'
LLM = (
    '("large language model" OR "large language models" OR LLM OR LLMs '
    'OR "generative AI" OR "generative artificial intelligence")'
)


def count(field, query):
    filt = (
        f"{field}:{query},"
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
    jobs = {
        "title_abstract_anthropomorph_and_llm": ("title_and_abstract.search", f"{ANTH} AND {LLM}"),
        "title_only_anthropomorph_and_llm": ("title.search", f"{ANTH} AND {LLM}"),
        "title_only_blockA_loose_not_run": ("title.search", f"{ANTH}"),
    }
    rows = {}
    for name, (field, query) in jobs.items():
        rows[name] = {"field": field, "count": count(field, query), "query": query}
        print(name, rows[name]["count"], flush=True)
    OUT.write_text(json.dumps({"search_date": "2026-09-29", "counts": rows}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
