"""Pull language statements from open PDFs of included studies.

Writes snippets only. Does not edit the evidence matrix.
"""

import csv
import re
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "evidence_matrix.csv"
OUT = ROOT / "data" / "fulltext" / "oa_attempts" / "language_snippets.txt"
PDF_DIR = ROOT / "data" / "fulltext" / "oa_attempts" / "included_pdfs"

LANG_RE = re.compile(
    r".{0,80}\b(English|Korean|Japanese|Chinese|Arabic|Urdu|Spanish|French|German|Hindi|multilingual|language of|in English|languages)\b.{0,80}",
    re.I,
)


def pdf_url(row):
    sid = row["study_id"]
    url = row.get("url") or ""
    if "aclanthology.org/" in sid and sid.endswith("/"):
        return sid.rstrip("/") + ".pdf"
    if "arxiv.org/abs/" in sid:
        return sid.replace("/abs/", "/pdf/") + ".pdf"
    if "arxiv.org" in url and "/abs/" in url:
        return url.replace("/abs/", "/pdf/") + ".pdf"
    if sid.startswith("https://doi.org/10.48550/arxiv."):
        arx = sid.rsplit("arxiv.", 1)[-1]
        return f"https://arxiv.org/pdf/{arx}.pdf"
    return ""


def main():
    import urllib.request

    rows = list(csv.DictReader(MATRIX.open(encoding="utf-8")))
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    parts = []
    for row in rows:
        lang = (row.get("language_of_communication") or "").strip()
        if not lang.lower().startswith("not stated"):
            continue
        url = pdf_url(row)
        if not url:
            parts.append(f"NOURL {row['study_id']}\n")
            continue
        dest = PDF_DIR / (re.sub(r"[^\w.]+", "_", row["study_id"])[:80] + ".pdf")
        if not dest.exists() or dest.stat().st_size < 1000:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            try:
                with urllib.request.urlopen(req, timeout=40) as resp:
                    data = resp.read()
                dest.write_bytes(data)
                status = f"saved {len(data)}"
            except Exception as exc:
                parts.append(f"FAIL {row['study_id']}\n{url}\n{type(exc).__name__}: {exc}\n")
                continue
        else:
            status = "cached"
        try:
            doc = fitz.open(dest)
            text = "\n".join(page.get_text() for page in doc[:8])
        except Exception as exc:
            parts.append(f"BADPDF {row['study_id']} {status} {exc}\n")
            continue
        hits = LANG_RE.findall(text)
        snippets = []
        for match in LANG_RE.finditer(text):
            snippets.append(" ".join(match.group(0).split()))
            if len(snippets) >= 6:
                break
        parts.append(
            f"OK {row['study_id']} {status} pages {doc.page_count}\n"
            + ("\n".join(snippets) if snippets else "(no language word in first 8 pages)")
            + "\n"
        )
        print("ok", row["study_id"][:60], status, "hits", len(snippets))
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
