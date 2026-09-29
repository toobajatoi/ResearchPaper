"""Locate arXiv records for seed papers and the 11 PubMed items still awaiting full text."""

import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "fulltext" / "arxiv_locate.json"

QUERIES = [
    ("seed_devrio", 'ti:"taxonomy of linguistic expressions" AND ti:anthropomorphism'),
    ("seed_ibrahim", "id:2502.07077"),
    ("seed_acl_dehumanizing", 'ti:"dehumanizing machines"'),
    ("shanahan", 'ti:"role play" AND ti:"large language models"'),
    ("pmid_42648233", 'ti:"seeing humans in technology"'),
    ("pmid_42463863", 'ti:"stickiness intentions"'),
    ("pmid_42269974", 'ti:"engagement-validation loop"'),
    ("pmid_41548427", 'ti:"therapy chatbots and emotional complexity"'),
    ("pmid_40810905", 'ti:"IPALLM"'),
    ("pmid_40694494", 'ti:"epistemic trust" AND ti:conversational'),
    ("pmid_40562106", 'ti:"depression intervention" AND ti:chatbots'),
    ("pmid_40286349", 'ti:"cringe, lit, or mid"'),
    ("pmid_38428201", 'ti:"unlocking human-like conversations"'),
    ("pmid_35976080", 'ti:"when a chatbot smiles"'),
]


def search(query):
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": query, "start": 0, "max_results": 3}
    )
    req = urllib.request.Request(url, headers={"User-Agent": "HMC-scoping-review"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read()
    root = ET.fromstring(raw)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    hits = []
    for entry in root.findall("a:entry", ns):
        title = "".join(entry.findtext("a:title", default="", namespaces=ns).split())
        pdf = ""
        for link in entry.findall("a:link", ns):
            if link.attrib.get("title") == "pdf":
                pdf = link.attrib.get("href", "")
        hits.append(
            {
                "id": entry.findtext("a:id", default="", namespaces=ns),
                "title": title,
                "pdf": pdf,
            }
        )
    return hits


def main():
    found = []
    for name, query in QUERIES:
        try:
            hits = search(query)
            print(name, len(hits), hits[0]["title"][:80] if hits else "-", flush=True)
        except Exception as exc:
            hits = []
            print("FAIL", name, type(exc).__name__, exc, flush=True)
        found.append({"name": name, "query": query, "hits": hits})
    OUT.write_text(json.dumps(found, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
