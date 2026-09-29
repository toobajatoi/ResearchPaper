"""Download HMC PDFs after visiting the article page, so the site sets a cookie."""

import csv
import http.cookiejar
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "data" / "screening.csv"
OUT = ROOT / "data" / "fulltext" / "hmc"
OUT.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/pdf,*/*",
}


def pdf_and_page(identifier):
    parts = [part.strip() for part in identifier.split("|")]
    pdf = next((part for part in parts if part.endswith(".pdf")), "")
    page = next((part for part in parts if "stars.library.ucf.edu/hmc/vol" in part and not part.endswith(".pdf")), "")
    return pdf, page


def main():
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    with SCREEN.open(encoding="utf-8", newline="") as handle:
        rows = [row for row in csv.DictReader(handle) if row["source"].startswith("HMC") and row["decision"] == "retain_for_full_text"]
    for row in rows:
        pdf, page = pdf_and_page(row["identifier"])
        dest = OUT / f"hmc_{int(row['record_number']):03d}.pdf"
        if dest.exists() and dest.stat().st_size > 5000:
            print("exists", dest.name)
            continue
        try:
            if page:
                req = urllib.request.Request(page, headers=HEADERS)
                opener.open(req, timeout=60).read()
            req = urllib.request.Request(pdf, headers={**HEADERS, "Referer": page or "https://stars.library.ucf.edu/hmc/"})
            data = opener.open(req, timeout=120).read()
            dest.write_bytes(data)
            print(dest.name, len(data), data[:5])
        except Exception as exc:
            print("FAIL", row["record_number"], type(exc).__name__, exc)


if __name__ == "__main__":
    main()
