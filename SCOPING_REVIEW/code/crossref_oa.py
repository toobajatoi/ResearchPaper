"""Ask Crossref whether the remaining no-PMC papers have an open PDF link."""

import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AVAIL = ROOT / "data" / "fulltext" / "availability.json"
OUT = ROOT / "data" / "fulltext" / "crossref_missing.json"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "HMC-scoping-review (mailto:local)"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def main():
    rows = json.loads(AVAIL.read_text(encoding="utf-8"))
    missing = [row for row in rows if not row.get("pmcid")]
    found = []
    for row in missing:
        doi = row["doi"]
        url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
        try:
            data = get(url)["message"]
        except Exception as exc:
            found.append({**row, "error": f"{type(exc).__name__}: {exc}"})
            print("FAIL", doi, type(exc).__name__, flush=True)
            continue
        links = []
        for link in data.get("link") or []:
            links.append(
                {
                    "url": link.get("URL"),
                    "content-type": link.get("content-type"),
                    "intended-application": link.get("intended-application"),
                }
            )
        item = {
            "pmid": row["pmid"],
            "doi": doi,
            "title": row["title"],
            "license": [lic.get("URL") for lic in data.get("license") or []],
            "links": links,
        }
        found.append(item)
        print(row["pmid"], item["license"], len(links), flush=True)
    OUT.write_text(json.dumps(found, indent=2), encoding="utf-8")
    print("wrote", len(found))


if __name__ == "__main__":
    main()
