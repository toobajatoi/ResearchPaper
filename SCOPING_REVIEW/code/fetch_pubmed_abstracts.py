"""Fetch abstracts for PubMed records retained at title screening."""

import csv
import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
OUT = ROOT / "data" / "pubmed" / "retained_abstracts.json"


def fetch(pmids):
    data = urllib.parse.urlencode(
        {"db": "pubmed", "id": ",".join(pmids), "retmode": "xml"}
    ).encode()
    req = urllib.request.Request(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
        data=data,
        headers={"User-Agent": "HMC-scoping-review"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def abstract_text(article):
    parts = []
    for node in article.findall(".//AbstractText"):
        label = node.attrib.get("Label")
        text = "".join(node.itertext()).strip()
        if not text:
            continue
        parts.append(f"{label}: {text}" if label else text)
    return "\n".join(parts)


def main():
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            if row["source"] == "PubMed supplementary Search 1"
            and row["decision"] == "retain_for_abstract"
        ]
    pmids = [row["identifier"].replace("PMID:", "") for row in rows]
    records = []
    for start in range(0, len(pmids), 40):
        batch = pmids[start : start + 40]
        root = ET.fromstring(fetch(batch))
        for article in root.findall(".//PubmedArticle"):
            pmid = article.findtext(".//PMID") or ""
            title = "".join(article.find(".//ArticleTitle").itertext()) if article.find(".//ArticleTitle") is not None else ""
            journal = article.findtext(".//Journal/Title") or ""
            year = article.findtext(".//PubDate/Year") or article.findtext(".//PubDate/MedlineDate") or ""
            authors = []
            for author in article.findall(".//Author"):
                last = author.findtext("LastName") or ""
                initials = author.findtext("Initials") or ""
                collective = author.findtext("CollectiveName") or ""
                authors.append(collective or f"{last} {initials}".strip())
            doi = ""
            for loc in article.findall(".//ArticleId"):
                if loc.attrib.get("IdType") == "doi":
                    doi = loc.text or ""
            records.append(
                {
                    "pmid": pmid,
                    "title": title,
                    "authors": "; ".join(authors),
                    "journal": journal,
                    "year": year,
                    "doi": doi,
                    "abstract": abstract_text(article),
                }
            )
        print(f"abstracts {len(records)}", flush=True)
        time.sleep(0.4)
    OUT.write_text(json.dumps({"n": len(records), "items": records}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("saved", len(records))


if __name__ == "__main__":
    main()
