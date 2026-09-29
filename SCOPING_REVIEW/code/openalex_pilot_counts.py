import json
import time
import urllib.error
import urllib.parse
import urllib.request

QUERIES = [
    "anthropomorphism",
    "anthropomorphism AND chatbot",
    '"large language model" AND anthropomorphism',
    "anthropomorphic language model",
]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "HMC-scoping-review"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as exc:
            if exc.code != 429 or attempt == 4:
                raise
            time.sleep(3 * (attempt + 1))
    raise RuntimeError("unreachable")


def count(query):
    filt = (
        "title_and_abstract.search:"
        + query
        + ",from_publication_date:2020-01-01,to_publication_date:2026-09-29"
    )
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(
        {"filter": filt, "per-page": "5", "select": "display_name,publication_year"}
    )
    data = fetch(url)
    print(data["meta"]["count"], "|", query)
    for work in data["results"]:
        print(" -", work.get("publication_year"), work.get("display_name"))
    print()
    time.sleep(1)


if __name__ == "__main__":
    for query in QUERIES:
        count(query)
