"""Download open arXiv PDFs from the full-text queue and extract text.

Files stay in the gitignored oa_attempts folder. Does not change the screening log.
"""

import json
import re
import time
import urllib.request
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
LOOKUP = ROOT / "data" / "fulltext" / "queue_oa_lookup.json"
OUT = ROOT / "data" / "fulltext" / "oa_attempts" / "queue_arxiv"
OUT.mkdir(parents=True, exist_ok=True)


def safe_name(doi_or_id):
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", doi_or_id)[:80]


def main():
    items = json.loads(LOOKUP.read_text(encoding="utf-8"))
    kept = []
    for item in items:
        url = item.get("pdf_url") or item.get("oa_url") or ""
        if "arxiv.org/pdf" not in url and "arxiv.org/pdf" not in (item.get("oa_url") or ""):
            continue
        pdf_url = item.get("pdf_url") or item.get("oa_url")
        if not pdf_url.endswith(".pdf") and "/pdf/" in pdf_url:
            pdf_url = pdf_url.split("?")[0]
        name = safe_name(item.get("doi") or item["identifier"])
        dest = OUT / f"{name}.pdf"
        if not dest.exists() or dest.stat().st_size < 1000:
            req = urllib.request.Request(pdf_url, headers={"User-Agent": "HMC-scoping-review"})
            try:
                with urllib.request.urlopen(req, timeout=90) as resp:
                    dest.write_bytes(resp.read())
                print("got", name, dest.stat().st_size, flush=True)
            except Exception as exc:
                print("fail", name, exc, flush=True)
                continue
            time.sleep(0.4)
        doc = fitz.open(dest)
        text = "\n".join(page.get_text() for page in doc)
        (OUT / f"{name}.txt").write_text(text, encoding="utf-8")
        kept.append((name, item["title"], len(text)))
        print("text", name, len(text), flush=True)
    print("done", len(kept))


if __name__ == "__main__":
    main()
