"""Record OpenAlex reported counts only. Does not export records."""

import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "code" / "openalex_search.py"
OUT = ROOT / "data" / "openalex" / "counts_2026-09-29.json"

# Import the query strings by executing the assignments only.
namespace = {}
text = SRC.read_text(encoding="utf-8")
start = text.index("SEARCH_1 = ")
end = text.index("QUERIES = ")
exec(text[start:end], namespace)


def count(query):
    filt = (
        f"title_and_abstract.search:{query},"
        "from_publication_date:2020-01-01,"
        "to_publication_date:2026-09-29"
    )
    params = urllib.parse.urlencode({"filter": filt, "per-page": "1"})
    url = "https://api.openalex.org/works?" + params
    req = urllib.request.Request(url, headers={"User-Agent": "HMC-scoping-review"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.load(resp)
    return data.get("meta", {}).get("count")


def main():
    names = {
        "search1_primary": namespace["SEARCH_1"],
        "search2_sensitivity": namespace["SEARCH_2"],
        "casa_extra": namespace["CASA"],
    }
    rows = {}
    for name, query in names.items():
        rows[name] = count(query)
        print(name, rows[name], flush=True)
    OUT.write_text(json.dumps({"search_date": "2026-09-29", "counts": rows}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
