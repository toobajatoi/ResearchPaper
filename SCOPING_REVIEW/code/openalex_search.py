"""OpenAlex pull for the scoping review.

This is not Scopus, Web of Science, or the ACM Digital Library.
Those require subscriptions this machine does not have.
OpenAlex is an open index used here so the search can start and every
hit can be saved. Counts from this script are OpenAlex counts only.
"""

import csv
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "openalex"
OUT.mkdir(parents=True, exist_ok=True)

SEARCH_DATE = "2026-09-29"
USER_AGENT = "HMC-scoping-review (literature search; contact via project files)"
PER_PAGE = 100

SEARCH_1 = (
    '(anthropomorphism OR anthropomorphic OR anthropomorphised OR anthropomorphized '
    'OR "human-like" OR "human likeness" OR "social presence" OR "social cues" '
    'OR "computers are social actors" OR "human-machine communication") '
    'AND ("large language model" OR "language model" OR LLM OR chatbot '
    'OR "generative AI" OR "conversational AI" OR "conversational agent" '
    'OR "dialogue system" OR "AI assistant" OR "text generation" OR "language technology")'
)

SEARCH_2 = (
    '(Urdu OR Hindi OR Arabic OR Persian OR Farsi OR Punjabi OR Bengali '
    'OR Chinese OR Mandarin OR Japanese OR Korean OR Spanish OR French '
    'OR multilingual OR "cross-lingual" OR "non-English" OR "low-resource" OR "South Asian") '
    'AND ("large language model" OR "language model" OR LLM OR chatbot '
    'OR "generative AI" OR "conversational AI" OR "conversational agent") '
    'AND (anthropomorphism OR anthropomorphic OR "human-like" OR "social presence" '
    'OR honorific OR "grammatical gender" OR politeness OR "kinship" OR pronoun)'
)

CASA = (
    'CASA AND (anthropomorphism OR anthropomorphic OR chatbot OR "language model" OR LLM)'
)

QUERIES = {
    "search1_primary": SEARCH_1,
    "search2_sensitivity": SEARCH_2,
    "casa_extra": CASA,
}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as exc:
            if exc.code != 429 or attempt == 5:
                raise
            time.sleep(5 * (attempt + 1))
    raise RuntimeError("unreachable")


def checkpoint_path(name):
    return OUT / f"{name}_checkpoint.json"


def run_query(name, query):
    filt = (
        f"title_and_abstract.search:{query},"
        f"from_publication_date:2020-01-01,"
        f"to_publication_date:{SEARCH_DATE}"
    )
    path = checkpoint_path(name)
    if path.exists():
        saved = json.loads(path.read_text(encoding="utf-8"))
        rows = saved["rows"]
        cursor = saved["cursor"]
        reported = saved["reported_count"]
        print(f"{name}: resuming at {len(rows)}", flush=True)
    else:
        rows = []
        cursor = "*"
        reported = None
    page = 0
    while cursor:
        params = {
            "filter": filt,
            "per-page": str(PER_PAGE),
            "cursor": cursor,
            "select": ",".join(
                [
                    "id",
                    "doi",
                    "display_name",
                    "publication_year",
                    "publication_date",
                    "type",
                    "language",
                    "authorships",
                    "primary_location",
                    "open_access",
                    "abstract_inverted_index",
                    "ids",
                ]
            ),
        }
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
        try:
            data = get(url)
        except urllib.error.HTTPError as exc:
            if exc.code != 429:
                raise
            print(f"{name}: rate limited at {len(rows)}; waiting 60s", flush=True)
            path.write_text(
                json.dumps(
                    {"reported_count": reported, "cursor": cursor, "rows": rows},
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            time.sleep(60)
            continue
        if reported is None:
            reported = data["meta"]["count"]
            print(f"{name}: reported count {reported}", flush=True)
        batch = data.get("results") or []
        rows.extend(batch)
        page += 1
        cursor = data["meta"].get("next_cursor")
        if not batch:
            cursor = None
        if page % 5 == 0 or not cursor:
            path.write_text(
                json.dumps(
                    {"reported_count": reported, "cursor": cursor, "rows": rows},
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            print(f"{name}: saved {len(rows)}", flush=True)
        time.sleep(1.1)
    raw_path = OUT / f"{name}_raw.json"
    raw_path.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    return reported, rows


def reconstruct_abstract(index):
    if not index:
        return ""
    positions = []
    for word, places in index.items():
        for place in places:
            positions.append((place, word))
    positions.sort()
    return " ".join(word for _, word in positions)


def authors_of(work):
    names = []
    for authorship in work.get("authorships") or []:
        author = authorship.get("author") or {}
        name = author.get("display_name")
        if name:
            names.append(name)
    return "; ".join(names)


def venue_of(work):
    location = work.get("primary_location") or {}
    source = location.get("source") or {}
    return source.get("display_name") or ""


def write_csv(name, rows):
    path = OUT / f"{name}.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "openalex_id",
                "doi",
                "title",
                "year",
                "publication_date",
                "type",
                "language",
                "authors",
                "venue",
                "url",
                "is_oa",
                "abstract",
            ],
        )
        writer.writeheader()
        for work in rows:
            location = work.get("primary_location") or {}
            oa = work.get("open_access") or {}
            writer.writerow(
                {
                    "openalex_id": work.get("id") or "",
                    "doi": work.get("doi") or "",
                    "title": work.get("display_name") or "",
                    "year": work.get("publication_year") or "",
                    "publication_date": work.get("publication_date") or "",
                    "type": work.get("type") or "",
                    "language": work.get("language") or "",
                    "authors": authors_of(work),
                    "venue": venue_of(work),
                    "url": location.get("landing_page_url") or work.get("doi") or work.get("id") or "",
                    "is_oa": oa.get("is_oa"),
                    "abstract": reconstruct_abstract(work.get("abstract_inverted_index")),
                }
            )


def main():
    summary = {"search_date": SEARCH_DATE, "source": "OpenAlex", "queries": {}}
    for name, query in QUERIES.items():
        reported, rows = run_query(name, query)
        write_csv(name, rows)
        summary["queries"][name] = {
            "query": query,
            "reported_count": reported,
            "rows_saved": len(rows),
        }
        print(f"{name}: rows saved {len(rows)}", flush=True)
    (OUT / "search_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
