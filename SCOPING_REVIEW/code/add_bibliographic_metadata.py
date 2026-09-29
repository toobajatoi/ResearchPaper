"""Fill empty year, venue, DOI, and URL cells. Never overwrite a cell that already has text.

Call this at the end of build_evidence_matrix.py. Hand-entered values survive a rebuild
because the rebuild snapshots them first and this script writes the snapshot back.
"""

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "evidence_matrix.csv"
SCREEN = ROOT / "data" / "screening.csv"
PUBMED_FILES = [
    ROOT / "data" / "pubmed" / "search1_summaries.json",
    ROOT / "data" / "pubmed" / "search2_records.json",
]
OPENALEX = ROOT / "data" / "openalex" / "search1_narrow_anthropomorph_llm.csv"
KEEP = ("year", "venue", "doi", "url")


def norm_doi(value):
    text = (value or "").strip()
    text = re.sub(r"^https?://(dx\.)?doi\.org/", "", text, flags=re.I)
    text = re.sub(r"^doi:\s*", "", text, flags=re.I)
    return text.strip()


def pubmed_by_pmid():
    found = {}
    for path in PUBMED_FILES:
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for item in data.get("items") or []:
            found[str(item.get("pmid"))] = item
    return found


def openalex_by_doi():
    found = {}
    if not OPENALEX.exists():
        return found
    with OPENALEX.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            doi = norm_doi(row.get("doi"))
            if doi:
                found[doi.lower()] = row
            match = re.search(r"arxiv\.org/(?:abs|pdf)/(\d+\.\d+)", row.get("url") or "", re.I)
            if match:
                found["arxiv:" + match.group(1)] = row
    return found


def screening_by_id():
    found = {}
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            found[row["identifier"]] = row
    return found


def fill_from_sources(row, screen, pubmed, alex):
    study_id = row.get("study_id") or ""
    screen_row = screen.get(study_id) or screen.get(row.get("doi") or "")
    pmid = study_id.replace("PMID:", "") if study_id.startswith("PMID:") else ""
    pub = pubmed.get(pmid) or {}
    doi = norm_doi(pub.get("doi") or "")
    if not doi:
        doi = norm_doi(row.get("doi") or "")
    if not doi and screen_row:
        doi = norm_doi(screen_row.get("identifier") or "")
    arxiv_match = re.search(r"arxiv\.org/abs/(\d+\.\d+)", study_id, re.I)
    alex_row = alex.get(doi.lower()) if doi else None
    if alex_row is None and arxiv_match:
        alex_row = alex.get("arxiv:" + arxiv_match.group(1))
    if not row.get("year"):
        row["year"] = (screen_row or {}).get("year") or (alex_row or {}).get("year") or ""
        if not row["year"] and pub.get("pubdate"):
            match = re.search(r"(20\d\d)", pub["pubdate"])
            row["year"] = match.group(1) if match else ""
    if not row.get("venue"):
        row["venue"] = pub.get("source") or (alex_row or {}).get("venue") or ""
    row["doi"] = doi if doi.startswith("10.") else ""
    if not row.get("url"):
        if doi.startswith("10."):
            row["url"] = "https://doi.org/" + doi
        elif screen_row and screen_row.get("identifier", "").startswith("http"):
            row["url"] = screen_row["identifier"]
        elif alex_row and alex_row.get("url"):
            row["url"] = alex_row["url"]
    return row


def apply(previous=None):
    previous = previous or {}
    with MATRIX.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0].keys()) if rows else []
    screen = screening_by_id()
    pubmed = pubmed_by_pmid()
    alex = openalex_by_doi()
    for row in rows:
        saved = previous.get(row.get("study_id"), {})
        row = fill_from_sources(row, screen, pubmed, alex)
        for key in ("year", "venue", "url"):
            if saved.get(key):
                row[key] = saved[key]
        saved_doi = norm_doi(saved.get("doi") or "")
        if saved_doi.startswith("10."):
            row["doi"] = saved_doi
    with MATRIX.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    filled = {key: sum(1 for row in rows if row.get(key)) for key in KEEP}
    print("bibliographic", filled, "rows", len(rows))
    return rows


if __name__ == "__main__":
    apply()
