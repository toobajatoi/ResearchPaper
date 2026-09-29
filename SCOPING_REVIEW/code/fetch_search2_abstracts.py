"""Fetch abstracts for the five PubMed Search 2 titles kept for abstract reading."""

import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PMIDS = ["42507678", "42277102", "41982350", "39752663", "35071147"]


def main():
    data = urllib.parse.urlencode(
        {"db": "pubmed", "id": ",".join(PMIDS), "retmode": "xml"}
    ).encode()
    req = urllib.request.Request(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
        data=data,
        headers={"User-Agent": "HMC-scoping-review"},
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        root = ET.fromstring(resp.read())
    out = []
    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID") or ""
        title = "".join((article.find(".//ArticleTitle") or article).itertext()) if article.find(".//ArticleTitle") is not None else ""
        parts = []
        for node in article.findall(".//AbstractText"):
            text = "".join(node.itertext()).strip()
            if text:
                parts.append(text)
        out.append(f"PMID {pmid}\n{title}\n\n" + "\n".join(parts) + "\n")
    dest = ROOT / "data" / "pubmed" / "search2_kept_abstracts.txt"
    dest.write_text("\n---\n".join(out), encoding="utf-8")
    print("wrote", len(out), flush=True)


if __name__ == "__main__":
    main()
